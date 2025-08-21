from flask import Blueprint, jsonify, request
from models import db, Location, Article

bp = Blueprint('api', __name__)

@bp.route('/locations')
def get_locations():
    """Get all locations for the map"""
    # TODO: Add filtering and pagination
    locations = Location.query.all()
    return jsonify([location.to_dict() for location in locations])

@bp.route('/locations/<int:location_id>')
def get_location(location_id):
    """Get a specific location"""
    location = Location.query.get_or_404(location_id)
    return jsonify(location.to_dict())

@bp.route('/articles')
def get_articles():
    """Get all articles"""
    articles = Article.query.all()
    return jsonify([article.to_dict() for article in articles])

@bp.route('/articles/<int:article_id>')
def get_article(article_id):
    """Get a specific article"""
    article = Article.query.get_or_404(article_id)
    return jsonify(article.to_dict())
