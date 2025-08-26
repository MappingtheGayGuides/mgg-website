#!/usr/bin/env python3
"""
Script to edit location details in the Mapping Gay Guides database
Usage: python edit_locations.py
"""

import sys
from pathlib import Path

# Add the current directory to the path so we can import our Flask app
sys.path.append(str(Path(__file__).parent))

from app import app, db
from models import Location, UniqueLocation, LocationType, AmenityFeature, LocationTypeAssignment, LocationAmenityAssignment

def list_all_locations():
    """List all locations with their unique IDs and basic info"""
    locations = db.session.query(Location).all()
    print("\n=== Available Locations ===")
    for loc in locations:
        print(f"Unique ID: {loc.unique_id} | {loc.title}")
        print(f"    Address: {loc.street_address or 'N/A'}, {loc.city or 'N/A'}, {loc.state or 'N/A'}")
        print(f"    Year: {loc.year or 'N/A'} | Status: {loc.status or 'N/A'}")
        print(f"    Database ID: {loc.id}")
        print()
    return locations

def search_locations_by_name(search_term):
    """Search for locations by title (partial match)"""
    locations = db.session.query(Location).filter(
        Location.title.ilike(f'%{search_term}%')
    ).all()
    
    if not locations:
        print(f"No locations found matching '{search_term}'")
        return []
    
    print(f"\n=== Locations matching '{search_term}' ===")
    for loc in locations:
        print(f"Unique ID: {loc.unique_id} | {loc.title}")
        print(f"    Address: {loc.street_address or 'N/A'}, {loc.city or 'N/A'}, {loc.state or 'N/A'}")
        print(f"    Year: {loc.year or 'N/A'}")
        print()
    
    return locations

def search_locations_by_city(city_name):
    """Search for locations by city"""
    locations = db.session.query(Location).filter(
        Location.city.ilike(f'%{city_name}%')
    ).all()
    
    if not locations:
        print(f"No locations found in '{city_name}'")
        return []
    
    print(f"\n=== Locations in '{city_name}' ===")
    for loc in locations:
        print(f"Unique ID: {loc.unique_id} | {loc.title}")
        print(f"    Address: {loc.street_address or 'N/A'}")
        print(f"    Year: {loc.year or 'N/A'} | Status: {loc.status or 'N/A'}")
        print()
    
    return locations

def get_location_by_unique_id(unique_id):
    """Get a location by its unique ID (e.g., d-1998-01297)"""
    location = db.session.query(Location).filter_by(unique_id=unique_id).first()
    return location

def view_location_details(unique_id):
    """Display detailed information about a specific location"""
    location = get_location_by_unique_id(unique_id)
    if not location:
        print(f"Location with unique ID '{unique_id}' not found!")
        return None
    
    print(f"\n=== Location Details: {location.title} ===")
    print(f"ID: {location.id}")
    print(f"Unique ID: {location.unique_id}")
    print(f"Title: {location.title}")
    print(f"Description: {location.description or 'None'}")
    print(f"Street Address: {location.street_address or 'None'}")
    print(f"City: {location.city or 'None'}")
    print(f"State: {location.state or 'None'}")
    print(f"Year: {location.year or 'None'}")
    print(f"Notes: {location.notes or 'None'}")
    print(f"Full Address: {location.full_address or 'None'}")
    print(f"Latitude: {location.latitude or 'None'}")
    print(f"Longitude: {location.longitude or 'None'}")
    print(f"Geo Address: {location.geo_address or 'None'}")
    print(f"Unclear Address: {location.unclear_address or 'None'}")
    print(f"Status: {location.status or 'None'}")
    print(f"Unique Location ID: {location.unique_location_id or 'None'}")
    
    # Show associated types
    if location.types:
        print(f"\nLocation Types:")
        for loc_type in location.types:
            print(f"  • {loc_type.name}")
    else:
        print(f"\nLocation Types: None")
    
    # Show associated amenities
    if location.amenities:
        print(f"\nAmenities:")
        for amenity in location.amenities:
            print(f"  • {amenity.name}")
    else:
        print(f"\nAmenities: None")
    
    return location

def edit_location_basic_info(unique_id):
    """Edit basic location information"""
    location = get_location_by_unique_id(unique_id)
    if not location:
        print(f"Location with unique ID '{unique_id}' not found!")
        return False
    
    print(f"\n=== Editing Location: {location.title} ===")
    print("(Press Enter to keep current value)")
    
    # Get new values
    new_title = input(f"Title [{location.title}]: ").strip()
    new_description = input(f"Description [{location.description or 'None'}]: ").strip()
    new_street_address = input(f"Street Address [{location.street_address or 'None'}]: ").strip()
    new_city = input(f"City [{location.city or 'None'}]: ").strip()
    new_state = input(f"State [{location.state or 'None'}]: ").strip()
    new_year = input(f"Year [{location.year or 'None'}]: ").strip()
    new_notes = input(f"Notes [{location.notes or 'None'}]: ").strip()
    new_status = input(f"Status [{location.status or 'None'}]: ").strip()
    
    # Update only if new values were provided
    if new_title:
        location.title = new_title
    if new_description:
        location.description = new_description
    if new_street_address:
        location.street_address = new_street_address
    if new_city:
        location.city = new_city
    if new_state:
        location.state = new_state
    if new_year:
        try:
            location.year = int(new_year)
        except ValueError:
            print("Warning: Year must be a number. Keeping current value.")
    if new_notes:
        location.notes = new_notes
    if new_status:
        location.status = new_status
    
    try:
        db.session.commit()
        print(f"Successfully updated location '{unique_id}'!")
        return True
    except Exception as e:
        print(f"Error updating location: {e}")
        db.session.rollback()
        return False

def edit_location_coordinates(unique_id):
    """Edit location coordinates"""
    location = get_location_by_unique_id(unique_id)
    if not location:
        print(f"Location with unique ID '{unique_id}' not found!")
        return False
    
    print(f"\n=== Editing Coordinates for: {location.title} ===")
    print(f"Current coordinates: Lat: {location.latitude or 'None'}, Lon: {location.longitude or 'None'}")
    print("(Press Enter to keep current value)")
    
    new_lat = input(f"Latitude [{location.latitude or 'None'}]: ").strip()
    new_lon = input(f"Longitude [{location.longitude or 'None'}]: ").strip()
    
    # Update only if new values were provided
    if new_lat:
        try:
            location.latitude = float(new_lat)
        except ValueError:
            print("Warning: Latitude must be a number. Keeping current value.")
    
    if new_lon:
        try:
            location.longitude = float(new_lon)
        except ValueError:
            print("Warning: Longitude must be a number. Keeping current value.")
    
    try:
        db.session.commit()
        print(f"Successfully updated coordinates for location '{unique_id}'!")
        return True
    except Exception as e:
        print(f"Error updating coordinates: {e}")
        db.session.rollback()
        return False

def add_location_type(unique_id, type_name):
    """Add a location type to a location"""
    location = get_location_by_unique_id(unique_id)
    if not location:
        print(f"Error: Location with unique ID '{unique_id}' not found!")
        return False
    
    # Get or create the location type
    loc_type = db.session.query(LocationType).filter_by(name=type_name).first()
    if not loc_type:
        # Create new type
        loc_type = LocationType(name=type_name)
        db.session.add(loc_type)
        db.session.flush()  # Get the ID
        print(f"Created new location type: '{type_name}'")
    
    # Check if this assignment already exists
    existing = db.session.query(LocationTypeAssignment).filter_by(
        location_id=location_id, 
        type_id=loc_type.id
    ).first()
    
    if existing:
        print(f"'{type_name}' is already assigned to '{location.title}'")
        return True
    
    # Create the assignment
    assignment = LocationTypeAssignment(
        location_id=location_id,
        type_id=loc_type.id
    )
    
    try:
        db.session.add(assignment)
        db.session.commit()
        print(f"Successfully added '{type_name}' to '{location.title}'!")
        return True
    except Exception as e:
        print(f"Error adding location type: {e}")
        db.session.rollback()
        return False

def remove_location_type(unique_id, type_name):
    """Remove a location type from a location"""
    location = get_location_by_unique_id(unique_id)
    if not location:
        print(f"Error: Location with unique ID '{unique_id}' not found!")
        return False
    
    # Find the type
    loc_type = db.session.query(LocationType).filter_by(name=type_name).first()
    if not loc_type:
        print(f"Error: Location type '{type_name}' not found!")
        return False
    
    # Find the assignment
    assignment = db.session.query(LocationTypeAssignment).filter_by(
        location_id=location_id, 
        type_id=loc_type.id
    ).first()
    
    if not assignment:
        print(f"Error: '{type_name}' is not assigned to '{location.title}'!")
        return False
    
    try:
        db.session.delete(assignment)
        db.session.commit()
        print(f"Successfully removed '{type_name}' from '{location.title}'!")
        return True
    except Exception as e:
        print(f"Error removing location type: {e}")
        db.session.rollback()
        return False

def list_all_location_types():
    """List all available location types"""
    types = db.session.query(LocationType).all()
    print("\n=== Available Location Types ===")
    for loc_type in types:
        print(f"ID: {loc_type.id} | {loc_type.name}")
        if loc_type.description:
            print(f"    Description: {loc_type.description}")
    return types

def create_new_location_type(name, description=None):
    """Create a new location type"""
    # Check if it already exists
    existing = db.session.query(LocationType).filter_by(name=name).first()
    if existing:
        print(f"Location type '{name}' already exists with ID {existing.id}")
        return existing
    
    # Create new type
    loc_type = LocationType(name=name, description=description)
    
    try:
        db.session.add(loc_type)
        db.session.commit()
        print(f"Successfully created new location type: '{name}' with ID {loc_type.id}")
        return loc_type
    except Exception as e:
        print(f"Error creating location type: {e}")
        db.session.rollback()
        return None

def interactive_mode():
    """Run the script in interactive mode"""
    print("=== Mapping Gay Guides - Location Management ===")
    print("Note: Use unique IDs (e.g., d-1998-01297) instead of database IDs")
    
    while True:
        print("\nOptions:")
        print("1. List all locations")
        print("2. Search locations by name")
        print("3. Search locations by city")
        print("4. View detailed location information")
        print("5. Edit basic location information")
        print("6. Edit location coordinates")
        print("7. Add location type to a location")
        print("8. Remove location type from a location")
        print("9. List all location types")
        print("10. Create new location type")
        print("11. Exit")
        
        choice = input("\nEnter your choice (1-11): ").strip()
        
        if choice == '1':
            list_all_locations()
        
        elif choice == '2':
            search_term = input("Enter search term: ").strip()
            if search_term:
                search_locations_by_name(search_term)
            else:
                print("Search term cannot be empty!")
        
        elif choice == '3':
            city_name = input("Enter city name: ").strip()
            if city_name:
                search_locations_by_city(city_name)
            else:
                print("City name cannot be empty!")
        
        elif choice == '4':
            unique_id = input("Enter location unique ID (e.g., d-1998-01297): ").strip()
            if unique_id:
                view_location_details(unique_id)
            else:
                print("Unique ID cannot be empty!")
        
        elif choice == '5':
            unique_id = input("Enter location unique ID (e.g., d-1998-01297): ").strip()
            if unique_id:
                edit_location_basic_info(unique_id)
            else:
                print("Unique ID cannot be empty!")
        
        elif choice == '6':
            unique_id = input("Enter location unique ID (e.g., d-1998-01297): ").strip()
            if unique_id:
                edit_location_coordinates(unique_id)
            else:
                print("Unique ID cannot be empty!")
        
        elif choice == '7':
            unique_id = input("Enter location unique ID (e.g., d-1998-01297): ").strip()
            if unique_id:
                type_name = input("Enter location type name: ").strip()
                if type_name:
                    add_location_type(unique_id, type_name)
                else:
                    print("Location type name cannot be empty!")
            else:
                print("Unique ID cannot be empty!")
        
        elif choice == '8':
            unique_id = input("Enter location unique ID (e.g., d-1998-01297): ").strip()
            if unique_id:
                type_name = input("Enter location type name: ").strip()
                if type_name:
                    remove_location_type(unique_id, type_name)
                else:
                    print("Location type name cannot be empty!")
            else:
                print("Unique ID cannot be empty!")
        
        elif choice == '9':
            list_all_location_types()
        
        elif choice == '10':
            name = input("Enter location type name: ").strip()
            if name:
                description = input("Enter description (optional): ").strip() or None
                create_new_location_type(name, description)
            else:
                print("Location type name cannot be empty!")
        
        elif choice == '11':
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Please enter 1-11.")

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
                print("  python edit_locations.py                    # Interactive mode")
                print("  python edit_locations.py --help            # Show this help")
                return
        else:
            # Run interactive mode
            interactive_mode()

if __name__ == '__main__':
    main()
