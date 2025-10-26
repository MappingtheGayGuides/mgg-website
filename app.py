from flask import Flask, render_template, jsonify
from flask_flatpages import FlatPages
import os
from models import db  # Import db from models

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')
# Database URI: Use DATABASE_URL from environment (e.g., PostgreSQL from Digital Ocean)
# Fallback to local SQLite for development
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///mgg.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Flask-FlatPages configuration
app.config['FLATPAGES_ROOT'] = 'content/markdown'
app.config['FLATPAGES_EXTENSION'] = '.md'
app.config['FLATPAGES_MARKDOWN_EXTENSIONS'] = ['codehilite', 'fenced_code', 'tables', 'toc', 'attr_list', 'footnotes']

# Initialize extensions
pages = FlatPages(app)

# Initialize the app with extensions FIRST
db.init_app(app)

# Models are now handled directly in the API routes

def ensure_database_exists():
    """Ensure the database exists and create tables if needed"""
    from models import Location, LocationType, AmenityFeature, UniqueLocation
    with app.app_context():
        # This will create tables if they don't exist
        db.create_all()
        print("✓ Database ready!")
        return True

# Route for static content pages using Flask-FlatPages
@app.route('/')
def index():
    """Serve the homepage with hero section"""
    page = pages.get_or_404('index')
    return render_template('homepage.html', page=page)

# Articles page route
@app.route('/articles/')
def articles():
    """Serve the articles/blog page"""
    # Get all articles from the markdown directory
    articles_list = []
    for article in pages:
        if hasattr(article, 'meta') and article.meta.get('title') and not article.meta.get('draft', True):
            articles_list.append({
                'title': article.meta.get('title', 'Untitled'),
                'date': article.meta.get('date', 'No date'),
                'author': article.meta.get('author', 'Unknown'),
                'description': article.meta.get('description', ''),
                'tags': article.meta.get('tags', []),
                'draft': article.meta.get('draft', False),
                'img': article.meta.get('img', ''),
                'url': article.path,
                'content': article.html
            })
    
    # Sort articles by date (newest first)
    articles_list.sort(key=lambda x: x['date'], reverse=True)
    
    return render_template('articles.html', articles=articles_list)

# Individual article route
@app.route('/articles/<path:path>/')
def article(path):
    """Serve individual article pages"""
    article = pages.get_or_404(path)
    return render_template('article.html', article=article)

# Amenities visualization route
@app.route('/amenities/')
def amenities():
    """Serve the amenities visualization page"""
    return render_template('amenities.html')

# Generic route for any markdown page
@app.route('/<path:path>/')
def page(path):
    """Serve any markdown page"""
    page = pages.get_or_404(path)
    return render_template('page.html', page=page)

# Import routes after db initialization to avoid circular imports
from routes import main, api

# Register blueprints
app.register_blueprint(main.bp)
app.register_blueprint(api.bp, url_prefix='/api')

if __name__ == '__main__':
    ensure_database_exists()
    
    # Get port from environment variable (for production) or default to 5001 (for local dev)
    port = int(os.environ.get('PORT', 5001))
    # Only run in debug mode if not in production
    debug = os.environ.get('FLASK_ENV') != 'production'
    
    app.run(debug=debug, host='0.0.0.0', port=port)
