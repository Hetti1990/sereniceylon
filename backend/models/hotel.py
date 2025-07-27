from .base import db

class Hotel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    destination_id = db.Column(db.Integer, db.ForeignKey('destination.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    rate = db.Column(db.Float, nullable=False)
    meal_basis = db.Column(db.String(100), nullable=True)
    room_basis = db.Column(db.String(100), nullable=True)
    room_type_validity = db.Column(db.String(100), nullable=True)
