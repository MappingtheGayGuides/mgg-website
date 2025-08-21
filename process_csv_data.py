#!/usr/bin/env python3
"""
CSV data processing script for Mapping the Gay Guides
Processes CSV data and properly splits comma-separated values into individual records
"""

import csv
import sqlite3
import os
from pathlib import Path
from datetime import datetime

def split_comma_values(value):
    """Split comma-separated values and clean them up"""
    if not value or value.strip() == 'NA':
        return []
    
    # Split by comma and clean each value
    values = [v.strip() for v in value.split(',')]
    # Remove empty strings and 'NA' values
    values = [v for v in values if v and v != 'NA']
    return values

def create_unique_locations(csv_path, conn):
    """Create unique_locations table from CSV data"""
    print("📍 Step 1: Creating unique locations from coordinate data...")
    
    cursor = conn.cursor()
    unique_coords = set()
    unique_locations = {}
    
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            lat = row.get('lat', '').strip()
            lon = row.get('lon', '').strip()
            
            if lat and lon and lat != 'NA' and lon != 'NA':
                try:
                    lat_float = float(lat)
                    lon_float = float(lon)
                    coord_key = (lat_float, lon_float, row.get('city', '').strip(), row.get('state', '').strip())
                    
                    if coord_key not in unique_coords:
                        unique_coords.add(coord_key)
                        
                        # Determine address precision
                        if row.get('unclear_address', '').strip() == 'NA':
                            precision = 'exact'
                        elif row.get('unclear_address', '').strip():
                            precision = 'approximate'
                        else:
                            precision = 'general'
                        
                        # Insert unique location
                        cursor.execute("""
                            INSERT INTO unique_locations (latitude, longitude, city, state, address_precision)
                            VALUES (?, ?, ?, ?, ?)
                        """, (lat_float, lon_float, row.get('city', '').strip(), row.get('state', '').strip(), precision))
                        
                        unique_locations[coord_key] = cursor.lastrowid
                        
                except (ValueError, TypeError):
                    continue
    
    conn.commit()
    print(f"✅ Created {len(unique_locations)} unique locations")
    return unique_locations

def create_lookup_tables(csv_path, conn):
    """Create lookup tables for types and amenity features with proper splitting"""
    print("🏷️ Step 2: Creating lookup tables with split values...")
    
    cursor = conn.cursor()
    type_names = set()
    amenity_names = set()
    
    # First pass: collect all unique values after splitting
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            type_val = row.get('type', '').strip()
            amenity_val = row.get('amenityfeatures', '').strip()
            
            # Split and add type values
            if type_val and type_val != 'NA':
                split_types = split_comma_values(type_val)
                type_names.update(split_types)
            
            # Split and add amenity values
            if amenity_val and amenity_val != 'NA':
                split_amenities = split_comma_values(amenity_val)
                amenity_names.update(split_amenities)
    
    # Create type lookup table
    type_lookup = {}
    for type_name in type_names:
        cursor.execute("""
            INSERT INTO location_types (name) VALUES (?)
        """, (type_name,))
        type_lookup[type_name] = cursor.lastrowid
    
    # Create amenity feature lookup table
    amenity_lookup = {}
    for amenity_name in amenity_names:
        cursor.execute("""
            INSERT INTO amenity_features (name) VALUES (?)
        """, (amenity_name,))
        amenity_lookup[amenity_name] = cursor.lastrowid
    
    # Commit lookup tables
    conn.commit()
    print(f"✅ Created {len(type_lookup)} location types and {len(amenity_lookup)} amenity features")
    return type_lookup, amenity_lookup

def import_locations(csv_path, unique_locations, type_lookup, amenity_lookup, conn):
    """Import locations with proper many-to-many relationships"""
    print("📍 Step 3: Importing locations with split value relationships...")
    
    cursor = conn.cursor()
    
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row_num, row in enumerate(reader, 1):
            try:
                # Get coordinates for unique_location_id lookup
                lat = row.get('lat', '').strip()
                lon = row.get('lon', '').strip()
                city = row.get('city', '').strip()
                state = row.get('state', '').strip()
                
                unique_location_id = None
                if lat and lon and lat != 'NA' and lon != 'NA':
                    try:
                        lat_float = float(lat)
                        lon_float = float(lon)
                        coord_key = (lat_float, lon_float, city, state)
                        unique_location_id = unique_locations.get(coord_key)
                    except (ValueError, TypeError):
                        pass
                
                # Insert location
                cursor.execute("""
                    INSERT INTO locations (
                        unique_id, title, description, street_address, city, state, year,
                        notes, full_address, latitude, longitude, geo_address,
                        unclear_address, status, unique_location_id
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    row.get('unique-id', '').strip(),
                    row.get('title', '').strip(),
                    row.get('description', '').strip(),
                    row.get('streetaddress', '').strip(),
                    city,
                    state,
                    int(row.get('Year', 0)) if row.get('Year') and row.get('Year').strip() and row.get('Year').strip() != 'NA' else None,
                    row.get('notes', '').strip(),
                    row.get('full.address', '').strip(),
                    float(row.get('lat', 0)) if lat and lat != 'NA' else None,
                    float(row.get('lon', 0)) if lon and lon != 'NA' else None,
                    row.get('geoAddress', '').strip(),
                    row.get('unclear_address', '').strip(),
                    row.get('status', '').strip(),
                    unique_location_id
                ))
                
                location_id = cursor.lastrowid
                
                # Create type assignments (split values)
                type_val = row.get('type', '').strip()
                if type_val and type_val != 'NA':
                    split_types = split_comma_values(type_val)
                    for type_name in split_types:
                        if type_name in type_lookup:
                            cursor.execute("""
                                INSERT INTO location_type_assignments (location_id, type_id)
                                VALUES (?, ?)
                            """, (location_id, type_lookup[type_name]))
                
                # Create amenity feature assignments (split values)
                amenity_val = row.get('amenityfeatures', '').strip()
                if amenity_val and amenity_val != 'NA':
                    split_amenities = split_comma_values(amenity_val)
                    for amenity_name in split_amenities:
                        if amenity_name in amenity_lookup:
                            cursor.execute("""
                                INSERT INTO location_amenity_assignments (location_id, amenity_id)
                                VALUES (?, ?)
                            """, (location_id, amenity_lookup[amenity_name]))
                
                if row_num % 1000 == 0:
                    print(f"Processed {row_num} rows...")
                    
            except Exception as e:
                print(f"Error processing row {row_num}: {e}")
                continue
    
    # Commit all changes
    conn.commit()
    print(f"✅ Successfully imported {row_num} locations with proper relationships!")

def main():
    """Main processing function"""
    print("🚀 Starting CSV data processing for Mapping the Gay Guides...")
    
    # Path to your CSV file
    csv_path = Path(__file__).parent / "data" / "raw" / "mgg-data-8-21-2025.csv"
    
    if not csv_path.exists():
        print(f"❌ CSV file not found at: {csv_path}")
        print("Please place your CSV file in the data/raw/ directory")
        return
    
    # Connect to database
    conn = sqlite3.connect('mgg.db')
    
    try:
        # Step 1: Create unique locations
        unique_locations = create_unique_locations(csv_path, conn)
        
        # Step 2: Create lookup tables with split values
        type_lookup, amenity_lookup = create_lookup_tables(csv_path, conn)
        
        # Step 3: Import locations with relationships
        import_locations(csv_path, unique_locations, type_lookup, amenity_lookup, conn)
        
        print("\n🎉 Data processing complete!")
        print(f"Database file: {Path('mgg.db').absolute()}")
        
    except Exception as e:
        print(f"❌ Error during processing: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    main()
