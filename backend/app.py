from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, Location, Sightseeing

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/locations', methods=['POST'])
def add_location():
    data = request.get_json()
    new_location = Location(city=data['city'], country=data['country'])
    db.session.add(new_location)
    db.session.commit()
    return jsonify({'message': 'Location added successfully'})

@app.route('/locations', methods=['GET'])
def get_locations():
    locations = Location.query.all()
    return jsonify([{'id': loc.id, 'city': loc.city, 'country': loc.country} for loc in locations])

@app.route('/locations/<int:id>', methods=['PUT'])
def update_location(id):
    data = request.get_json()
    location = Location.query.get(id)
    location.city = data['city']
    location.country = data['country']
    db.session.commit()
    return jsonify({'message': 'Location updated successfully'})

@app.route('/locations/<int:id>', methods=['DELETE'])
def delete_location(id):
    location = Location.query.get(id)
    db.session.delete(location)
    db.session.commit()
    return jsonify({'message': 'Location deleted successfully'})

@app.route('/sightseeing', methods=['POST'])
def add_sightseeing():
    data = request.get_json()
    new_sightseeing = Sightseeing(
        location_id=data['location_id'],
        name=data['name'],
        description=data['description'],
        category=data['category']
    )
    db.session.add(new_sightseeing)
    db.session.commit()
    return jsonify({'message': 'Sightseeing added successfully'})

@app.route('/sightseeing', methods=['GET'])
def get_sightseeing():
    sightseeing = Sightseeing.query.all()
    return jsonify([{'id': s.id, 'location_id': s.location_id, 'name': s.name, 'description': s.description, 'category': s.category} for s in sightseeing])

@app.route('/sightseeing/<int:id>', methods=['PUT'])
def update_sightseeing(id):
    data = request.get_json()
    sightseeing = Sightseeing.query.get(id)
    sightseeing.location_id = data['location_id']
    sightseeing.name = data['name']
    sightseeing.description = data['description']
    sightseeing.category = data['category']
    db.session.commit()
    return jsonify({'message': 'Sightseeing updated successfully'})

@app.route('/sightseeing/<int:id>', methods=['DELETE'])
def delete_sightseeing(id):
    sightseeing = Sightseeing.query.get(id)
    db.session.delete(sightseeing)
    db.session.commit()
    return jsonify({'message': 'Sightseeing deleted successfully'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
