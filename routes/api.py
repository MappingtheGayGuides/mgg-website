from flask import Blueprint, jsonify, request
from models import db, Location, UniqueLocation, LocationType, AmenityFeature

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

@bp.route('/unique-locations')
def get_unique_locations():
    """Get all unique locations for the map (no duplicates)"""
    unique_locations = UniqueLocation.query.all()
    return jsonify([loc.to_dict() for loc in unique_locations])

@bp.route('/unique-locations/<int:location_id>')
def get_unique_location(location_id):
    """Get a specific unique location"""
    unique_location = UniqueLocation.query.get_or_404(location_id)
    return jsonify(unique_location.to_dict())

@bp.route('/location-types')
def get_location_types():
    """Get all location types"""
    types = LocationType.query.all()
    return jsonify([type_obj.to_dict() for type_obj in types])

@bp.route('/amenity-features')
def get_amenity_features():
    """Get all amenity features"""
    features = AmenityFeature.query.all()
    return jsonify([feature.to_dict() for feature in features])


