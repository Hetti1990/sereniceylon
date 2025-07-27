from .base import db

class Currency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True, nullable=False)
    exchange_rate = db.Column(db.Float, nullable=False)
