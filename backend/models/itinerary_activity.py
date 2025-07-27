from .base import db

class ItineraryActivity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    itinerary_id = db.Column(db.Integer, db.ForeignKey('itinerary.id'), nullable=False)
    sight_id = db.Column(db.Integer, db.ForeignKey('sightseeing.id'), nullable=True)
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotel.id'), nullable=True)
    transport_id = db.Column(db.Integer, db.ForeignKey('transport.id'), nullable=True)
    entrance_fee = db.Column(db.Float, nullable=True)
    pax = db.Column(db.Integer, nullable=True)
