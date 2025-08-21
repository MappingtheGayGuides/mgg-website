from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mgg.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy()

# Import routes after db initialization to avoid circular imports
from routes import main, api

# Register blueprints
app.register_blueprint(main.bp)
app.register_blueprint(api.bp, url_prefix='/api')

# Initialize the app with extensions
db.init_app(app)

def ensure_database_exists():
    """Ensure the database and tables exist"""
    with app.app_context():
        if not os.path.exists('mgg.db'):
            print("Database not found. Creating tables...")
            db.create_all()
            print("Database tables created successfully!")

if __name__ == '__main__':
    ensure_database_exists()
    app.run(debug=True)
