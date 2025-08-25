#!/usr/bin/env python3
"""
Script to create the split_logging table for tracking Smart Split operations
"""

import sqlite3
import os

def create_split_logging_table():
    """Create the split_logging table to track all Smart Split operations"""
    
    # Connect to the database
    db_path = 'mgg.db'
    if not os.path.exists(db_path):
        print(f"Database {db_path} not found!")
        return False
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Create the split_logging table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS split_logging (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                operation_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                source_amenity_id INTEGER,
                source_amenity_name TEXT,
                operation_type TEXT CHECK(operation_type IN ('split', 'merge', 'rename')),
                target_amenities TEXT, -- JSON string of target amenity IDs and names
                locations_processed INTEGER,
                locations_reassigned INTEGER,
                locations_unassigned INTEGER,
                source_removed BOOLEAN,
                user_notes TEXT,
                operation_status TEXT CHECK(operation_status IN ('success', 'partial_success', 'failed')),
                error_message TEXT,
                execution_time_ms INTEGER,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create the split_location_details table for detailed tracking of each location change
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS split_location_details (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                split_log_id INTEGER,
                location_id INTEGER,
                location_title TEXT,
                location_city TEXT,
                location_state TEXT,
                location_year INTEGER,
                old_amenity_id INTEGER,
                old_amenity_name TEXT,
                new_amenity_id INTEGER,
                new_amenity_name TEXT,
                reassignment_type TEXT CHECK(reassignment_type IN ('manual', 'auto', 'year_based')),
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (split_log_id) REFERENCES split_logging (id),
                FOREIGN KEY (location_id) REFERENCES locations (id),
                FOREIGN KEY (old_amenity_id) REFERENCES amenity_features (id),
                FOREIGN KEY (new_amenity_id) REFERENCES amenity_features (id)
            )
        """)
        
        # Create indexes for better performance
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_split_logging_timestamp ON split_logging(operation_timestamp)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_split_logging_source ON split_logging(source_amenity_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_split_location_details_split_id ON split_location_details(split_log_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_split_location_details_location ON split_location_details(location_id)")
        
        conn.commit()
        print("✅ Split logging tables created successfully!")
        
        # Show table structure
        cursor.execute("PRAGMA table_info(split_logging)")
        columns = cursor.fetchall()
        print("\n📋 split_logging table structure:")
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")
        
        cursor.execute("PRAGMA table_info(split_location_details)")
        columns = cursor.fetchall()
        print("\n📋 split_location_details table structure:")
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        conn.rollback()
        return False
        
    finally:
        conn.close()

if __name__ == "__main__":
    print("🔧 Creating Smart Split logging tables...")
    success = create_split_logging_table()
    if success:
        print("\n🎉 Setup complete! The Smart Split system now has comprehensive logging.")
    else:
        print("\n💥 Setup failed. Please check the error messages above.") 