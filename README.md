# Mapping the Gay Guides - Flask Version

A digital history project exploring LGBTQ+ spaces through historical travel guides, built with Flask and SQLite.

## Features

- Interactive map visualization using Leaflet.js
- SQLite database for storing location and article data
- RESTful API endpoints for data access
- Responsive Bootstrap-based UI
- Content management for articles and research

## Setup

### Prerequisites

- Python 3.8+
- pip

### Installation

1. Clone the repository and navigate to the project directory:
```bash
cd MGG-Site
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the database:
```bash
python
>>> from app import app, db
>>> with app.app_context():
...     db.create_all()
>>> exit()
```

5. Run the application:
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Project Structure

```
MGG-Site/
├── app.py                 # Main Flask application
├── models.py             # Database models
├── routes/               # Route blueprints
│   ├── __init__.py
│   ├── main.py          # Main page routes
│   └── api.py           # API endpoints
├── templates/            # HTML templates
│   ├── base.html        # Base template
│   ├── index.html       # Home page
│   └── map.html         # Map page
├── static/               # Static assets
│   ├── css/
│   │   └── style.css    # Custom styles
│   └── js/
│       ├── main.js      # General JavaScript
│       └── map.js       # Map functionality
└── requirements.txt      # Python dependencies
```

## Database Models

### Location
- Stores information about LGBTQ+ spaces from historical guides
- Includes coordinates, categories, years, and descriptions
- Supports filtering by location, time period, and type

### Article
- Manages research articles and content
- Supports markdown content and metadata
- Includes publication status and author information

## API Endpoints

- `GET /api/locations` - Get all locations
- `GET /api/locations/<id>` - Get specific location
- `GET /api/articles` - Get all articles
- `GET /api/articles/<id>` - Get specific article

## Development

### Adding New Routes
Create new route files in the `routes/` directory and register them in `app.py`.

### Database Migrations
Use Flask-Migrate for database schema changes:
```bash
flask db init
flask db migrate -m "Description of changes"
flask db upgrade
```

### Styling
Custom CSS is in `static/css/style.css`. The site uses Bootstrap 5 for the base framework.

## Contributing

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## License

This project is part of the Mapping the Gay Guides digital history initiative.
