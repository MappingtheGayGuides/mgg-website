#!/usr/bin/env python3
"""
Quick script to add an amenity to a location
Usage: python quick_add_amenity.py <location_id> <amenity_name>
Example: python quick_add_amenity.py 123 "Dance Floor"
"""

import sys
from pathlib import Path

# Add the current directory to the path so we can import our Flask app
sys.path.append(str(Path(__file__).parent))

from app import app, db
from models import Location, AmenityFeature, LocationAmenityAssignment

def quick_add_amenity(location_id, amenity_name):
    """Quickly add an amenity to a location"""
    with app.app_context():
        # Test database connection first
        try:
            from sqlalchemy import text
            db.session.execute(text('SELECT 1'))
        except Exception as e:
            print(f"Database connection failed: {e}")
            return False
        # Get the location
        location = db.session.get(Location, location_id)
        if not location:
            print(f"Error: Location with ID {location_id} not found!")
            return False
        
        # Get or create the amenity
        amenity = db.session.query(AmenityFeature).filter_by(name=amenity_name).first()
        if not amenity:
            # Create new amenity
            amenity = AmenityFeature(name=amenity_name)
            db.session.add(amenity)
            db.session.flush()  # Get the ID
            print(f"Created new amenity: '{amenity_name}'")
        
        # Check if this assignment already exists
        existing = db.session.query(LocationAmenityAssignment).filter_by(
            location_id=location_id, 
            amenity_id=amenity.id
        ).first()
        
        if existing:
            print(f"'{amenity_name}' is already assigned to '{location.title}'")
            return True
        
        # Create the assignment
        assignment = LocationAmenityAssignment(
            location_id=location_id,
            amenity_id=amenity.id
        )
        
        try:
            db.session.add(assignment)
            db.session.commit()
            print(f"Successfully added '{amenity_name}' to '{location.title}'!")
            return True
        except Exception as e:
            print(f"Error adding amenity: {e}")
            db.session.rollback()
            return False

def main():
    if len(sys.argv) != 3:
        print("Usage: python quick_add_amenity.py <location_id> <amenity_name>")
        print("Example: python quick_add_amenity.py 123 'Dance Floor'")
        sys.exit(1)
    
    try:
        location_id = int(sys.argv[1])
        amenity_name = sys.argv[2]
        
        success = quick_add_amenity(location_id, amenity_name)
        if success:
            sys.exit(0)
        else:
            sys.exit(1)
            
    except ValueError:
        print("Error: location_id must be a number")
        sys.exit(1)

if __name__ == '__main__':
    main()
