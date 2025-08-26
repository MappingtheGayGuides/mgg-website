#!/usr/bin/env python3
"""
Script to add amenities to locations in the Mapping Gay Guides database
Usage: python add_amenity.py
"""

import sys
from pathlib import Path

# Add the current directory to the path so we can import our Flask app
sys.path.append(str(Path(__file__).parent))

from app import app, db
from models import Location, AmenityFeature, LocationAmenityAssignment

def list_all_locations():
    """List all locations with their unique IDs and titles"""
    locations = db.session.query(Location).all()
    print("\n=== Available Locations ===")
    for loc in locations:
        print(f"Unique ID: {loc.unique_id} | {loc.title} | {loc.city}, {loc.state} | Year: {loc.year}")
        print(f"    Database ID: {loc.id}")
    return locations

def list_all_amenities():
    """List all available amenities"""
    amenities = db.session.query(AmenityFeature).all()
    print("\n=== Available Amenities ===")
    for amenity in amenities:
        print(f"ID: {amenity.id} | {amenity.name}")
        if amenity.description:
            print(f"    Description: {amenity.description}")
    return amenities

def search_amenities_by_name(search_term):
    """Search for amenities by name (partial match)"""
    amenities = db.session.query(AmenityFeature).filter(
        AmenityFeature.name.ilike(f'%{search_term}%')
    ).all()
    
    if not amenities:
        print(f"No amenities found matching '{search_term}'")
        return []
    
    print(f"\n=== Amenities matching '{search_term}' ===")
    for amenity in amenities:
        print(f"ID: {amenity.id} | {amenity.name}")
        if amenity.description:
            print(f"    Description: {amenity.description}")
    
    return amenities

def get_location_by_unique_id(unique_id):
    """Get a location by its unique ID (e.g., d-1998-01297)"""
    location = db.session.query(Location).filter_by(unique_id=unique_id).first()
    return location

def list_location_amenities(unique_id):
    """List all amenities for a specific location"""
    location = get_location_by_unique_id(unique_id)
    if not location:
        print(f"Location with unique ID '{unique_id}' not found!")
        return
    
    print(f"\n=== Amenities for: {location.title} ===")
    if location.amenities:
        for amenity in location.amenities:
            print(f"• {amenity.name}")
    else:
        print("No amenities assigned yet.")
    
    return location

def add_amenity_to_location(unique_id, amenity_id):
    """Add an amenity to a location"""
    # Check if both exist
    location = get_location_by_unique_id(unique_id)
    amenity = db.session.get(AmenityFeature, amenity_id)
    
    if not location:
        print(f"Error: Location with unique ID '{unique_id}' not found!")
        return False
    
    if not amenity:
        print(f"Error: Amenity with ID {amenity_id} not found!")
        return False
    
    # Check if this assignment already exists
    existing = db.session.query(LocationAmenityAssignment).filter_by(
        location_id=location.id, 
        amenity_id=amenity_id
    ).first()
    
    if existing:
        print(f"Error: {amenity.name} is already assigned to {location.title}!")
        return False
    
    # Create the assignment
    assignment = LocationAmenityAssignment(
        location_id=location.id,
        amenity_id=amenity_id
    )
    
    try:
        db.session.add(assignment)
        db.session.commit()
        print(f"Successfully added '{amenity.name}' to '{location.title}'!")
        return True
    except Exception as e:
        print(f"Error adding amenity: {e}")
        db.session.rollback()
        return False

def remove_amenity_from_location(unique_id, amenity_id):
    """Remove an amenity from a location"""
    # Check if both exist
    location = get_location_by_unique_id(unique_id)
    amenity = db.session.get(AmenityFeature, amenity_id)
    
    if not location:
        print(f"Error: Location with unique ID '{unique_id}' not found!")
        return False
    
    if not amenity:
        print(f"Error: Amenity with ID {amenity_id} not found!")
        return False
    
    # Find the assignment
    assignment = db.session.query(LocationAmenityAssignment).filter_by(
        location_id=location.id, 
        amenity_id=amenity_id
    ).first()
    
    if not assignment:
        print(f"Error: {amenity.name} is not assigned to {location.title}!")
        return False
    
    try:
        db.session.delete(assignment)
        db.session.commit()
        print(f"Successfully removed '{amenity.name}' from '{location.title}'!")
        return True
    except Exception as e:
        print(f"Error removing amenity: {e}")
        db.session.rollback()
        return False

def edit_amenity(amenity_id):
    """Edit an amenity's name and description"""
    amenity = db.session.get(AmenityFeature, amenity_id)
    
    if not amenity:
        print(f"Error: Amenity with ID {amenity_id} not found!")
        return False
    
    print(f"\n=== Editing Amenity: {amenity.name} ===")
    print(f"Current name: {amenity.name}")
    print(f"Current description: {amenity.description or 'None'}")
    
    # Get new values
    new_name = input("Enter new name (or press Enter to keep current): ").strip()
    new_description = input("Enter new description (or press Enter to keep current): ").strip()
    
    # Update only if new values were provided
    if new_name:
        amenity.name = new_name
    if new_description:
        amenity.description = new_description
    
    try:
        db.session.commit()
        print(f"Successfully updated amenity ID {amenity_id}!")
        print(f"New name: {amenity.name}")
        print(f"New description: {amenity.description or 'None'}")
        return True
    except Exception as e:
        print(f"Error updating amenity: {e}")
        db.session.rollback()
        return False

def delete_amenity_completely(amenity_id):
    """Delete an amenity completely from the system"""
    amenity = db.session.get(AmenityFeature, amenity_id)
    
    if not amenity:
        print(f"Error: Amenity with ID {amenity_id} not found!")
        return False
    
    # Check if this amenity is assigned to any locations
    assignments = db.session.query(LocationAmenityAssignment).filter_by(amenity_id=amenity_id).all()
    
    if assignments:
        print(f"Warning: This amenity is assigned to {len(assignments)} location(s).")
        print("Deleting it will remove all these assignments.")
        confirm = input("Are you sure you want to continue? (yes/no): ").strip().lower()
        
        if confirm != 'yes':
            print("Deletion cancelled.")
            return False
    
    try:
        # Delete all assignments first
        for assignment in assignments:
            db.session.delete(assignment)
        
        # Delete the amenity
        db.session.delete(amenity)
        db.session.commit()
        
        print(f"Successfully deleted amenity '{amenity.name}' and all its assignments!")
        return True
    except Exception as e:
        print(f"Error deleting amenity: {e}")
        db.session.rollback()
        return False

def create_new_amenity(name, description=None):
    """Create a new amenity feature"""
    # Check if it already exists
    existing = db.session.query(AmenityFeature).filter_by(name=name).first()
    if existing:
        print(f"Amenity '{name}' already exists with ID {existing.id}")
        return existing
    
    # Create new amenity
    amenity = AmenityFeature(name=name, description=description)
    
    try:
        db.session.add(amenity)
        db.session.commit()
        print(f"Successfully created new amenity: '{name}' with ID {amenity.id}")
        return amenity
    except Exception as e:
        print(f"Error creating amenity: {e}")
        db.session.rollback()
        return None

def interactive_mode():
    """Run the script in interactive mode"""
    print("=== Mapping Gay Guides - Amenity Management ===")
    print("Note: Use unique IDs (e.g., d-1998-01297) for locations, database IDs for amenities")
    
    while True:
        print("\nOptions:")
        print("1. List all locations")
        print("2. List all amenities")
        print("3. View amenities for a specific location")
        print("4. Add existing amenity to a location")
        print("5. Create new amenity")
        print("6. Remove amenity from a location")
        print("7. Edit amenity details")
        print("8. Delete amenity completely")
        print("9. Search amenities by name")
        print("10. Exit")
        
        choice = input("\nEnter your choice (1-10): ").strip()
        
        if choice == '1':
            list_all_locations()
        
        elif choice == '2':
            list_all_amenities()
        
        elif choice == '3':
            unique_id = input("Enter location unique ID (e.g., d-1998-01297): ").strip()
            if unique_id:
                list_location_amenities(unique_id)
            else:
                print("Unique ID cannot be empty!")
        
        elif choice == '4':
            unique_id = input("Enter location unique ID (e.g., d-1998-01297): ").strip()
            if unique_id:
                try:
                    amenity_id = int(input("Enter amenity ID: "))
                    add_amenity_to_location(unique_id, amenity_id)
                except ValueError:
                    print("Please enter a valid amenity ID number!")
            else:
                print("Unique ID cannot be empty!")
        
        elif choice == '5':
            name = input("Enter amenity name: ").strip()
            if name:
                description = input("Enter description (optional): ").strip() or None
                create_new_amenity(name, description)
            else:
                print("Amenity name cannot be empty!")
        
        elif choice == '6':
            unique_id = input("Enter location unique ID (e.g., d-1998-01297): ").strip()
            if unique_id:
                try:
                    amenity_id = int(input("Enter amenity ID: "))
                    remove_amenity_from_location(unique_id, amenity_id)
                except ValueError:
                    print("Please enter a valid amenity ID number!")
            else:
                print("Unique ID cannot be empty!")
        
        elif choice == '7':
            try:
                amenity_id = int(input("Enter amenity ID: "))
                edit_amenity(amenity_id)
            except ValueError:
                print("Please enter a valid number!")
        
        elif choice == '8':
            try:
                amenity_id = int(input("Enter amenity ID: "))
                delete_amenity_completely(amenity_id)
            except ValueError:
                print("Please enter a valid number!")
        
        elif choice == '9':
            search_term = input("Enter search term: ").strip()
            if search_term:
                search_amenities_by_name(search_term)
            else:
                print("Search term cannot be empty!")
        
        elif choice == '10':
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Please enter 1-10.")

def main():
    """Main function"""
    with app.app_context():
        # Check if database exists
        try:
            # Test database connection
            from sqlalchemy import text
            db.session.execute(text('SELECT 1'))
            print("Database connection successful!")
        except Exception as e:
            print(f"Database connection failed: {e}")
            print("Make sure the database exists and is accessible.")
            return
        
        # Check if we have command line arguments
        if len(sys.argv) > 1:
            if sys.argv[1] == '--help':
                print("Usage:")
                print("  python add_amenity.py                    # Interactive mode")
                print("  python add_amenity.py --help            # Show this help")
                return
        else:
            # Run interactive mode
            interactive_mode()

if __name__ == '__main__':
    main()
