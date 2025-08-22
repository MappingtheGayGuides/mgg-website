from flask import Blueprint, render_template
from models import db

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@bp.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@bp.route('/map')
def map():
    """Main map visualization"""
    return render_template('map.html')

@bp.route('/articles')
def articles():
    """Articles listing page"""
    return render_template('articles.html')

@bp.route('/methodology')
def methodology():
    """Methodology page"""
    return render_template('methodology.html')

@bp.route('/database')
def database():
    """Database browser page"""
    from models import Location, AmenityFeature
    from flask import request, current_app
    from sqlalchemy import distinct
    
    # Get query parameters
    page = request.args.get('page', 1, type=int)
    year = request.args.get('year', type=int)
    state = request.args.get('state', type=str)
    amenity = request.args.get('amenity', type=str)
    search = request.args.get('search', type=str)  # Add search parameter
    sort_by = request.args.get('sort', 'year')  # Default sort by year
    sort_order = request.args.get('order', 'desc')  # Default descending
    per_page = 20
    
    # Get the database session from the Flask app
    db = current_app.extensions['sqlalchemy'].db
    
    # Build query using the proper session
    query = db.session.query(Location)
    
    # Apply filters
    if year:
        query = query.filter(Location.year == year)
    
    if state:
        query = query.filter(Location.state == state)
    
    if amenity:
        # Filter by amenity feature
        query = query.join(Location.amenities).filter(AmenityFeature.name == amenity)
    
    # Apply search if provided
    if search and search.strip():
        search_term = f"%{search.strip()}%"
        query = query.filter(
            db.or_(
                Location.title.ilike(search_term),
                Location.description.ilike(search_term),
                Location.city.ilike(search_term),
                Location.state.ilike(search_term),
                Location.year.cast(db.String).ilike(search_term)
            )
        )
    
    # Apply sorting
    if sort_by == 'city':
        if sort_order == 'desc':
            query = query.order_by(Location.city.desc().nullslast(), Location.title)
        else:
            query = query.order_by(Location.city.asc().nullslast(), Location.title)
    elif sort_by == 'state':
        if sort_order == 'desc':
            query = query.order_by(Location.state.desc().nullslast(), Location.title)
        else:
            query = query.order_by(Location.state.asc().nullslast(), Location.title)
    elif sort_by == 'title':
        if sort_order == 'desc':
            query = query.order_by(Location.title.desc())
        else:
            query = query.order_by(Location.title.asc())
    else:  # Default: sort by year
        if sort_order == 'desc':
            query = query.order_by(Location.year.desc().nullslast(), Location.title)
        else:
            query = query.order_by(Location.year.asc().nullslast(), Location.title)
    
    # Get available years for filter dropdown
    years = db.session.query(Location.year).distinct().filter(Location.year.isnot(None)).order_by(Location.year.desc()).all()
    years = [y[0] for y in years]
    
    # Get available cities and states for sorting context
    cities = db.session.query(Location.city).distinct().filter(Location.city.isnot(None)).order_by(Location.city).all()
    cities = [c[0] for c in cities if c[0]]
    
    states = db.session.query(Location.state).distinct().filter(Location.state.isnot(None)).order_by(Location.state).all()
    states = [s[0] for s in states if s[0]]
    
    # Get available amenity features
    amenities = db.session.query(AmenityFeature.name).distinct().order_by(AmenityFeature.name).all()
    amenities = [a[0] for a in amenities if a[0]]
    
    # Paginate results
    pagination = query.paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    locations = pagination.items
    
    return render_template('database.html', 
                         locations=locations, 
                         pagination=pagination, 
                         years=years, 
                         selected_year=year,
                         selected_state=state,
                         selected_amenity=amenity,
                         search=search,  # Pass search to template
                         sort_by=sort_by,
                         sort_order=sort_order,
                         cities=cities,
                         states=states,
                         amenities=amenities)
