import os
from flask import Flask
from flask_cors import CORS
from flask import request, jsonify
from models import db, Currency, Destination, Sightseeing, Hotel, Transport
from pricing import calculate_total_cost

app = Flask(__name__)
CORS(app)

# Database Configuration
basedir = os.path.abspath(os.path.dirname(__file__))
# Ensure the instance folder exists
instance_path = os.path.join(basedir, 'instance')
if not os.path.exists(instance_path):
    os.makedirs(instance_path)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(instance_path, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route("/")
def hello_world():
    return "Hello, World!"

# Currency CRUD
@app.route('/currency', methods=['POST'])
def add_currency():
    data = request.get_json()
    new_currency = Currency(code=data['code'], exchange_rate=data['exchange_rate'])
    db.session.add(new_currency)
    db.session.commit()
    return jsonify({'message': 'Currency added successfully'}), 201

@app.route('/currency', methods=['GET'])
def get_currencies():
    currencies = Currency.query.all()
    return jsonify([{'id': c.id, 'code': c.code, 'exchange_rate': c.exchange_rate} for c in currencies])

@app.route('/currency/<int:id>', methods=['GET'])
def get_currency(id):
    currency = Currency.query.get_or_404(id)
    return jsonify({'id': currency.id, 'code': currency.code, 'exchange_rate': currency.exchange_rate})

@app.route('/currency/<int:id>', methods=['PUT'])
def update_currency(id):
    currency = Currency.query.get_or_404(id)
    data = request.get_json()
    currency.code = data['code']
    currency.exchange_rate = data['exchange_rate']
    db.session.commit()
    return jsonify({'message': 'Currency updated successfully'})

@app.route('/currency/<int:id>', methods=['DELETE'])
def delete_currency(id):
    currency = Currency.query.get_or_404(id)
    db.session.delete(currency)
    db.session.commit()
    return jsonify({'message': 'Currency deleted successfully'})


# Destination CRUD
@app.route('/destination', methods=['POST'])
def add_destination():
    data = request.get_json()
    new_destination = Destination(country=data['country'], city=data['city'], description=data.get('description'))
    db.session.add(new_destination)
    db.session.commit()
    return jsonify({'message': 'Destination added successfully'}), 201

@app.route('/destination', methods=['GET'])
def get_destinations():
    destinations = Destination.query.all()
    return jsonify([{'id': d.id, 'country': d.country, 'city': d.city, 'description': d.description} for d in destinations])

@app.route('/destination/<int:id>', methods=['GET'])
def get_destination(id):
    destination = Destination.query.get_or_404(id)
    return jsonify({'id': destination.id, 'country': destination.country, 'city': destination.city, 'description': destination.description})

@app.route('/destination/<int:id>', methods=['PUT'])
def update_destination(id):
    destination = Destination.query.get_or_404(id)
    data = request.get_json()
    destination.country = data['country']
    destination.city = data['city']
    destination.description = data.get('description')
    db.session.commit()
    return jsonify({'message': 'Destination updated successfully'})

@app.route('/destination/<int:id>', methods=['DELETE'])
def delete_destination(id):
    destination = Destination.query.get_or_404(id)
    db.session.delete(destination)
    db.session.commit()
    return jsonify({'message': 'Destination deleted successfully'})


# Sightseeing CRUD
@app.route('/sightseeing', methods=['POST'])
def add_sightseeing():
    data = request.get_json()
    new_sightseeing = Sightseeing(
        destination_id=data['destination_id'],
        name=data['name'],
        description=data.get('description'),
        is_paid=data.get('is_paid', False)
    )
    db.session.add(new_sightseeing)
    db.session.commit()
    return jsonify({'message': 'Sightseeing added successfully'}), 201

@app.route('/sightseeing', methods=['GET'])
def get_sightseeings():
    sightseeings = Sightseeing.query.all()
    return jsonify([{'id': s.id, 'destination_id': s.destination_id, 'name': s.name, 'description': s.description, 'is_paid': s.is_paid} for s in sightseeings])

@app.route('/sightseeing/<int:id>', methods=['GET'])
def get_sightseeing(id):
    sightseeing = Sightseeing.query.get_or_404(id)
    return jsonify({'id': sightseeing.id, 'destination_id': sightseeing.destination_id, 'name': sightseeing.name, 'description': sightseeing.description, 'is_paid': sightseeing.is_paid})

@app.route('/sightseeing/<int:id>', methods=['PUT'])
def update_sightseeing(id):
    sightseeing = Sightseeing.query.get_or_404(id)
    data = request.get_json()
    sightseeing.destination_id = data['destination_id']
    sightseeing.name = data['name']
    sightseeing.description = data.get('description')
    sightseeing.is_paid = data.get('is_paid', False)
    db.session.commit()
    return jsonify({'message': 'Sightseeing updated successfully'})

@app.route('/sightseeing/<int:id>', methods=['DELETE'])
def delete_sightseeing(id):
    sightseeing = Sightseeing.query.get_or_404(id)
    db.session.delete(sightseeing)
    db.session.commit()
    return jsonify({'message': 'Sightseeing deleted successfully'})


# Hotel CRUD
@app.route('/hotel', methods=['POST'])
def add_hotel():
    data = request.get_json()
    new_hotel = Hotel(
        destination_id=data['destination_id'],
        name=data['name'],
        address=data['address'],
        rate=data['rate'],
        meal_basis=data.get('meal_basis'),
        room_basis=data.get('room_basis'),
        room_type_validity=data.get('room_type_validity')
    )
    db.session.add(new_hotel)
    db.session.commit()
    return jsonify({'message': 'Hotel added successfully'}), 201

@app.route('/hotel', methods=['GET'])
def get_hotels():
    hotels = Hotel.query.all()
    return jsonify([{'id': h.id, 'destination_id': h.destination_id, 'name': h.name, 'address': h.address, 'rate': h.rate, 'meal_basis': h.meal_basis, 'room_basis': h.room_basis, 'room_type_validity': h.room_type_validity} for h in hotels])

@app.route('/hotel/<int:id>', methods=['GET'])
def get_hotel(id):
    hotel = Hotel.query.get_or_404(id)
    return jsonify({'id': hotel.id, 'destination_id': hotel.destination_id, 'name': hotel.name, 'address': hotel.address, 'rate': hotel.rate, 'meal_basis': hotel.meal_basis, 'room_basis': hotel.room_basis, 'room_type_validity': hotel.room_type_validity})

@app.route('/hotel/<int:id>', methods=['PUT'])
def update_hotel(id):
    hotel = Hotel.query.get_or_404(id)
    data = request.get_json()
    hotel.destination_id = data['destination_id']
    hotel.name = data['name']
    hotel.address = data['address']
    hotel.rate = data['rate']
    hotel.meal_basis = data.get('meal_basis')
    hotel.room_basis = data.get('room_basis')
    hotel.room_type_validity = data.get('room_type_validity')
    db.session.commit()
    return jsonify({'message': 'Hotel updated successfully'})

@app.route('/hotel/<int:id>', methods=['DELETE'])
def delete_hotel(id):
    hotel = Hotel.query.get_or_404(id)
    db.session.delete(hotel)
    db.session.commit()
    return jsonify({'message': 'Hotel deleted successfully'})


# Transport CRUD
@app.route('/transport', methods=['POST'])
def add_transport():
    data = request.get_json()
    new_transport = Transport(
        destination_id=data['destination_id'],
        from_location=data['from_location'],
        to_location=data['to_location'],
        mode=data['mode'],
        cost=data['cost'],
        currency=data['currency']
    )
    db.session.add(new_transport)
    db.session.commit()
    return jsonify({'message': 'Transport added successfully'}), 201

@app.route('/transport', methods=['GET'])
def get_transports():
    transports = Transport.query.all()
    return jsonify([{'id': t.id, 'destination_id': t.destination_id, 'from_location': t.from_location, 'to_location': t.to_location, 'mode': t.mode, 'cost': t.cost, 'currency': t.currency} for t in transports])

@app.route('/transport/<int:id>', methods=['GET'])
def get_transport(id):
    transport = Transport.query.get_or_404(id)
    return jsonify({'id': transport.id, 'destination_id': transport.destination_id, 'from_location': transport.from_location, 'to_location': transport.to_location, 'mode': transport.mode, 'cost': transport.cost, 'currency': transport.currency})

@app.route('/transport/<int:id>', methods=['PUT'])
def update_transport(id):
    transport = Transport.query.get_or_404(id)
    data = request.get_json()
    transport.destination_id = data['destination_id']
    transport.from_location = data['from_location']
    transport.to_location = data['to_location']
    transport.mode = data['mode']
    transport.cost = data['cost']
    transport.currency = data['currency']
    db.session.commit()
    return jsonify({'message': 'Transport updated successfully'})

@app.route('/transport/<int:id>', methods=['DELETE'])
def delete_transport(id):
    transport = Transport.query.get_or_404(id)
    db.session.delete(transport)
    db.session.commit()
    return jsonify({'message': 'Transport deleted successfully'})


# Itinerary Cost Calculation
@app.route('/itinerary/calculate-cost', methods=['POST'])
def calculate_itinerary_cost():
    data = request.get_json()
    itinerary_details = data.get('itinerary_details')
    target_currency_code = data.get('target_currency_code')

    if not itinerary_details or not target_currency_code:
        return jsonify({'error': 'Missing itinerary_details or target_currency_code'}), 400

    try:
        with app.app_context():
            total_cost = calculate_total_cost(itinerary_details, target_currency_code)
        return jsonify({'total_cost': total_cost, 'currency': target_currency_code})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)
