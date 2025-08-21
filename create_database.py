#!/usr/bin/env python3
"""
Database creation script for Mapping the Gay Guides
Creates the database tables manually with the correct schema
"""

import sqlite3
import os

def create_database():
    """Create the database and all tables"""
    
    # Remove existing database if it exists
    if os.path.exists('mgg.db'):
        os.remove('mgg.db')
        print("Removed existing database")
    
    # Create new database
    conn = sqlite3.connect('mgg.db')
    cursor = conn.cursor()
    
    print("Creating database tables...")
    
    # Create unique_locations table
    cursor.execute("""
        CREATE TABLE unique_locations (
            id INTEGER PRIMARY KEY,
            latitude FLOAT NOT NULL,
            longitude FLOAT NOT NULL,
            city VARCHAR(100),
            state VARCHAR(50),
            address_precision VARCHAR(50) DEFAULT 'general',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("✓ Created unique_locations table")
    
    # Create location_types table
    cursor.execute("""
        CREATE TABLE location_types (
            id INTEGER PRIMARY KEY,
            name VARCHAR(500) UNIQUE NOT NULL,
            description TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("✓ Created location_types table")
    
    # Create amenity_features table
    cursor.execute("""
        CREATE TABLE amenity_features (
            id INTEGER PRIMARY KEY,
            name VARCHAR(500) UNIQUE NOT NULL,
            description TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("✓ Created amenity_features table")
    
    # Create locations table
    cursor.execute("""
        CREATE TABLE locations (
            id INTEGER PRIMARY KEY,
            unique_id VARCHAR(100) UNIQUE NOT NULL,
            title VARCHAR(500),
            description TEXT,
            street_address VARCHAR(500),
            city VARCHAR(100),
            state VARCHAR(50),
            year INTEGER,
            notes TEXT,
            full_address VARCHAR(500),
            latitude FLOAT,
            longitude FLOAT,
            geo_address VARCHAR(500),
            unclear_address VARCHAR(10),
            status VARCHAR(200),
            unique_location_id INTEGER,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(unique_location_id) REFERENCES unique_locations(id)
        )
    """)
    print("✓ Created locations table")
    
    # Create location_type_assignments table
    cursor.execute("""
        CREATE TABLE location_type_assignments (
            id INTEGER PRIMARY KEY,
            location_id INTEGER NOT NULL,
            type_id INTEGER NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(location_id) REFERENCES locations(id),
            FOREIGN KEY(type_id) REFERENCES location_types(id),
            UNIQUE(location_id, type_id)
        )
    """)
    print("✓ Created location_type_assignments table")
    
    # Create location_amenity_assignments table
    cursor.execute("""
        CREATE TABLE location_amenity_assignments (
            id INTEGER PRIMARY KEY,
            location_id INTEGER NOT NULL,
            amenity_id INTEGER NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(location_id) REFERENCES locations(id),
            FOREIGN KEY(amenity_id) REFERENCES amenity_features(id),
            UNIQUE(location_id, amenity_id)
        )
    """)
    print("✓ Created location_amenity_assignments table")
    
    # Commit and close
    conn.commit()
    conn.close()
    
    print("\n✅ Database created successfully!")
    print(f"Database file: {os.path.abspath('mgg.db')}")

if __name__ == "__main__":
    create_database()
