from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, Transport, Destination

app = Flask(__name__)
CORS(app)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)

# Create the database tables
with app.app_context():
    db.create_all()

# API Endpoints for Transport Management

@app.route("/transport", methods=["POST"])
def add_transport():
    data = request.get_json()

    # Basic validation
    required_fields = ['destination_id', 'from_location', 'to_location', 'mode', 'currency']
    if not data or not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    destination = Destination.query.get(data['destination_id'])
    if not destination:
        return jsonify({"error": "Destination not found"}), 404

    # Destination-specific logic
    pricing_model = data.get('pricing_model', 'trip')
    if destination.country == 'Maldives':
        if data['mode'] not in ['Speed Boat', 'Sea Plane']:
            return jsonify({"error": "Invalid transport mode for Maldives. Must be 'Speed Boat' or 'Sea Plane'."}), 400
        if pricing_model != 'per_person':
            return jsonify({"error": "Invalid pricing model for Maldives. Must be 'per_person'."}), 400
        if not data.get('per_person_cost'):
            return jsonify({"error": "Missing 'per_person_cost' for Maldives."}), 400
    elif destination.country in ['Sri Lanka', 'Thailand']:
        if pricing_model != 'trip':
            return jsonify({"error": "Invalid pricing model for Sri Lanka/Thailand. Must be 'trip'."}), 400
        if not data.get('trip_cost'):
            return jsonify({"error": "Missing 'trip_cost' for Sri Lanka/Thailand."}), 400

    new_transport = Transport(
        destination_id=data['destination_id'],
        from_location=data['from_location'],
        to_location=data['to_location'],
        mode=data['mode'],
        distance=data.get('distance'),
        pricing_model=pricing_model,
        trip_cost=data.get('trip_cost'),
        per_person_cost=data.get('per_person_cost'),
        currency=data['currency'],
        driver_bata=data.get('driver_bata')
    )

    db.session.add(new_transport)
    db.session.commit()

    return jsonify({"message": "Transport added successfully", "id": new_transport.id}), 201

@app.route("/transport", methods=["GET"])
def get_all_transport():
    transports = Transport.query.all()
    return jsonify([
        {
            "id": t.id,
            "destination_id": t.destination_id,
            "from_location": t.from_location,
            "to_location": t.to_location,
            "mode": t.mode,
            "distance": t.distance,
            "pricing_model": t.pricing_model,
            "trip_cost": t.trip_cost,
            "per_person_cost": t.per_person_cost,
            "currency": t.currency,
            "driver_bata": t.driver_bata
        } for t in transports
    ])

@app.route("/transport/<int:id>", methods=["PUT"])
def update_transport(id):
    transport = Transport.query.get(id)
    if not transport:
        return jsonify({"error": "Transport not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    destination_id = data.get('destination_id', transport.destination_id)
    destination = Destination.query.get(destination_id)
    if not destination:
        return jsonify({"error": "Destination not found"}), 404

    # Destination-specific logic
    mode = data.get('mode', transport.mode)
    pricing_model = data.get('pricing_model', transport.pricing_model)

    if destination.country == 'Maldives':
        if mode not in ['Speed Boat', 'Sea Plane']:
            return jsonify({"error": "Invalid transport mode for Maldives. Must be 'Speed Boat' or 'Sea Plane'."}), 400
        if pricing_model != 'per_person':
            return jsonify({"error": "Invalid pricing model for Maldives. Must be 'per_person'."}), 400
        if 'per_person_cost' in data and not data.get('per_person_cost'):
            return jsonify({"error": "Missing 'per_person_cost' for Maldives."}), 400
    elif destination.country in ['Sri Lanka', 'Thailand']:
        if pricing_model != 'trip':
            return jsonify({"error": "Invalid pricing model for Sri Lanka/Thailand. Must be 'trip'."}), 400
        if 'trip_cost' in data and not data.get('trip_cost'):
            return jsonify({"error": "Missing 'trip_cost' for Sri Lanka/Thailand."}), 400

    transport.destination_id = data.get('destination_id', transport.destination_id)
    transport.from_location = data.get('from_location', transport.from_location)
    transport.to_location = data.get('to_location', transport.to_location)
    transport.mode = mode
    transport.distance = data.get('distance', transport.distance)
    transport.pricing_model = pricing_model
    transport.trip_cost = data.get('trip_cost', transport.trip_cost)
    transport.per_person_cost = data.get('per_person_cost', transport.per_person_cost)
    transport.currency = data.get('currency', transport.currency)
    transport.driver_bata = data.get('driver_bata', transport.driver_bata)

    db.session.commit()

    return jsonify({"message": "Transport updated successfully"})

@app.route("/transport/<int:id>", methods=["DELETE"])
def delete_transport(id):
    transport = Transport.query.get(id)
    if not transport:
        return jsonify({"error": "Transport not found"}), 404

    db.session.delete(transport)
    db.session.commit()

    return jsonify({"message": "Transport deleted successfully"})

@app.route("/transport/destination/<int:destination_id>", methods=["GET"])
def get_transport_by_destination(destination_id):
    transports = Transport.query.filter_by(destination_id=destination_id).all()
    if not transports:
        return jsonify({"error": "No transport found for this destination"}), 404

    return jsonify([
        {
            "id": t.id,
            "destination_id": t.destination_id,
            "from_location": t.from_location,
            "to_location": t.to_location,
            "mode": t.mode,
            "distance": t.distance,
            "pricing_model": t.pricing_model,
            "trip_cost": t.trip_cost,
            "per_person_cost": t.per_person_cost,
            "currency": t.currency,
            "driver_bata": t.driver_bata
        } for t in transports
    ])

@app.route("/")
def hello_world():
    return "Hello, World!"

if __name__ == "__main__":
    app.run(debug=True)
