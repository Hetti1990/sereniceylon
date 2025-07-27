from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': self.role,
        }

class Destination(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'country': self.country,
            'city': self.city,
            'description': self.description,
        }

class Sightseeing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    destination_id = db.Column(db.Integer, db.ForeignKey('destination.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    is_paid = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'destination_id': self.destination_id,
            'name': self.name,
            'description': self.description,
            'is_paid': self.is_paid,
        }

class Hotel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    destination_id = db.Column(db.Integer, db.ForeignKey('destination.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    rate = db.Column(db.Float, nullable=False)
    meal_basis = db.Column(db.String(100), nullable=True)
    room_basis = db.Column(db.String(100), nullable=True)
    room_type_validity = db.Column(db.String(100), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'destination_id': self.destination_id,
            'name': self.name,
            'address': self.address,
            'rate': self.rate,
            'meal_basis': self.meal_basis,
            'room_basis': self.room_basis,
            'room_type_validity': self.room_type_validity,
        }

class Transport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    destination_id = db.Column(db.Integer, db.ForeignKey('destination.id'), nullable=False)
    from_location = db.Column(db.String(100), nullable=False)
    to_location = db.Column(db.String(100), nullable=False)
    mode = db.Column(db.String(100), nullable=False)
    cost = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(10), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'destination_id': self.destination_id,
            'from_location': self.from_location,
            'to_location': self.to_location,
            'mode': self.mode,
            'cost': self.cost,
            'currency': self.currency,
        }

class Itinerary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    destination_id = db.Column(db.Integer, db.ForeignKey('destination.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    total_cost = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'destination_id': self.destination_id,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat(),
            'total_cost': self.total_cost,
        }

class ItineraryDay(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    itinerary_id = db.Column(db.Integer, db.ForeignKey('itinerary.id'), nullable=False)
    day_number = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'itinerary_id': self.itinerary_id,
            'day_number': self.day_number,
            'description': self.description,
        }

class ItineraryActivity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day_id = db.Column(db.Integer, db.ForeignKey('itinerary_day.id'), nullable=False)
    sight_id = db.Column(db.Integer, db.ForeignKey('sightseeing.id'), nullable=True)
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotel.id'), nullable=True)
    transport_id = db.Column(db.Integer, db.ForeignKey('transport.id'), nullable=True)
    entrance_fee = db.Column(db.Float, nullable=True)
    pax = db.Column(db.Integer, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'day_id': self.day_id,
            'sight_id': self.sight_id,
            'hotel_id': self.hotel_id,
            'transport_id': self.transport_id,
            'entrance_fee': self.entrance_fee,
            'pax': self.pax,
        }

class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    destination_id = db.Column(db.Integer, db.ForeignKey('destination.id'), nullable=True)
    activity_id = db.Column(db.Integer, db.ForeignKey('itinerary_activity.id'), nullable=True)
    image_url = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'destination_id': self.destination_id,
            'activity_id': self.activity_id,
            'image_url': self.image_url,
            'description': self.description,
        }

class Pricing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    itinerary_id = db.Column(db.Integer, db.ForeignKey('itinerary.id'), nullable=False)
    item_type = db.Column(db.String(100), nullable=False)
    cost = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(10), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'itinerary_id': self.itinerary_id,
            'item_type': self.item_type,
            'cost': self.cost,
            'currency': self.currency,
        }

class Currency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True, nullable=False)
    exchange_rate = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'exchange_rate': self.exchange_rate,
        }
