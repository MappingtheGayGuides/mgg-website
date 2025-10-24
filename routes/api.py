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

@bp.route('/amenity-cleanup/merge', methods=['POST'])
def merge_amenities():
    """Merge multiple amenities into one"""
    try:
        data = request.get_json()
        keep_id = data.get('keep_id')
        merge_ids = data.get('merge_ids', [])
        
        if not keep_id or not merge_ids:
            return jsonify({'error': 'Missing required parameters'}), 400
        
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'mgg.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Update all assignments to use the kept amenity
        for merge_id in merge_ids:
            cursor.execute("""
                UPDATE location_amenity_assignments 
                SET amenity_id = ? 
                WHERE amenity_id = ?
            """, (keep_id, merge_id))
            
            # Delete the merged amenity
            cursor.execute("DELETE FROM amenity_features WHERE id = ?", (merge_id,))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': f'Merged {len(merge_ids)} amenities'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/amenity-cleanup/rename', methods=['POST'])
def rename_amenity():
    """Rename an amenity"""
    try:
        data = request.get_json()
        amenity_id = data.get('amenity_id')
        new_name = data.get('new_name')
        
        print(f"Rename request: amenity_id={amenity_id}, new_name={new_name}")
        
        if not amenity_id or not new_name:
            return jsonify({'error': 'Missing required parameters'}), 400
        
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'mgg.db')
        print(f"Database path: {db_path}")
        print(f"Database exists: {os.path.exists(db_path)}")
        
        if not os.path.exists(db_path):
            return jsonify({'error': 'Database not found'}), 500
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if the amenity exists
        cursor.execute("SELECT id, name FROM amenity_features WHERE id = ?", (amenity_id,))
        amenity = cursor.fetchone()
        if not amenity:
            conn.close()
            return jsonify({'error': 'Amenity not found'}), 404
        
        print(f"Found amenity: {amenity}")
        
        # Check if the new name already exists
        cursor.execute("SELECT id FROM amenity_features WHERE name = ? AND id != ?", (new_name, amenity_id))
        if cursor.fetchone():
            conn.close()
            return jsonify({'error': 'An amenity with that name already exists'}), 400
        
        # Update the amenity name
        cursor.execute("UPDATE amenity_features SET name = ? WHERE id = ?", (new_name, amenity_id))
        
        conn.commit()
        conn.close()
        
        print(f"Amenity {amenity_id} renamed from '{amenity[1]}' to '{new_name}'")
        return jsonify({'success': True, 'message': 'Amenity renamed successfully'})
        
    except Exception as e:
        print(f"Error in rename_amenity: {e}")
        return jsonify({'error': str(e)}), 500

@bp.route('/amenity-cleanup/usage/<int:amenity_id>')
def get_amenity_usage(amenity_id):
    """Get all locations that use a specific amenity"""
    try:
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'mgg.db')
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT l.id, l.title, l.city, l.state, l.year
            FROM locations l
            JOIN location_amenity_assignments laa ON l.id = laa.location_id
            WHERE laa.amenity_id = ?
            ORDER BY l.title
        """, (amenity_id,))
        
        locations = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return jsonify(locations)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/amenity-cleanup/smart-merge', methods=['POST'])
def smart_merge_amenities():
    """Smart merge amenities with similar names"""
    try:
        data = request.get_json()
        target_name = data.get('target_name')
        source_ids = data.get('source_ids', [])
        
        if not target_name or not source_ids:
            return jsonify({'error': 'Missing required parameters'}), 400
        
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'mgg.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # First, create the target amenity if it doesn't exist
        cursor.execute("SELECT id FROM amenity_features WHERE name = ?", (target_name,))
        target_amenity = cursor.fetchone()
        
        if target_amenity:
            target_id = target_amenity[0]
        else:
            # Create new amenity with the target name
            cursor.execute("INSERT INTO amenity_features (name) VALUES (?)", (target_name,))
            target_id = cursor.lastrowid
        
        # Get all location assignments from source amenities
        all_assignments = set()
        for source_id in source_ids:
            cursor.execute("""
                SELECT location_id FROM location_amenity_assignments 
                WHERE amenity_id = ?
            """, (source_id,))
            assignments = cursor.fetchall()
            all_assignments.update([row[0] for row in assignments])
        
        # Assign all locations to the target amenity (avoiding duplicates)
        for location_id in all_assignments:
            cursor.execute("""
                INSERT OR IGNORE INTO location_amenity_assignments (location_id, amenity_id)
                VALUES (?, ?)
            """, (location_id, target_id))
        
        # Remove all source amenities
        for source_id in source_ids:
            cursor.execute("DELETE FROM location_amenity_assignments WHERE amenity_id = ?", (source_id,))
            cursor.execute("DELETE FROM amenity_features WHERE id = ?", (source_id,))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True, 
            'message': f'Successfully merged {len(source_ids)} amenities into "{target_name}"',
            'target_id': target_id,
            'locations_updated': len(all_assignments)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/amenity-cleanup/find-similar')
def find_similar_amenities():
    """Find amenities with similar names for potential merging"""
    try:
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'mgg.db')
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Get all amenities with their usage counts
        cursor.execute("""
            SELECT af.id, af.name, COUNT(laa.location_id) as usage_count
            FROM amenity_features af
            LEFT JOIN location_amenity_assignments laa ON af.id = laa.amenity_id
            GROUP BY af.id, af.name
            ORDER BY af.name
        """)
        amenities = [dict(row) for row in cursor.fetchall()]
        
        # Find potential duplicates (simple similarity check)
        similar_groups = []
        processed = set()
        
        for i, amenity1 in enumerate(amenities):
            if amenity1['id'] in processed:
                continue
                
            group = [amenity1]
            processed.add(amenity1['id'])
            
            # Check for similar names
            name1_clean = amenity1['name'].lower().strip()
            
            for j, amenity2 in enumerate(amenities[i+1:], i+1):
                if amenity2['id'] in processed:
                    continue
                    
                name2_clean = amenity2['name'].lower().strip()
                
                # Check if names are similar (you can adjust this logic)
                if (name1_clean == name2_clean or 
                    name1_clean in name2_clean or 
                    name2_clean in name1_clean or
                    name1_clean.replace('-', '').replace(' ', '') == name2_clean.replace('-', '').replace(' ', '') or
                    name1_clean.split('(')[0].strip() == name2_clean.split('(')[0].strip()):
                    
                    group.append(amenity2)
                    processed.add(amenity2['id'])
            
            if len(group) > 1:
                similar_groups.append(group)
        
        conn.close()
        return jsonify(similar_groups)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/amenity-cleanup/smart-split', methods=['POST'])
def smart_split_amenities():
    """Smart split amenities with manual location assignment and comprehensive logging"""
    import sqlite3
    import os
    import json
    import time
    
    start_time = time.time()
    
    try:
        data = request.get_json()
        source_amenity_id = data.get('source_amenity_id')
        target_mappings = data.get('target_mappings', [])
        manual_assignments = data.get('manual_assignments', [])
        user_notes = data.get('user_notes', '')
        
        if not source_amenity_id or not target_mappings:
            return jsonify({'error': 'Missing required parameters'}), 400
        
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'mgg.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get source amenity info
        cursor.execute("SELECT name FROM amenity_features WHERE id = ?", (source_amenity_id,))
        source_amenity = cursor.fetchone()
        if not source_amenity:
            conn.close()
            return jsonify({'error': 'Source amenity not found'}), 404
        
        source_name = source_amenity[0]
        
        # Get all locations using the source amenity
        cursor.execute("""
            SELECT l.id, l.year, l.title, l.city, l.state
            FROM locations l
            JOIN location_amenity_assignments laa ON l.id = laa.location_id
            WHERE laa.amenity_id = ?
            ORDER BY l.year
        """, (source_amenity_id,))
        
        source_locations = cursor.fetchall()
        
        if not source_locations:
            conn.close()
            return jsonify({'error': 'No locations found for source amenity'}), 400
        
        # Prepare target amenities info for logging
        target_amenities_info = []
        for mapping in target_mappings:
            cursor.execute("SELECT name FROM amenity_features WHERE id = ?", (mapping['target_id'],))
            target_name = cursor.fetchone()[0]
            target_amenities_info.append({
                'id': mapping['target_id'],
                'name': target_name
            })
        
        # Process manual assignments
        reassigned_count = 0
        unassigned_count = 0
        unassigned_locations = []
        location_changes = []  # Track all location changes for detailed logging
        
        # Create a map of location_id to target_id from manual assignments
        assignment_map = {assignment['location_id']: assignment['target_amenity_id'] for assignment in manual_assignments}
        
        for location in source_locations:
            location_id, year, title, city, state = location
            
            if location_id in assignment_map:
                # Use manual assignment
                target_id = assignment_map[location_id]
                target_name = next((t['name'] for t in target_amenities_info if t['id'] == target_id), 'Unknown')
                
                cursor.execute("""
                    INSERT OR IGNORE INTO location_amenity_assignments (location_id, amenity_id)
                    VALUES (?, ?)
                """, (location_id, target_id))
                reassigned_count += 1
                
                # Track this location change
                location_changes.append({
                    'location_id': location_id,
                    'title': title,
                    'city': city,
                    'state': state,
                    'year': year,
                    'old_amenity_id': source_amenity_id,
                    'old_amenity_name': source_name,
                    'new_amenity_id': target_id,
                    'new_amenity_name': target_name,
                    'reassignment_type': 'manual'
                })
            else:
                # Location was not manually assigned
                unassigned_count += 1
                unassigned_locations.append({
                    'id': location_id,
                    'title': title,
                    'city': city,
                    'state': state,
                    'year': year
                })
        
        # Remove the source amenity assignments
        cursor.execute("DELETE FROM location_amenity_assignments WHERE amenity_id = ?", (source_amenity_id,))
        
        # Optionally remove the source amenity if it's no longer used
        cursor.execute("SELECT COUNT(*) FROM location_amenity_assignments WHERE amenity_id = ?", (source_amenity_id,))
        if cursor.fetchone()[0] == 0:
            cursor.execute("DELETE FROM amenity_features WHERE id = ?", (source_amenity_id,))
            source_removed = True
        else:
            source_removed = False
        
        # Calculate execution time
        execution_time_ms = int((time.time() - start_time) * 1000)
        
        # Log the operation
        cursor.execute("""
            INSERT INTO split_logging (
                source_amenity_id, source_amenity_name, operation_type, target_amenities,
                locations_processed, locations_reassigned, locations_unassigned,
                source_removed, user_notes, operation_status, execution_time_ms
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            source_amenity_id, source_name, 'split', json.dumps(target_amenities_info),
            len(source_locations), reassigned_count, unassigned_count,
            source_removed, user_notes, 'success', execution_time_ms
        ))
        
        split_log_id = cursor.lastrowid
        
        # Log detailed location changes
        for change in location_changes:
            cursor.execute("""
                INSERT INTO split_location_details (
                    split_log_id, location_id, location_title, location_city, location_state, location_year,
                    old_amenity_id, old_amenity_name, new_amenity_id, new_amenity_name, reassignment_type
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                split_log_id, change['location_id'], change['title'], change['city'], change['state'], change['year'],
                change['old_amenity_id'], change['old_amenity_name'], change['new_amenity_id'], change['new_amenity_name'], change['reassignment_type']
            ))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': f'Successfully split "{source_name}" with {reassigned_count} manually assigned locations',
            'reassigned_count': reassigned_count,
            'unassigned_count': unassigned_count,
            'unassigned_locations': unassigned_locations,
            'source_removed': source_removed,
            'split_log_id': split_log_id,
            'execution_time_ms': execution_time_ms
        })
        
    except Exception as e:
        execution_time_ms = int((time.time() - start_time) * 1000)
        error_message = str(e)
        
        # Log the failed operation
        try:
            db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'mgg.db')
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO split_logging (
                    source_amenity_id, source_amenity_name, operation_type, target_amenities,
                    locations_processed, locations_reassigned, locations_unassigned,
                    source_removed, user_notes, operation_status, error_message, execution_time_ms
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                source_amenity_id if 'source_amenity_id' in locals() else None,
                source_name if 'source_name' in locals() else 'Unknown',
                'split', json.dumps(target_amenities_info if 'target_amenities_info' in locals() else []),
                0, 0, 0, False, user_notes if 'user_notes' in locals() else '', 'failed', error_message, execution_time_ms
            ))
            
            conn.commit()
            conn.close()
        except:
            pass  # Don't let logging errors interfere with the main error response
        
        return jsonify({'error': error_message}), 500

@bp.route('/amenity-cleanup/get-location-years/<int:amenity_id>')
def get_location_years_for_amenity(amenity_id):
    """Get year distribution for locations using a specific amenity"""
    try:
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'mgg.db')
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Get all locations with years for this amenity
        cursor.execute("""
            SELECT l.id, l.year, l.title, l.city, l.state
            FROM locations l
            JOIN location_amenity_assignments laa ON l.id = laa.location_id
            WHERE laa.amenity_id = ?
            ORDER BY l.year
        """, (amenity_id,))
        
        locations = [dict(row) for row in cursor.fetchall()]
        
        # Calculate year statistics
        years = [loc['year'] for loc in locations if loc['year']]
        year_stats = {
            'total_locations': len(locations),
            'locations_with_years': len(years),
            'min_year': min(years) if years else None,
            'max_year': max(years) if years else None,
            'year_distribution': {}
        }
        
        # Count locations by year
        for year in years:
            year_stats['year_distribution'][year] = year_stats['year_distribution'].get(year, 0) + 1
        
        conn.close()
        
        return jsonify({
            'locations': locations,
            'year_stats': year_stats
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/test')
def test_api():
    """Simple test endpoint to check if API is working"""
    return jsonify({'status': 'ok', 'message': 'API is working'})

@bp.route('/amenity-cleanup/split-history')
def get_split_history():
    """Get a list of all split operations with basic information"""
    import sqlite3
    import os
    import json
    
    try:
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'mgg.db')
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Get all split operations ordered by most recent first
        cursor.execute("""
            SELECT id, operation_timestamp, source_amenity_name, operation_type,
                   target_amenities, locations_processed, locations_reassigned,
                   locations_unassigned, source_removed, user_notes, operation_status,
                   execution_time_ms, created_at
            FROM split_logging
            ORDER BY operation_timestamp DESC
            LIMIT 100
        """)
        
        operations = []
        for row in cursor.fetchall():
            op = dict(row)
            # Parse target amenities JSON
            try:
                op['target_amenities'] = json.loads(op['target_amenities']) if op['target_amenities'] else []
            except:
                op['target_amenities'] = []
            operations.append(op)
        
        conn.close()
        
        return jsonify({
            'operations': operations,
            'total_count': len(operations)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/amenity-cleanup/split-details/<int:split_id>')
def get_split_details(split_id):
    """Get detailed information about a specific split operation"""
    import sqlite3
    import os
    
    try:
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'mgg.db')
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Get the main split operation
        cursor.execute("""
            SELECT * FROM split_logging WHERE id = ?
        """, (split_id,))
        
        operation = cursor.fetchone()
        if not operation:
            conn.close()
            return jsonify({'error': 'Split operation not found'}), 404
        
        operation = dict(operation)
        
        # Get detailed location changes
        cursor.execute("""
            SELECT * FROM split_location_details 
            WHERE split_log_id = ?
            ORDER BY location_title, location_city
        """, (split_id,))
        
        location_details = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        
        return jsonify({
            'operation': operation,
            'location_details': location_details
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/amenity-cleanup/split-stats')
def get_split_statistics():
    """Get overall statistics about split operations"""
    import sqlite3
    import os
    
    try:
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'mgg.db')
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Get overall statistics
        cursor.execute("""
            SELECT 
                COUNT(*) as total_operations,
                COUNT(CASE WHEN operation_status = 'success' THEN 1 END) as successful_operations,
                COUNT(CASE WHEN operation_status = 'failed' THEN 1 END) as failed_operations,
                SUM(locations_processed) as total_locations_processed,
                SUM(locations_reassigned) as total_locations_reassigned,
                SUM(locations_unassigned) as total_locations_unassigned,
                AVG(execution_time_ms) as avg_execution_time_ms,
                MIN(operation_timestamp) as first_operation,
                MAX(operation_timestamp) as last_operation
            FROM split_logging
        """)
        
        stats = dict(cursor.fetchone())
        
        # Get top source amenities by frequency
        cursor.execute("""
            SELECT source_amenity_name, COUNT(*) as operation_count
            FROM split_logging
            GROUP BY source_amenity_name
            ORDER BY operation_count DESC
            LIMIT 10
        """)
        
        top_sources = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        
        return jsonify({
            'overall_stats': stats,
            'top_source_amenities': top_sources
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/debug/database-structure')
def debug_database_structure():
    """Debug endpoint to check database structure and data"""
    import sqlite3
    import os
    
    try:
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'mgg.db')
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Check tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        # Check data counts
        cursor.execute("SELECT COUNT(*) FROM locations")
        location_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM amenity_features")
        amenity_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM location_amenity_assignments")
        assignment_count = cursor.fetchone()[0]
        
        # Check sample data
        cursor.execute("SELECT * FROM locations LIMIT 3")
        sample_locations = [dict(row) for row in cursor.fetchall()]
        
        cursor.execute("SELECT * FROM amenity_features LIMIT 3")
        sample_amenities = [dict(row) for row in cursor.fetchall()]
        
        cursor.execute("SELECT * FROM location_amenity_assignments LIMIT 3")
        sample_assignments = [dict(row) for row in cursor.fetchall()]
        
        # Check if a specific location has amenities
        if sample_locations:
            first_location_id = sample_locations[0]['id']
            cursor.execute("""
                SELECT af.name 
                FROM amenity_features af
                JOIN location_amenity_assignments laa ON af.id = laa.amenity_id
                WHERE laa.location_id = ?
            """, (first_location_id,))
            first_location_amenities = [row[0] for row in cursor.fetchall()]
        else:
            first_location_amenities = []
        
        conn.close()
        
        return jsonify({
            'tables': tables,
            'counts': {
                'locations': location_count,
                'amenities': amenity_count,
                'assignments': assignment_count
            },
            'sample_locations': sample_locations,
            'sample_amenities': sample_amenities,
            'sample_assignments': sample_assignments,
            'first_location_amenities': first_location_amenities
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/amenity-cleanup/delete', methods=['POST'])
def delete_amenity():
    """Delete an amenity and all its references"""
    import sqlite3
    import os
    import time
    import json
    
    start_time = time.time()
    
    try:
        data = request.get_json()
        amenity_id = data.get('amenity_id')
        amenity_name = data.get('amenity_name', 'Unknown')
        
        if not amenity_id:
            return jsonify({'error': 'Missing amenity_id parameter'}), 400
        
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'mgg.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get amenity info before deletion
        cursor.execute("SELECT name FROM amenity_features WHERE id = ?", (amenity_id,))
        amenity = cursor.fetchone()
        if not amenity:
            conn.close()
            return jsonify({'error': 'Amenity not found'}), 404
        
        actual_name = amenity[0]
        
        # Get count of locations that will be affected
        cursor.execute("SELECT COUNT(*) FROM location_amenity_assignments WHERE amenity_id = ?", (amenity_id,))
        affected_locations = cursor.fetchone()[0]
        
        # Get locations that will become completely unassigned (only have this amenity)
        cursor.execute("""
            SELECT laa.location_id
            FROM location_amenity_assignments laa
            WHERE laa.amenity_id = ?
            AND NOT EXISTS (
                SELECT 1 FROM location_amenity_assignments laa2 
                WHERE laa2.location_id = laa.location_id 
                AND laa2.amenity_id != ?
            )
        """, (amenity_id, amenity_id))
        
        unassigned_locations = [row[0] for row in cursor.fetchall()]
        
        # Start transaction
        cursor.execute("BEGIN TRANSACTION")
        
        try:
            # Delete all location assignments for this amenity
            cursor.execute("DELETE FROM location_amenity_assignments WHERE amenity_id = ?", (amenity_id,))
            assignments_deleted = cursor.rowcount
            
            # Delete the amenity itself
            cursor.execute("DELETE FROM amenity_features WHERE id = ?", (amenity_id,))
            amenity_deleted = cursor.rowcount
            
            # Log the deletion operation
            execution_time_ms = int((time.time() - start_time) * 1000)
            
            cursor.execute("""
                INSERT INTO split_logging (
                    source_amenity_id, source_amenity_name, operation_type, target_amenities,
                    locations_processed, locations_reassigned, locations_unassigned,
                    source_removed, user_notes, operation_status, execution_time_ms
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                amenity_id, actual_name, 'delete', json.dumps([]),
                affected_locations, 0, len(unassigned_locations),
                True, f'Deleted amenity "{actual_name}"', 'success', execution_time_ms
            ))
            
            split_log_id = cursor.lastrowid
            
            # Log details about affected locations
            for location_id in unassigned_locations:
                cursor.execute("""
                    SELECT title, city, state, year FROM locations WHERE id = ?
                """, (location_id,))
                loc_data = cursor.fetchone()
                
                if loc_data:
                    cursor.execute("""
                        INSERT INTO split_location_details (
                            split_log_id, location_id, location_title, location_city, location_state, location_year,
                            old_amenity_id, old_amenity_name, new_amenity_id, new_amenity_name, reassignment_type
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        split_log_id, location_id, loc_data[0], loc_data[1], loc_data[2], loc_data[3],
                        amenity_id, actual_name, None, 'None', 'deleted'
                    ))
            
            # Commit transaction
            cursor.execute("COMMIT")
            
            conn.close()
            
            return jsonify({
                'success': True,
                'message': f'Successfully deleted amenity "{actual_name}"',
                'details': {
                    'amenity_deleted': amenity_deleted,
                    'assignments_removed': assignments_deleted,
                    'locations_affected': affected_locations,
                    'locations_unassigned': len(unassigned_locations),
                    'execution_time_ms': execution_time_ms
                }
            })
            
        except Exception as e:
            # Rollback on error
            cursor.execute("ROLLBACK")
            conn.close()
            raise e
            
    except Exception as e:
        print(f"Error in delete_amenity: {e}")
        return jsonify({'error': str(e)}), 500


@bp.route('/all-amenities-city-data/<int:year>')
def get_all_amenities_city_data_by_year(year):
    """Get city-level data for all amenities combined in a specific year"""
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'mgg.db')
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Get city-level counts for all amenities combined in the specific year
        cursor.execute("""
            SELECT 
                l.city,
                l.state,
                COUNT(DISTINCT l.id) as count,
                AVG(l.latitude) as avg_lat,
                AVG(l.longitude) as avg_lng
            FROM locations l
            WHERE l.year = ?
            AND l.latitude IS NOT NULL 
            AND l.longitude IS NOT NULL
            GROUP BY l.city, l.state
            HAVING COUNT(DISTINCT l.id) > 0
            ORDER BY count DESC
        """, (year,))
        
        city_data = cursor.fetchall()
        
        # Convert to list of dictionaries
        cities = []
        for row in city_data:
            cities.append({
                'city': row['city'],
                'state': row['state'],
                'count': row['count'],
                'latitude': float(row['avg_lat']) if row['avg_lat'] else None,
                'longitude': float(row['avg_lng']) if row['avg_lng'] else None
            })
        
        conn.close()
        
        return jsonify({
            'amenity': 'All Amenities',
            'year': year,
            'cities': cities,
            'total_cities': len(cities)
        })
        
    except Exception as e:
        print(f"Error getting all amenities city data for year {year}: {e}")
        return jsonify({'error': f'Failed to load city data: {str(e)}'}), 500






@bp.route('/amenities-trends')
def get_amenities_trends():
    """Get amenities trends data for visualization - OPTIMIZED VERSION"""
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'mgg.db')
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Get all available years
        cursor.execute("SELECT DISTINCT year FROM locations WHERE year IS NOT NULL ORDER BY year")
        years_result = cursor.fetchall()
        years = [row['year'] for row in years_result] if years_result else []
        
        # Get all amenities
        cursor.execute("SELECT DISTINCT name FROM amenity_features ORDER BY name")
        amenities_result = cursor.fetchall()
        amenities = [row['name'] for row in amenities_result] if amenities_result else []
        
        # Calculate total locations per year in one optimized query
        cursor.execute("""
            SELECT year, COUNT(*) as total_count 
            FROM locations 
            WHERE year IS NOT NULL 
            GROUP BY year 
            ORDER BY year
        """)
        total_locations_data = cursor.fetchall()
        total_locations_per_year = [0] * len(years)
        for row in total_locations_data:
            year_index = years.index(row['year'])
            total_locations_per_year[year_index] = row['total_count']
        
        # Calculate trends for all amenities in one optimized query
        cursor.execute("""
            SELECT af.name as amenity_name, l.year, COUNT(DISTINCT l.id) as count
            FROM locations l
            JOIN location_amenity_assignments laa ON l.id = laa.location_id
            JOIN amenity_features af ON laa.amenity_id = af.id
            WHERE l.year IS NOT NULL
            GROUP BY af.name, l.year
            ORDER BY af.name, l.year
        """)
        
        trends_data = cursor.fetchall()
        trends = {}
        
        # Initialize all amenities with zeros
        for amenity in amenities:
            trends[amenity] = [0] * len(years)
        
        # Fill in the actual counts
        for row in trends_data:
            amenity_name = row['amenity_name']
            year = row['year']
            count = row['count']
            
            if amenity_name in trends and year in years:
                year_index = years.index(year)
                trends[amenity_name][year_index] = count
        
        conn.close()
        
        print(f"OPTIMIZED API Response: {len(amenities)} amenities, {len(years)} years")
        print(f"Total locations per year: {total_locations_per_year[:5]}...")  # Show first 5 years
        
        return jsonify({
            'amenities': amenities,
            'years': years,
            'trends': trends,
            'totalLocations': total_locations_per_year
        })
        
    except Exception as e:
        print(f"Error getting amenities trends: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Failed to load amenities trends: {str(e)}'}), 500


