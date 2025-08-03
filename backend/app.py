import os
from flask import Flask, jsonify
from flask_cors import CORS
from models import db, Destination, Hotel, Sightseeing

app = Flask(__name__)
CORS(app)

# Absolute path to the database
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance', 'database.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route("/destinations", methods=['GET'])
def get_destinations():
    destinations = Destination.query.all()
    return jsonify([{
        'id': d.id,
        'country': d.country,
        'city': d.city,
        'description': d.description,
        'currency_code': d.currency_code
    } for d in destinations])

@app.route("/destinations/<int:id>", methods=['GET'])
def get_destination(id):
    destination = Destination.query.get_or_404(id)
    hotels = Hotel.query.filter_by(destination_id=id).all()
    sights = Sightseeing.query.filter_by(destination_id=id).all()

    return jsonify({
        'id': destination.id,
        'country': destination.country,
        'city': destination.city,
        'description': destination.description,
        'currency_code': destination.currency_code,
        'hotels': [{
            'id': h.id,
            'name': h.name,
            'rate': h.rate,
            'currency': h.currency
        } for h in hotels],
        'sightseeing': [{
            'id': s.id,
            'name': s.name,
            'is_paid': s.is_paid,
            'cost': s.cost
        } for s in sights]
    })

if __name__ == "__main__":
    app.run(debug=True, port=5001) # Use a different port to avoid conflict with frontend
