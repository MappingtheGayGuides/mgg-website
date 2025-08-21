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
