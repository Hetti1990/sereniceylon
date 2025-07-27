from .base import db

class ItineraryTemplate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    destinations = db.Column(db.JSON, nullable=False)
    activities = db.Column(db.JSON, nullable=False)
    accommodations = db.Column(db.JSON, nullable=False)
    meals = db.Column(db.JSON, nullable=True)
