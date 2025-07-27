from flask import Flask, jsonify, request
from flask_cors import CORS
from models import db, Itinerary, ItineraryTemplate

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)

@app.route('/itineraries', methods=['GET', 'POST'])
def handle_itineraries():
    if request.method == 'POST':
        data = request.get_json()
        new_itinerary = Itinerary(
            title=data['title'],
            description=data.get('description'),
            duration_days=data['duration_days'],
            destinations=data['destinations'],
            activities=data['activities'],
            accommodations=data['accommodations'],
            meals=data.get('meals'),
            is_group_package=data.get('is_group_package', False),
            template_id=data.get('template_id')
        )
        db.session.add(new_itinerary)
        db.session.commit()
        return jsonify({'message': 'Itinerary created successfully'}), 201
    elif request.method == 'GET':
        itineraries = Itinerary.query.all()
        return jsonify([itinerary.__dict__ for itinerary in itineraries])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
