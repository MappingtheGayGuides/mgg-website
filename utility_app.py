#!/usr/bin/env python3
"""
Standalone utility app for Mapping Gay Guides development tools
Run with: python utility_app.py
"""

from flask import Flask, render_template, request, jsonify
import sqlite3
import os
import re
from difflib import SequenceMatcher

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'dev-utility-key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

def get_db_connection():
    """Get database connection"""
    db_path = os.path.join(os.path.dirname(__file__), 'mgg.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    """Utility tools index"""
    return render_template('utility/index.html')

@app.route('/amenity-cleanup')
def amenity_cleanup():
    """Amenity cleanup interface page"""
    conn = get_db_connection()
    try:
        # Get all amenities with usage counts
        cursor = conn.cursor()
        cursor.execute("""
            SELECT af.id, af.name, COUNT(laa.location_id) as usage_count
            FROM amenity_features af
            LEFT JOIN location_amenity_assignments laa ON af.id = laa.amenity_id
            GROUP BY af.id, af.name
            ORDER BY af.name ASC
        """)
        amenities = [dict(row) for row in cursor.fetchall()]
        
        # Get all locations for reference
        cursor.execute("SELECT id, title, city, state FROM locations")
        locations = [dict(row) for row in cursor.fetchall()]
        
        return render_template('utility/amenity_cleanup.html', 
                             amenities=amenities,
                             locations=locations)
    finally:
        conn.close()

# API Routes for Amenity Cleanup
@app.route('/api/amenity-cleanup/rename', methods=['POST'])
def rename_amenity():
    """Rename an amenity feature"""
    try:
        data = request.get_json()
        amenity_id = data.get('amenity_id')
        new_name = data.get('new_name')
        
        if not amenity_id or not new_name:
            return jsonify({'success': False, 'error': 'Missing amenity_id or new_name'})
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if new name already exists
        cursor.execute("SELECT id FROM amenity_features WHERE name = ? AND id != ?", (new_name, amenity_id))
        if cursor.fetchone():
            conn.close()
            return jsonify({'success': False, 'error': 'An amenity with that name already exists'})
        
        # Update the amenity name
        cursor.execute("UPDATE amenity_features SET name = ? WHERE id = ?", (new_name, amenity_id))
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Amenity renamed successfully'})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/amenity-cleanup/usage/<int:amenity_id>')
def get_amenity_usage(amenity_id):
    """Get locations that use a specific amenity"""
    try:
        conn = get_db_connection()
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

@app.route('/api/amenity-cleanup/merge', methods=['POST'])
def merge_amenities():
    """Merge multiple amenities into one"""
    try:
        data = request.get_json()
        keep_id = data.get('keep_id')
        merge_ids = data.get('merge_ids')
        
        if not keep_id or not merge_ids:
            return jsonify({'success': False, 'error': 'Missing keep_id or merge_ids'})
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Update all location assignments to use the kept amenity
        cursor.execute("""
            UPDATE location_amenity_assignments 
            SET amenity_id = ? 
            WHERE amenity_id IN ({})
        """.format(','.join('?' * len(merge_ids))), [keep_id] + merge_ids)
        
        # Delete the merged amenities
        cursor.execute("""
            DELETE FROM amenity_features 
            WHERE id IN ({})
        """.format(','.join('?' * len(merge_ids))), merge_ids)
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': f'Successfully merged {len(merge_ids)} amenities'})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/amenity-cleanup/find-similar')
def find_similar_amenities():
    """Find groups of similar amenities that could be merged"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get all amenities
        cursor.execute("SELECT id, name FROM amenity_features ORDER BY name")
        amenities = [dict(row) for row in cursor.fetchall()]
        
        # Group similar amenities
        similar_groups = []
        processed = set()
        
        for i, amenity1 in enumerate(amenities):
            if amenity1['id'] in processed:
                continue
                
            similar_group = [amenity1]
            processed.add(amenity1['id'])
            
            for j, amenity2 in enumerate(amenities[i+1:], i+1):
                if amenity2['id'] in processed:
                    continue
                    
                # Calculate similarity
                similarity = SequenceMatcher(None, amenity1['name'].lower(), amenity2['name'].lower()).ratio()
                
                if similarity > 0.7:  # 70% similarity threshold
                    similar_group.append(amenity2)
                    processed.add(amenity2['id'])
            
            if len(similar_group) > 1:
                similar_groups.append(similar_group)
        
        conn.close()
        return jsonify(similar_groups)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/amenity-cleanup/smart-merge', methods=['POST'])
def smart_merge_amenities():
    """Smart merge similar amenities"""
    try:
        data = request.get_json()
        target_name = data.get('target_name')
        source_ids = data.get('source_ids')
        
        if not target_name or not source_ids:
            return jsonify({'success': False, 'error': 'Missing target_name or source_ids'})
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Create new target amenity if it doesn't exist
        cursor.execute("SELECT id FROM amenity_features WHERE name = ?", (target_name,))
        target_amenity = cursor.fetchone()
        
        if target_amenity:
            target_id = target_amenity['id']
        else:
            cursor.execute("INSERT INTO amenity_features (name) VALUES (?)", (target_name,))
            target_id = cursor.lastrowid
        
        # Update all location assignments to use the target amenity
        cursor.execute("""
            UPDATE location_amenity_assignments 
            SET amenity_id = ? 
            WHERE amenity_id IN ({})
        """.format(','.join('?' * len(source_ids))), [target_id] + source_ids)
        
        # Delete the source amenities
        cursor.execute("""
            DELETE FROM amenity_features 
            WHERE id IN ({})
        """.format(','.join('?' * len(source_ids))), source_ids)
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': f'Successfully merged {len(source_ids)} amenities into "{target_name}"'})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/amenity-cleanup/get-location-years/<int:amenity_id>')
def get_location_years(amenity_id):
    """Get year distribution for locations using a specific amenity"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get all locations using this amenity
        cursor.execute("""
            SELECT l.id, l.title, l.city, l.state, l.year
            FROM locations l
            JOIN location_amenity_assignments laa ON l.id = laa.location_id
            WHERE laa.amenity_id = ?
            ORDER BY l.title
        """, (amenity_id,))
        
        locations = [dict(row) for row in cursor.fetchall()]
        
        # Calculate year statistics
        years = [loc['year'] for loc in locations if loc['year'] is not None]
        year_distribution = {}
        
        for year in years:
            year_distribution[year] = year_distribution.get(year, 0) + 1
        
        year_stats = {
            'total_locations': len(locations),
            'locations_with_years': len(years),
            'min_year': min(years) if years else None,
            'max_year': max(years) if years else None,
            'year_distribution': year_distribution
        }
        
        conn.close()
        
        return jsonify({
            'year_stats': year_stats,
            'locations': locations
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/amenity-cleanup/smart-split', methods=['POST'])
def smart_split_amenity():
    """Smart split amenity by reassigning locations to different categories"""
    try:
        data = request.get_json()
        source_amenity_id = data.get('source_amenity_id')
        target_mappings = data.get('target_mappings')
        manual_assignments = data.get('manual_assignments')
        
        if not source_amenity_id or not target_mappings or not manual_assignments:
            return jsonify({'success': False, 'error': 'Missing required parameters'})
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Process manual assignments
        for assignment in manual_assignments:
            location_id = assignment['location_id']
            target_amenity_id = assignment['target_amenity_id']
            
            # Remove old assignment
            cursor.execute("""
                DELETE FROM location_amenity_assignments 
                WHERE location_id = ? AND amenity_id = ?
            """, (location_id, source_amenity_id))
            
            # Add new assignment
            cursor.execute("""
                INSERT INTO location_amenity_assignments (location_id, amenity_id)
                VALUES (?, ?)
            """, (location_id, target_amenity_id))
        
        # Log the split operation
        cursor.execute("""
            INSERT INTO split_logging (source_amenity_id, target_mappings, manual_assignments, timestamp)
            VALUES (?, ?, ?, datetime('now'))
        """, (source_amenity_id, str(target_mappings), str(manual_assignments)))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': f'Successfully split amenity and reassigned {len(manual_assignments)} locations'})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/amenity-cleanup/split-history')
def get_split_history():
    """Get history of smart split operations"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, source_amenity_id, target_mappings, manual_assignments, timestamp
            FROM split_logging
            ORDER BY timestamp DESC
            LIMIT 50
        """)
        
        splits = []
        for row in cursor.fetchall():
            split = dict(row)
            # Get source amenity name
            cursor.execute("SELECT name FROM amenity_features WHERE id = ?", (split['source_amenity_id'],))
            source_amenity = cursor.fetchone()
            split['source_amenity_name'] = source_amenity['name'] if source_amenity else 'Unknown'
            splits.append(split)
        
        conn.close()
        return jsonify(splits)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/amenity-cleanup/split-details/<int:split_id>')
def get_split_details(split_id):
    """Get detailed information about a specific split operation"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM split_logging WHERE id = ?
        """, (split_id,))
        
        split = cursor.fetchone()
        if not split:
            return jsonify({'error': 'Split not found'}), 404
        
        conn.close()
        return jsonify(dict(split))
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/amenity-cleanup/split-stats')
def get_split_stats():
    """Get statistics about split operations"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Total splits
        cursor.execute("SELECT COUNT(*) as total_splits FROM split_logging")
        total_splits = cursor.fetchone()['total_splits']
        
        # Recent splits (last 30 days)
        cursor.execute("""
            SELECT COUNT(*) as recent_splits 
            FROM split_logging 
            WHERE timestamp > datetime('now', '-30 days')
        """)
        recent_splits = cursor.fetchone()['recent_splits']
        
        # Most split amenities
        cursor.execute("""
            SELECT source_amenity_id, COUNT(*) as split_count
            FROM split_logging
            GROUP BY source_amenity_id
            ORDER BY split_count DESC
            LIMIT 5
        """)
        
        top_split_amenities = []
        for row in cursor.fetchall():
            cursor.execute("SELECT name FROM amenity_features WHERE id = ?", (row['source_amenity_id'],))
            amenity = cursor.fetchone()
            if amenity:
                top_split_amenities.append({
                    'name': amenity['name'],
                    'split_count': row['split_count']
                })
        
        conn.close()
        
        return jsonify({
            'total_splits': total_splits,
            'recent_splits': recent_splits,
            'top_split_amenities': top_split_amenities
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/amenity-cleanup/delete', methods=['POST'])
def delete_split_record():
    """Delete a split record"""
    try:
        data = request.get_json()
        split_id = data.get('split_id')
        
        if not split_id:
            return jsonify({'success': False, 'error': 'Missing split_id'})
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM split_logging WHERE id = ?", (split_id,))
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Split record deleted successfully'})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/amenity-cleanup/delete-amenity', methods=['POST'])
def delete_amenity():
    """Delete an amenity feature"""
    try:
        data = request.get_json()
        amenity_id = data.get('amenity_id')
        
        if not amenity_id:
            return jsonify({'success': False, 'error': 'Missing amenity_id'})
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if amenity is used by any locations
        cursor.execute("SELECT COUNT(*) FROM location_amenity_assignments WHERE amenity_id = ?", (amenity_id,))
        usage_count = cursor.fetchone()[0]
        
        if usage_count > 0:
            return jsonify({'success': False, 'error': f'Cannot delete amenity: it is used by {usage_count} locations. Please reassign or delete those locations first.'})
        
        # Delete the amenity
        cursor.execute("DELETE FROM amenity_features WHERE id = ?", (amenity_id,))
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Amenity deleted successfully'})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/smart-split')
def smart_split():
    """Smart Split page for manually assigning locations to amenity categories"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get all amenities with usage counts
        cursor.execute("""
            SELECT af.id, af.name, COUNT(laa.location_id) as usage_count
            FROM amenity_features af
            LEFT JOIN location_amenity_assignments laa ON af.id = laa.amenity_id
            GROUP BY af.id, af.name
            ORDER BY af.name ASC
        """)
        
        amenities = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        
        return render_template('utility/smart_split.html', amenities=amenities)
        
    except Exception as e:
        print(f"Error in smart_split route: {e}")
        return "Error loading page", 500

@app.route('/database')
def database():
    """Database browser page"""
    # Get query parameters
    page = request.args.get('page', 1, type=int)
    year = request.args.get('year', type=str)
    if year is None:
        year = 1965
    elif year == '':
        year = None
    else:
        year = int(year)
    state = request.args.get('state', type=str)
    amenity = request.args.get('amenity', type=str)
    search = request.args.get('search', type=str)
    sort_by = request.args.get('sort', 'year')
    sort_order = request.args.get('order', 'desc')
    per_page = 20
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Build base query
        base_query = "FROM locations l"
        where_conditions = []
        params = []
        
        # Apply filters
        if year:
            where_conditions.append("l.year = ?")
            params.append(year)
        
        if state:
            where_conditions.append("l.state = ?")
            params.append(state)
        
        if amenity:
            # Filter by amenity feature
            base_query += " JOIN location_amenity_assignments laa ON l.id = laa.location_id"
            base_query += " JOIN amenity_features af ON laa.amenity_id = af.id"
            where_conditions.append("af.name = ?")
            params.append(amenity)
        
        # Apply search if provided
        if search and search.strip():
            search_term = f"%{search.strip()}%"
            where_conditions.append("(l.title LIKE ? OR l.description LIKE ? OR l.city LIKE ? OR l.state LIKE ?)")
            params.extend([search_term, search_term, search_term, search_term])
        
        # Build WHERE clause
        if where_conditions:
            base_query += " WHERE " + " AND ".join(where_conditions)
        
        # Apply sorting
        order_clause = "ORDER BY "
        if sort_by == 'city':
            order_clause += f"l.city {'DESC' if sort_order == 'desc' else 'ASC'}, l.title"
        elif sort_by == 'state':
            order_clause += f"l.state {'DESC' if sort_order == 'desc' else 'ASC'}, l.title"
        elif sort_by == 'title':
            order_clause += f"l.title {'DESC' if sort_order == 'desc' else 'ASC'}"
        else:
            order_clause += f"l.year {'DESC' if sort_order == 'desc' else 'ASC'}, l.title"
        
        # Get total count
        count_query = f"SELECT COUNT(*) {base_query}"
        cursor.execute(count_query, params)
        total_count = cursor.fetchone()[0]
        
        # Calculate pagination
        total_pages = (total_count + per_page - 1) // per_page
        offset = (page - 1) * per_page
        
        # Get locations for current page
        locations_query = f"""
            SELECT l.*, 
                   GROUP_CONCAT(DISTINCT af.name) as amenities,
                   GROUP_CONCAT(DISTINCT lt.name) as types
            {base_query}
            LEFT JOIN location_amenity_assignments laa ON l.id = laa.location_id
            LEFT JOIN amenity_features af ON laa.amenity_id = af.id
            LEFT JOIN location_type_assignments lta ON l.id = lta.location_id
            LEFT JOIN location_types lt ON lta.type_id = lt.id
            {order_clause}
            LIMIT ? OFFSET ?
        """
        
        cursor.execute(locations_query, params + [per_page, offset])
        locations = [dict(row) for row in cursor.fetchall()]
        
        # Get filter options
        cursor.execute("SELECT DISTINCT year FROM locations WHERE year IS NOT NULL ORDER BY year DESC")
        years = [row['year'] for row in cursor.fetchall()]
        
        cursor.execute("SELECT DISTINCT state FROM locations WHERE state IS NOT NULL ORDER BY state")
        states = [row['state'] for row in cursor.fetchall()]
        
        cursor.execute("SELECT DISTINCT city FROM locations WHERE city IS NOT NULL ORDER BY city")
        cities = [row['city'] for row in cursor.fetchall()]
        
        cursor.execute("SELECT DISTINCT af.name FROM amenity_features af ORDER BY af.name")
        amenities = [row['name'] for row in cursor.fetchall()]
        
        # Pagination info
        has_prev = page > 1
        has_next = page < total_pages
        
        # Create pagination object for template compatibility
        class Pagination:
            def __init__(self, items, page, per_page, total, total_pages, has_prev, has_next):
                self.items = items
                self.page = page
                self.per_page = per_page
                self.total = total
                self.pages = total_pages
                self.prev_num = page - 1 if has_prev else None
                self.next_num = page + 1 if has_next else None
                self.has_prev = has_prev
                self.has_next = has_next
                self.iter_pages = lambda left_edge=2, left_current=2, right_current=3, right_edge=2: range(1, total_pages + 1)
        
        pagination = Pagination(locations, page, per_page, total_count, total_pages, has_prev, has_next)
        
        return render_template('utility/database.html', 
                             locations=locations, 
                             pagination=pagination, 
                             years=years, 
                             selected_year=year,
                             selected_state=state,
                             selected_amenity=amenity,
                             search=search,
                             sort_by=sort_by,
                             sort_order=sort_order,
                             cities=cities,
                             states=states,
                             amenities=amenities)
    
    finally:
        conn.close()

if __name__ == '__main__':
    print("Starting Mapping Gay Guides Utility App...")
    print("Access utility tools at:")
    print("  - http://localhost:5002/ (index)")
    print("  - http://localhost:5002/amenity-cleanup")
    print("  - http://localhost:5002/smart-split")
    print("  - http://localhost:5002/database")
    print("\nPress Ctrl+C to stop")
    
    app.run(debug=True, port=5002)
