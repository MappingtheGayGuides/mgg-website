#!/usr/bin/env python3
"""
Data import script for Mapping the Gay Guides
Imports CSV data into the SQLite database exactly as-is
"""

import csv
import os
import sys
from pathlib import Path
from decimal import Decimal

# Add the parent directory to the path so we can import our Flask app
sys.path.append(str(Path(__file__).parent.parent.parent))

from app import app, db
from models import Location, UniqueLocation, LocationType, AmenityFeature, LocationTypeAssignment, LocationAmenityAssignment

def create_unique_locations_from_csv(csv_path):
    """Create unique_locations table from CSV data to avoid duplicate coordinates"""
    print("Creating unique locations from coordinate data...")
    
    unique_coords = set()
    unique_locations = {}
    
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            try:
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
                            
                            # Create unique location
                            unique_loc = UniqueLocation(
                                latitude=lat_float,
                                longitude=lon_float,
                                city=row.get('city', '').strip(),
                                state=row.get('state', '').strip(),
                                address_precision=precision
                            )
                            
                            db.session.add(unique_loc)
                            db.session.flush()  # Get the ID
                            
                            unique_locations[coord_key] = unique_loc.id
                            
                    except (ValueError, TypeError):
                        continue
                        
            except Exception as e:
                print(f"Error processing coordinates in row: {e}")
                continue
    
    # Commit unique locations
    try:
        db.session.commit()
        print(f"Created {len(unique_locations)} unique locations")
        return unique_locations
    except Exception as e:
        print(f"Error committing unique locations: {e}")
        db.session.rollback()
        return {}

def create_lookup_tables_from_csv(csv_path):
    """Create lookup tables for types and amenity features"""
    print("Creating lookup tables from CSV data...")
    
    type_names = set()
    amenity_names = set()
    
    # First pass: collect all unique values
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            type_val = row.get('type', '').strip()
            amenity_val = row.get('amenityfeatures', '').strip()
            
            if type_val and type_val != 'NA':
                type_names.add(type_val)
            
            if amenity_val and amenity_val != 'NA':
                amenity_names.add(amenity_val)
    
    # Create type lookup table
    type_lookup = {}
    for type_name in type_names:
        location_type = LocationType(name=type_name)
        db.session.add(location_type)
        db.session.flush()  # Get the ID
        type_lookup[type_name] = location_type.id
    
    # Create amenity feature lookup table
    amenity_lookup = {}
    for amenity_name in amenity_names:
        amenity_feature = AmenityFeature(name=amenity_name)
        db.session.add(amenity_feature)
        db.session.flush()  # Get the ID
        amenity_lookup[amenity_name] = amenity_feature.id
    
    # Commit lookup tables
    try:
        db.session.commit()
        print(f"Created {len(type_lookup)} location types and {len(amenity_lookup)} amenity features")
        return type_lookup, amenity_lookup
    except Exception as e:
        print(f"Error committing lookup tables: {e}")
        db.session.rollback()
        return {}, {}

def import_locations_from_csv(csv_path, unique_locations, type_lookup, amenity_lookup):
    """Import locations from CSV file with proper lookup table relationships"""
    print(f"Importing locations from {csv_path}...")
    
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
                
                # Create location object from CSV row - EXACTLY as-is
                location = Location(
                    unique_id=row.get('unique-id', '').strip(),
                    title=row.get('title', '').strip(),
                    description=row.get('description', '').strip(),
                    street_address=row.get('streetaddress', '').strip(),
                    city=city,
                    state=state,
                    year=int(row.get('Year', 0)) if row.get('Year') and row.get('Year').strip() and row.get('Year').strip() != 'NA' else None,
                    notes=row.get('notes', '').strip(),
                    full_address=row.get('full.address', '').strip(),
                    latitude=float(row.get('lat', 0)) if lat and lat != 'NA' else None,
                    longitude=float(row.get('lon', 0)) if lon and lon != 'NA' else None,
                    geo_address=row.get('geoAddress', '').strip(),
                    unclear_address=row.get('unclear_address', '').strip(),
                    status=row.get('status', '').strip(),
                    unique_location_id=unique_location_id
                )
                
                db.session.add(location)
                db.session.flush()  # Get the location ID
                
                # Create type assignments
                type_val = row.get('type', '').strip()
                if type_val and type_val != 'NA' and type_val in type_lookup:
                    type_assignment = LocationTypeAssignment(
                        location_id=location.id,
                        type_id=type_lookup[type_val]
                    )
                    db.session.add(type_assignment)
                
                # Create amenity feature assignments
                amenity_val = row.get('amenityfeatures', '').strip()
                if amenity_val and amenity_val != 'NA' and amenity_val in amenity_lookup:
                    amenity_assignment = LocationAmenityAssignment(
                        location_id=location.id,
                        amenity_id=amenity_lookup[amenity_val]
                    )
                    db.session.add(amenity_assignment)
                
                if row_num % 100 == 0:
                    print(f"Processed {row_num} rows...")
                    
            except Exception as e:
                print(f"Error processing row {row_num}: {e}")
                print(f"Row data: {row}")
                continue
    
    # Commit all changes
    try:
        db.session.commit()
        print(f"Successfully imported {row_num} locations with lookup table relationships!")
    except Exception as e:
        print(f"Error committing to database: {e}")
        db.session.rollback()

def main():
    """Main import function"""
    print("🚀 Starting data import for Mapping the Gay Guides...")
    
    # Path to your CSV file
    csv_path = Path(__file__).parent.parent / "raw" / "mgg-data-8-21-2025.csv"
    
    if not csv_path.exists():
        print(f"❌ CSV file not found at: {csv_path}")
        print("Please place your CSV file in the data/raw/ directory")
        return
    
    with app.app_context():
        # First create unique locations
        print("📍 Step 1: Creating unique locations...")
        unique_locations = create_unique_locations_from_csv(csv_path)
        
        # Then create lookup tables
        print("🏷️ Step 2: Creating lookup tables...")
        type_lookup, amenity_lookup = create_lookup_tables_from_csv(csv_path)
        
        # Finally import all location data with relationships
        print("📍 Step 3: Importing locations with relationships...")
        import_locations_from_csv(csv_path, unique_locations, type_lookup, amenity_lookup)
        
        print("✅ Data import complete!")
        print(f"Database file: {Path('mgg.db').absolute()}")

if __name__ == "__main__":
    main()
