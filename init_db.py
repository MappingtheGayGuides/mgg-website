#!/usr/bin/env python3
"""
Database initialization script for Mapping the Gay Guides
Creates the database and adds sample data if it doesn't exist
"""

import os
from app import app, db
from models import Location, Article
from datetime import date

def init_database():
    """Initialize the database with tables and sample data"""
    
    # Check if database file exists
    db_path = 'mgg.db'
    db_exists = os.path.exists(db_path)
    
    print(f"Database file exists: {db_exists}")
    
    with app.app_context():
        # Create all tables
        print("Creating database tables...")
        db.create_all()
        print("✓ Database tables created")
        
        # Only add sample data if database is new
        if not db_exists:
            print("Adding sample data...")
            add_sample_data()
            print("✓ Sample data added")
        else:
            print("Database already exists, skipping sample data")
        
        print(f"\nDatabase initialized successfully!")
        print(f"Database file: {os.path.abspath(db_path)}")

def add_sample_data():
    """Add sample locations and articles to the database"""
    
    # Sample locations from gay guides
    sample_locations = [
        {
            'name': 'Gold Room',
            'address': '123 Main St',
            'city': 'San Francisco',
            'state': 'CA',
            'zip_code': '94102',
            'latitude': 37.7749,
            'longitude': -122.4194,
            'category': 'bar',
            'year_listed': 1976,
            'guide_edition': 'Damron 1976',
            'description': 'Historic gay bar in the Castro district',
            'notes': 'One of the oldest continuously operating gay bars in San Francisco'
        },
        {
            'name': 'Stonewall Inn',
            'address': '53 Christopher St',
            'city': 'New York',
            'state': 'NY',
            'zip_code': '10014',
            'latitude': 40.7338,
            'longitude': -74.0027,
            'category': 'bar',
            'year_listed': 1969,
            'guide_edition': 'Damron 1969',
            'description': 'Historic gay bar, site of the Stonewall riots',
            'notes': 'National Historic Landmark and birthplace of the modern LGBTQ+ rights movement'
        },
        {
            'name': 'Upstairs Lounge',
            'address': '604 Iberville St',
            'city': 'New Orleans',
            'state': 'LA',
            'zip_code': '70130',
            'latitude': 29.9511,
            'longitude': -90.0715,
            'category': 'bar',
            'year_listed': 1973,
            'guide_edition': 'Damron 1973',
            'description': 'Gay bar and community gathering space',
            'notes': 'Site of tragic 1973 fire that killed 32 people'
        },
        {
            'name': 'Gay Community Center',
            'address': '208 W 13th St',
            'city': 'New York',
            'state': 'NY',
            'zip_code': '10011',
            'latitude': 40.7379,
            'longitude': -74.0018,
            'category': 'community',
            'year_listed': 1983,
            'guide_edition': 'Damron 1983',
            'description': 'Community center providing services and support',
            'notes': 'Important community resource for LGBTQ+ New Yorkers'
        }
    ]
    
    # Add locations
    for loc_data in sample_locations:
        location = Location(**loc_data)
        db.session.add(location)
    
    # Sample articles
    sample_articles = [
        {
            'title': 'Mapping Queer Spaces: A Digital History Approach',
            'slug': 'mapping-queer-spaces-digital-history',
            'content': 'This article explores the methodology behind our digital mapping project...',
            'excerpt': 'An introduction to our digital humanities approach to mapping LGBTQ+ history.',
            'author': 'Amanda Regan',
            'published_date': date(2024, 1, 15),
            'is_published': True
        },
        {
            'title': 'The Evolution of Gay Travel Guides',
            'slug': 'evolution-gay-travel-guides',
            'content': 'From the early Damron guides to modern digital platforms...',
            'excerpt': 'How travel guides have documented and shaped LGBTQ+ spaces over time.',
            'author': 'Research Team',
            'published_date': date(2024, 1, 20),
            'is_published': True
        }
    ]
    
    # Add articles
    for article_data in sample_articles:
        article = Article(**article_data)
        db.session.add(article)
    
    # Commit all changes
    db.session.commit()
    print(f"  - Added {len(sample_locations)} sample locations")
    print(f"  - Added {len(sample_articles)} sample articles")

if __name__ == '__main__':
    print("Initializing Mapping the Gay Guides Database...")
    print("=" * 50)
    init_database()
    print("=" * 50)
    print("You can now run: python3 app.py")
