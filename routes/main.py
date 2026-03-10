import os
from flask import Blueprint, render_template, request
from models import db, Location, LocationType, AmenityFeature, LocationAmenityAssignment
from sqlalchemy import or_, func

bp = Blueprint('main', __name__)

@bp.route('/map')
def map():
    """Main map visualization"""
    mapbox_token = os.environ.get('MAPBOX_ACCESS_TOKEN', '')
    return render_template('map.html', mapbox_token=mapbox_token)

@bp.route('/database')
def database():
    """Database browser page"""
    # Get query parameters
    page = request.args.get('page', 1, type=int)
    year = request.args.get('year', type=str)
    # Set default year to 1965 if no year is specified
    if year is None:
        year = 1965
    elif year == '':
        year = None  # User selected "All Years"
    else:
        year = int(year)
    state = request.args.get('state', type=str)
    amenity = request.args.get('amenity', type=str)
    search = request.args.get('search', type=str)
    sort_by = request.args.get('sort', 'year')
    sort_order = request.args.get('order', 'desc')
    per_page = 20
    
    try:
        # Build base query
        query = Location.query
        
        # Apply filters
        if year:
            query = query.filter(Location.year == year)
        
        if state:
            query = query.filter(Location.state == state)
        
        if amenity:
            # Filter by amenity feature
            query = query.join(LocationAmenityAssignment).join(AmenityFeature).filter(
                AmenityFeature.name == amenity
            ).distinct()
        
        # Apply search if provided
        if search and search.strip():
            search_term = f"%{search.strip()}%"
            query = query.filter(
                or_(
                    Location.title.like(search_term),
                    Location.description.like(search_term),
                    Location.city.like(search_term),
                    Location.state.like(search_term)
                )
            )
        
        # Apply sorting
        if sort_by == 'city':
            if sort_order == 'desc':
                query = query.order_by(Location.city.desc(), Location.title)
            else:
                query = query.order_by(Location.city, Location.title)
        elif sort_by == 'state':
            if sort_order == 'desc':
                query = query.order_by(Location.state.desc(), Location.title)
            else:
                query = query.order_by(Location.state, Location.title)
        elif sort_by == 'title':
            if sort_order == 'desc':
                query = query.order_by(Location.title.desc())
            else:
                query = query.order_by(Location.title)
        else:  # Default: sort by year
            if sort_order == 'desc':
                query = query.order_by(Location.year.desc(), Location.title)
            else:
                query = query.order_by(Location.year, Location.title)
        
        # Get total count for pagination
        total_count = query.count()
        
        # Get paginated results
        offset = (page - 1) * per_page
        locations = query.offset(offset).limit(per_page).all()
        
        # Convert to dictionaries and add amenities
        location_dicts = []
        for loc in locations:
            loc_dict = loc.to_dict()
            
            # Get amenities for this location
            amenity_list = db.session.query(AmenityFeature.name).join(
                LocationAmenityAssignment
            ).filter(
                LocationAmenityAssignment.location_id == loc.id
            ).order_by(AmenityFeature.name).all()
            
            loc_dict['amenities'] = [{'name': name[0]} for name in amenity_list]
            location_dicts.append(loc_dict)
        
        # Get available years for filter dropdown
        years = db.session.query(Location.year).filter(
            Location.year.isnot(None)
        ).distinct().order_by(Location.year).all()
        years = [row[0] for row in years]
        
        # Get available cities and states
        cities = db.session.query(Location.city).filter(
            Location.city.isnot(None)
        ).distinct().order_by(Location.city).all()
        cities = [row[0] for row in cities if row[0]]
        
        states = db.session.query(Location.state).filter(
            Location.state.isnot(None)
        ).distinct().order_by(Location.state).all()
        states = [row[0] for row in states if row[0]]
        
        # Get available amenity features
        amenities = db.session.query(AmenityFeature.name).distinct().order_by(
            AmenityFeature.name
        ).all()
        amenities = [row[0] for row in amenities if row[0]]
        
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
                    start_page = max(1, page - 2)
                    end_page = min(total_pages, start_page + 4)
                    if end_page - start_page < 4:
                        start_page = max(1, end_page - 4)
                    for num in range(start_page, end_page + 1):
                        yield num
                self.iter_pages = iter_pages.__get__(self)
        
        pagination = Pagination(location_dicts, page, per_page, total_count, total_pages, has_prev, has_next)
        
        return render_template('database.html', 
                             locations=location_dicts, 
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
    
    except Exception as e:
        print(f"Database error: {e}")
        import traceback
        traceback.print_exc()
        return render_template('database.html', error=str(e))

# Utility pages moved to admin section
# See routes/admin.py for amenity-cleanup and smart-split routes
