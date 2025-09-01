from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_flatpages import FlatPages
import os

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/amandaregan/Dropbox/MappingGayGuides/MGG-Site/mgg.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Flask-FlatPages configuration
app.config['FLATPAGES_ROOT'] = 'content/markdown'
app.config['FLATPAGES_EXTENSION'] = '.md'
app.config['FLATPAGES_MARKDOWN_EXTENSIONS'] = ['codehilite', 'fenced_code', 'tables', 'toc', 'attr_list', 'footnotes']

# Initialize extensions
db = SQLAlchemy()
pages = FlatPages(app)

# Initialize the app with extensions FIRST
db.init_app(app)

# Models are now handled directly in the API routes

def ensure_database_exists():
    """Ensure the database exists"""
    if not os.path.exists('mgg.db'):
        print("Database not found. Please run create_database.py first!")
        return False
    print("Database found and ready!")
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
    app.run(debug=True, port=5001)
