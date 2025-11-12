from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class UniqueLocation(db.Model):
    """Model for standardized unique locations with coordinates"""
    __tablename__ = 'unique_locations'
    
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    city = db.Column(db.String(100))
    state = db.Column(db.String(50))
    address_precision = db.Column(db.String(50), default='general')  # exact, approximate, general
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to locations
    locations = db.relationship('Location', backref='unique_location', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'city': self.city,
            'state': self.state,
            'address_precision': self.address_precision
        }

class LocationType(db.Model):
    """Model for location types (e.g., Bar, Restaurant, Hotel)"""
    __tablename__ = 'location_types'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Many-to-many relationship with locations
    locations = db.relationship('Location', secondary='location_type_assignments', backref='types')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }

class AmenityFeature(db.Model):
    """Model for amenity features (e.g., Dance Floor, Pool Table, Drag Shows)"""
    __tablename__ = 'amenity_features'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    description = db.Column(db.Text)
    short_description = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Many-to-many relationship with locations
    locations = db.relationship('Location', secondary='location_amenity_assignments', backref='amenities')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'short_description': self.short_description
        }

class LocationTypeAssignment(db.Model):
    """Association table for locations and types (many-to-many)"""
    __tablename__ = 'location_type_assignments'
    
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('location_types.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('location_id', 'type_id'),)

class LocationAmenityAssignment(db.Model):
    """Association table for locations and amenity features (many-to-many)"""
    __tablename__ = 'location_amenity_assignments'
    
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)
    amenity_id = db.Column(db.Integer, db.ForeignKey('amenity_features.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('location_id', 'amenity_id'),)

class Location(db.Model):
    """Model for locations from the gay guides CSV"""
    __tablename__ = 'locations'
    
    id = db.Column(db.Integer, primary_key=True)
    unique_id = db.Column(db.String(100), unique=True, nullable=False)  # from CSV: "d-2003-00001"
    title = db.Column(db.String(500))
    description = db.Column(db.Text)
    street_address = db.Column(db.String(500))
    city = db.Column(db.String(100))
    state = db.Column(db.String(50))
    year = db.Column(db.Integer)
    notes = db.Column(db.Text)
    full_address = db.Column(db.String(500))
    latitude = db.Column(db.Float)  # original CSV coordinates
    longitude = db.Column(db.Float)  # original CSV coordinates
    geo_address = db.Column(db.String(500))
    unclear_address = db.Column(db.String(10))  # from CSV
    status = db.Column(db.String(200))  # from CSV "status" column
    unique_location_id = db.Column(db.Integer, db.ForeignKey('unique_locations.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'unique_id': self.unique_id,
            'title': self.title,
            'description': self.description,
            'street_address': self.street_address,
            'city': self.city,
            'state': self.state,
            'year': self.year,
            'notes': self.notes,
            'full_address': self.full_address,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'geo_address': self.geo_address,
            'unclear_address': self.unclear_address,
            'status': self.status,
            'unique_location_id': self.unique_location_id
        }
    
    def __repr__(self):
        return f'<Location {self.id}: {self.title}>'

class SplitLogging(db.Model):
    """Model for tracking amenity split operations"""
    __tablename__ = 'split_logging'
    
    id = db.Column(db.Integer, primary_key=True)
    source_amenity_id = db.Column(db.Integer)
    source_amenity_name = db.Column(db.String(200))
    operation_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    operation_type = db.Column(db.String(50))  # 'split', 'delete', etc.
    target_amenities = db.Column(db.Text)  # JSON string
    locations_processed = db.Column(db.Integer, default=0)
    locations_reassigned = db.Column(db.Integer, default=0)
    locations_unassigned = db.Column(db.Integer, default=0)
    source_removed = db.Column(db.Boolean, default=False)
    user_notes = db.Column(db.Text)
    operation_status = db.Column(db.String(50))  # 'success', 'failed'
    error_message = db.Column(db.Text)
    execution_time_ms = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class SplitLocationDetail(db.Model):
    """Model for detailed logging of location reassignments during splits"""
    __tablename__ = 'split_location_details'
    
    id = db.Column(db.Integer, primary_key=True)
    split_log_id = db.Column(db.Integer, db.ForeignKey('split_logging.id'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)
    location_title = db.Column(db.String(500))
    location_city = db.Column(db.String(100))
    location_state = db.Column(db.String(50))
    location_year = db.Column(db.Integer)
    old_amenity_id = db.Column(db.Integer)
    old_amenity_name = db.Column(db.String(200))
    new_amenity_id = db.Column(db.Integer)
    new_amenity_name = db.Column(db.String(200))
    reassignment_type = db.Column(db.String(50))  # 'manual', 'deleted', etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)