from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/amandaregan/Dropbox/MappingGayGuides/MGG-Site/mgg.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy()

# Initialize the app with extensions FIRST
db.init_app(app)

# Import models to register them with SQLAlchemy
from models import Location, UniqueLocation, LocationType, AmenityFeature, LocationTypeAssignment, LocationAmenityAssignment

# Import routes after db initialization to avoid circular imports
from routes import main, api

# Register blueprints
app.register_blueprint(main.bp)
app.register_blueprint(api.bp, url_prefix='/api')

def ensure_database_exists():
    """Ensure the database exists"""
    if not os.path.exists('mgg.db'):
        print("Database not found. Please run create_database.py first!")
        return False
    print("Database found and ready!")
    return True

if __name__ == '__main__':
    ensure_database_exists()
    app.run(debug=True, port=5001)
