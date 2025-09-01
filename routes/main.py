from flask import Blueprint, render_template
from models import db

bp = Blueprint('main', __name__)

@bp.route('/map')
def map():
    """Main map visualization"""
    return render_template('map.html')

@bp.route('/database')
def database():
    """Database browser page"""
    import sqlite3
    import os
    from flask import request
    
    # Get query parameters
    page = request.args.get('page', 1, type=int)
    year = request.args.get('year', type=str)  # Get as string to handle empty value for "All Years"
    # Set default year to 1965 if no year is specified
    if year is None:
        year = 1965
    elif year == '':
        year = None  # User selected "All Years"
    else:
        year = int(year)  # Convert to int for filtering
    state = request.args.get('state', type=str)
    amenity = request.args.get('amenity', type=str)
    search = request.args.get('search', type=str)  # Add search parameter
    sort_by = request.args.get('sort', 'year')  # Default sort by year
    sort_order = request.args.get('order', 'desc')  # Default descending
    per_page = 20
    
    # Connect to database
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'mgg.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
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
        else:  # Default: sort by year
            order_clause += f"l.year {'DESC' if sort_order == 'desc' else 'ASC'}, l.title"
        
        # Get total count for pagination
        count_query = f"SELECT COUNT(*) {base_query}"
        cursor.execute(count_query, params)
        total_count = cursor.fetchone()[0]
        
        # Get paginated results with amenities
        offset = (page - 1) * per_page
        
        # First get the basic location data without JOINs to avoid duplicates
        select_query = f"SELECT l.* {base_query} {order_clause} LIMIT ? OFFSET ?"
        cursor.execute(select_query, params + [per_page, offset])
        locations = [dict(row) for row in cursor.fetchall()]
        
        # Now fetch amenities for each location separately to avoid JOIN issues
        for location in locations:
            location_id = location['id']
            
            # Get amenities for this specific location
            cursor.execute("""
                SELECT af.name 
                FROM amenity_features af
                JOIN location_amenity_assignments laa ON af.id = laa.amenity_id
                WHERE laa.location_id = ?
                ORDER BY af.name
            """, (location_id,))
            
            amenity_names = [row[0] for row in cursor.fetchall()]
            if amenity_names:
                # Convert to list of objects with 'name' property as template expects
                location['amenities'] = [{'name': name} for name in amenity_names]
            else:
                location['amenities'] = []
        
        # Get available years for filter dropdown
        cursor.execute("SELECT DISTINCT year FROM locations WHERE year IS NOT NULL ORDER BY year DESC")
        years = [row[0] for row in cursor.fetchall()]
        
        # Get available cities and states for sorting context
        cursor.execute("SELECT DISTINCT city FROM locations WHERE city IS NOT NULL ORDER BY city")
        cities = [row[0] for row in cursor.fetchall() if row[0]]
        
        cursor.execute("SELECT DISTINCT state FROM locations WHERE state IS NOT NULL ORDER BY state")
        states = [row[0] for row in cursor.fetchall() if row[0]]
        
        # Get available amenity features
        cursor.execute("SELECT DISTINCT name FROM amenity_features ORDER BY name")
        amenities = [row[0] for row in cursor.fetchall() if row[0]]
        
        # Calculate pagination info
        total_pages = (total_count + per_page - 1) // per_page
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
                def iter_pages(self, left_edge=2, left_current=2, right_current=3, right_edge=2):
                    # Calculate the range of 5 pages to show
                    start_page = max(1, page - 2)
                    end_page = min(total_pages, start_page + 4)
                    
                    # Adjust start if we're near the end
                    if end_page - start_page < 4:
                        start_page = max(1, end_page - 4)
                    
                    # Yield the 5 sequential pages
                    for num in range(start_page, end_page + 1):
                        yield num
                self.iter_pages = iter_pages.__get__(self)
        
        pagination = Pagination(locations, page, per_page, total_count, total_pages, has_prev, has_next)
        
        return render_template('database.html', 
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

# Utility pages moved to admin section
# See routes/admin.py for amenity-cleanup and smart-split routes
