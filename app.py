from flask import Flask, render_template, jsonify
from flask_flatpages import FlatPages
import os
from models import db  # Import db from models

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')
# Database URI: Use SQLite3 (switched back from PostgreSQL for Render deployment)
# Use absolute path to the actual database file
db_path = os.path.join(os.path.dirname(__file__), 'mgg.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
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
    """Serve the articles/vignettes page (excludes news posts)"""
    # Get all articles from the markdown directory, excluding news posts
    articles_list = []
    for article in pages:
        # Exclude news posts (category == "Project News") and drafts
        category = article.meta.get('category', '') if hasattr(article, 'meta') else ''
        if (hasattr(article, 'meta') and 
            article.meta.get('title') and 
            not article.meta.get('draft', True) and
            category != 'Project News'):  # Exclude news posts
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

# Amenity guide route (table of amenity blurbs from markdown)
@app.route('/amenity-guide/')
def amenity_guide():
    """Serve the amenity guide page with DaisyUI table layout"""
    import re
    from html import unescape
    page = pages.get_or_404('amenity-guide')
    html = page.html

    h2_pattern = r'<h2[^>]*>(.*?)</h2>'
    matches = list(re.finditer(h2_pattern, html))

    if not matches:
        return render_template('page.html', page=page, is_methodology=False)

    intro_html = html[:matches[0].start()].strip()
    sections = []
    for i, match in enumerate(matches):
        heading = unescape(re.sub(r'<[^>]+>', '', match.group(1))).strip()
        start_pos = match.end()
        end_pos = matches[i + 1].start() if i + 1 < len(matches) else len(html)
        content = html[start_pos:end_pos].strip()
        # Split heading into name (code) and short_description: "CODE - Short Desc"
        parts = heading.split(' - ', 1)
        name = parts[0].strip() if parts else heading
        short_description = parts[1].strip() if len(parts) > 1 else ''
        sections.append({
            'name': name,
            'short_description': short_description,
            'description': content
        })

    return render_template('amenity-guide.html', page=page,
                          intro_html=intro_html, sections=sections)

# News page route
@app.route('/news/')
def news():
    """Serve the news/blog page"""
    # Get all news posts from the markdown directory
    news_list = []
    for page in pages:
        if hasattr(page, 'meta') and page.meta.get('category') == 'Project News' and not page.meta.get('draft', True):
            is_affiliate = page.meta.get('affiliate', False)
            news_list.append({
                'title': page.meta.get('title', 'Untitled'),
                'date': page.meta.get('lastmod', page.meta.get('date', 'No date')),
                'author': page.meta.get('author', 'Unknown'),
                'description': page.meta.get('description', ''),
                'img': page.meta.get('img', ''),
                'url': page.path,
                'content': page.html if not is_affiliate else None,
                'is_affiliate': is_affiliate,
                'affiliatelink': page.meta.get('affiliatelink', ''),
                'affiliatename': page.meta.get('affiliatename', ''),
                'affiliatewebsite': page.meta.get('affiliatewebsite', '')
            })
    
    # Sort news by date (newest first)
    def sort_key(x):
        date_str = x['date']
        try:
            # Try to parse date for sorting
            from datetime import datetime
            # Try different date formats
            for fmt in ['%Y-%m-%d', '%B %d, %Y', '%Y-%m-%d %H:%M:%S']:
                try:
                    return datetime.strptime(date_str, fmt)
                except:
                    continue
            return datetime.min
        except:
            from datetime import datetime
            return datetime.min
    
    news_list.sort(key=sort_key, reverse=True)
    
    # Format dates for display
    from datetime import datetime
    for post in news_list:
        try:
            date_obj = datetime.strptime(post['date'], '%Y-%m-%d')
            post['date_formatted'] = date_obj.strftime('%B %d, %Y')
        except:
            post['date_formatted'] = post['date']
    
    return render_template('news.html', news=news_list)

# Generic route for any markdown page
@app.route('/<path:path>/')
def page(path):
    """Serve any markdown page"""
    page = pages.get_or_404(path)
    
    # Special handling for methodology page - convert h2 sections to accordions
    if path == 'methodology':
        import re
        from html import unescape
        html = page.html
        
        # Find all h2 tags and split content
        h2_pattern = r'<h2[^>]*>(.*?)</h2>'
        matches = list(re.finditer(h2_pattern, html))
        
        if not matches:
            # No h2 tags found, render normally
            return render_template('page.html', page=page, is_methodology=False)
        
        # Get intro content (everything before first h2)
        intro_html = html[:matches[0].start()].strip()
        
        # Process each h2 section
        sections = []
        for i, match in enumerate(matches):
            heading = unescape(re.sub(r'<[^>]+>', '', match.group(1))).strip()
            
            # Get content from this h2 to the next h2 (or end)
            start_pos = match.end()
            end_pos = matches[i + 1].start() if i + 1 < len(matches) else len(html)
            content = html[start_pos:end_pos].strip()
            
            sections.append({'heading': heading, 'content': content})
        
        return render_template('page.html', page=page, is_methodology=True, 
                             intro_html=intro_html, sections=sections)
    
    return render_template('page.html', page=page, is_methodology=False)

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
