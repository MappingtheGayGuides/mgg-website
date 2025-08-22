from flask import Blueprint, jsonify, request
import sqlite3
import os

bp = Blueprint('api', __name__)

@bp.route('/locations')
def get_locations():
    """Get all locations for the map with their types and amenities"""
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'mgg.db')
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row  # This enables column access by name
        cursor = conn.cursor()
        
        # Get all locations
        cursor.execute("""
            SELECT id, unique_id, title, description, street_address, city, state, year, 
                   notes, full_address, latitude, longitude, geo_address, unclear_address, 
                   status, unique_location_id
            FROM locations
        """)
        locations = cursor.fetchall()
        
        location_data = []
        for location in locations:
            loc_dict = dict(location)
            
            # Get types for this location
            cursor.execute("""
                SELECT lt.name 
                FROM location_type_assignments lta
                JOIN location_types lt ON lta.type_id = lt.id
                WHERE lta.location_id = ?
            """, (location['id'],))
            types = [row['name'] for row in cursor.fetchall()]
            loc_dict['types'] = types
            
            # Get amenities for this location
            cursor.execute("""
                SELECT af.name 
                FROM location_amenity_assignments laa
                JOIN amenity_features af ON laa.amenity_id = af.id
                WHERE laa.location_id = ?
            """, (location['id'],))
            amenities = [row['name'] for row in cursor.fetchall()]
            loc_dict['amenities'] = amenities
            
            location_data.append(loc_dict)
        
        conn.close()
        return jsonify(location_data)
        
    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({'error': str(e)}), 500

@bp.route('/locations/<int:location_id>')
def get_location(location_id):
    """Get a specific location"""
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'mgg.db')
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, unique_id, title, description, street_address, city, state, year, 
                   notes, full_address, latitude, longitude, geo_address, unclear_address, 
                   status, unique_location_id
            FROM locations WHERE id = ?
        """, (location_id,))
        
        location = cursor.fetchone()
        if not location:
            return jsonify({'error': 'Location not found'}), 404
            
        conn.close()
        return jsonify(dict(location))
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/unique-locations')
def get_unique_locations():
    """Get all unique locations for the map (no duplicates)"""
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'mgg.db')
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM unique_locations")
        unique_locations = cursor.fetchall()
        
        conn.close()
        return jsonify([dict(loc) for loc in unique_locations])
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/unique-locations/<int:location_id>')
def get_unique_location(location_id):
    """Get a specific unique location"""
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'mgg.db')
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM unique_locations WHERE id = ?", (location_id,))
        unique_location = cursor.fetchone()
        
        if not unique_location:
            return jsonify({'error': 'Unique location not found'}), 404
            
        conn.close()
        return jsonify(dict(unique_location))
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/location-types')
def get_location_types():
    """Get all location types"""
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'mgg.db')
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM location_types ORDER BY name")
        types = cursor.fetchall()
        
        conn.close()
        return jsonify([dict(type_obj) for type_obj in types])
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/amenity-features')
def get_amenity_features():
    """Get all amenity features"""
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'mgg.db')
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM amenity_features ORDER BY name")
        features = cursor.fetchall()
        
        conn.close()
        return jsonify([dict(feature) for feature in features])
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


