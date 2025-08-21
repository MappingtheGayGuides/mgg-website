#!/usr/bin/env python3
"""
Data import script for Mapping the Gay Guides
Imports CSV data into the SQLite database
"""

import csv
import os
import sys
from pathlib import Path

# Add the parent directory to the path so we can import our Flask app
sys.path.append(str(Path(__file__).parent.parent.parent))

from app import app, db
from models import Location, Article

def import_locations_from_csv(csv_path):
    """Import locations from CSV file"""
    print(f"Importing locations from {csv_path}...")
    
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row_num, row in enumerate(reader, 1):
            try:
                # Create location object from CSV row
                # Adjust these field mappings based on your CSV structure
                location = Location(
                    name=row.get('name', '').strip(),
                    address=row.get('address', '').strip(),
                    city=row.get('city', '').strip(),
                    state=row.get('state', '').strip(),
                    zip_code=row.get('zip_code', '').strip(),
                    latitude=float(row.get('latitude', 0)) if row.get('latitude') else None,
                    longitude=float(row.get('longitude', 0)) if row.get('longitude') else None,
                    category=row.get('category', '').strip(),
                    year_listed=int(row.get('year_listed', 0)) if row.get('year_listed') else None,
                    guide_edition=row.get('guide_edition', '').strip(),
                    description=row.get('description', '').strip(),
                    notes=row.get('notes', '').strip()
                )
                
                db.session.add(location)
                
                if row_num % 100 == 0:
                    print(f"Processed {row_num} rows...")
                    
            except Exception as e:
                print(f"Error processing row {row_num}: {e}")
                print(f"Row data: {row}")
                continue
    
    # Commit all changes
    try:
        db.session.commit()
        print(f"Successfully imported {row_num} locations!")
    except Exception as e:
        print(f"Error committing to database: {e}")
        db.session.rollback()

def main():
    """Main import function"""
    print("🚀 Starting data import for Mapping the Gay Guides...")
    
    # Path to your CSV file
    csv_path = Path(__file__).parent.parent / "raw" / "your_data.csv"
    
    if not csv_path.exists():
        print(f"❌ CSV file not found at: {csv_path}")
        print("Please place your CSV file in the data/raw/ directory")
        return
    
    with app.app_context():
        # Import locations
        import_locations_from_csv(csv_path)
        
        print("✅ Data import complete!")
        print(f"Database file: {Path('mgg.db').absolute()}")

if __name__ == "__main__":
    main()
