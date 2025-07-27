from .base import db

class Itinerary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    duration_days = db.Column(db.Integer, nullable=False)
    destinations = db.Column(db.JSON, nullable=False)  # Store a list of destination IDs
    activities = db.Column(db.JSON, nullable=False)  # Store a list of activity objects
    accommodations = db.Column(db.JSON, nullable=False)  # Store a list of accommodation objects
    meals = db.Column(db.JSON, nullable=True)  # Store a list of meal objects
    is_group_package = db.Column(db.Boolean, default=False)
    template_id = db.Column(db.Integer, db.ForeignKey('itinerary_template.id'), nullable=True)
