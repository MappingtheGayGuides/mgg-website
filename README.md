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

- Python 3.8+ (or Python 3)
- Node.js 16+ and npm
- pip (usually comes with Python)

### Installation

#### Option 1: Automated Setup (Recommended)
```bash
# Make the setup script executable
chmod +x setup.sh

# Run the setup script
./setup.sh
```

#### Option 2: Manual Setup

1. Clone the repository and navigate to the project directory:
```bash
cd MGG-Site
```

2. Install Python dependencies:
```bash
pip3 install -r requirements.txt
```

3. Install Node.js dependencies:
```bash
npm install
```

4. Build Tailwind CSS:
```bash
npm run build
```

5. Initialize the database:
```bash
python3 init_db.py
```

6. Run the application:
```bash
python3 app.py
```

The main application will be available at `http://localhost:5001`

### Running the Application

#### Start the Main App
```bash
python3 app.py
```
Access at: `http://localhost:5001`

#### Development Mode (with auto-reload on changes)
The app runs in debug mode by default, so it will auto-reload when you make changes to Python files.

#### CSS Development
For development with CSS watching:
```bash
npm run build
```
This will watch your template files and rebuild the CSS automatically.

For production builds:
```bash
npm run build-prod
```
This creates a minified, optimized CSS file.

#### Utility Tools

Development tools are available in the `utilities/` directory:

```bash
cd utilities
python utility_app.py
```

Access utility tools at: http://localhost:5002

> **Important:** Utility tools are for local development only. Do not deploy them to production.

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
│   │   ├── input.css   # Tailwind input
│   │   └── style.css   # Compiled CSS
│   └── js/
│       ├── main.js      # General JavaScript
│       ├── map.js       # Map functionality
│       ├── viz.js       # Visualizations
│       └── amenities.js
├── utilities/            # Development tools (NOT for production)
│   ├── utility_app.py   # Utility Flask app (port 5002)
│   ├── templates/       # Utility templates
│   ├── add_amenity.py   # Utility scripts
│   └── README.md        # Utility documentation
├── content/              # Markdown content
│   └── markdown/        # Article files
├── data/                # Data files
├── routes/              # Route blueprints
│   ├── main.py         # Main routes
│   └── api.py          # API endpoints
├── mgg.db              # Database file
├── models.py            # Database models
├── requirements.txt     # Python dependencies
└── package.json         # Node.js dependencies
```

> **Note:** The `utilities/` directory contains development tools for data management. These should **NOT** be deployed to production. Keep them local for development use only.

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
The site uses **Tailwind CSS** with **DaisyUI** for styling. 
- Source CSS: `static/css/input.css`
- Compiled CSS: `static/css/style.css`
- To rebuild CSS: `npm run build-prod` (production) or `npm run build` (dev with watch)

## Contributing

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## License

This project is part of the Mapping the Gay Guides digital history initiative.
