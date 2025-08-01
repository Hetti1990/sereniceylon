from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, Hotel, Rate

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route("/")
def hello_world():
    return "Hello, World!"

@app.route("/hotels", methods=["GET", "POST"])
def handle_hotels():
    if request.method == "POST":
        data = request.get_json()
        new_hotel = Hotel(
            name=data['name'],
            location=data['location'],
            meal_basis=data.get('meal_basis'),
            room_basis=data.get('room_basis'),
            room_type_validity=data.get('room_type_validity')
        )
        db.session.add(new_hotel)
        db.session.commit()
        for rate_data in data.get('rates', []):
            new_rate = Rate(
                hotel_id=new_hotel.id,
                pax=rate_data['pax'],
                rate=rate_data['rate']
            )
            db.session.add(new_rate)
        db.session.commit()
        return jsonify({"message": "Hotel added successfully"}), 201
    else:
        hotels = Hotel.query.all()
        return jsonify([
            {
                "id": hotel.id,
                "name": hotel.name,
                "location": hotel.location,
                "meal_basis": hotel.meal_basis,
                "room_basis": hotel.room_basis,
                "room_type_validity": hotel.room_type_validity,
                "rates": [{"pax": rate.pax, "rate": rate.rate} for rate in hotel.rates]
            } for hotel in hotels
        ])

@app.route("/hotels/<int:id>", methods=["GET", "PUT", "DELETE"])
def handle_hotel(id):
    hotel = Hotel.query.get_or_404(id)
    if request.method == "GET":
        return jsonify({
            "id": hotel.id,
            "name": hotel.name,
            "location": hotel.location,
            "meal_basis": hotel.meal_basis,
            "room_basis": hotel.room_basis,
            "room_type_validity": hotel.room_type_validity,
            "rates": [{"pax": rate.pax, "rate": rate.rate} for rate in hotel.rates]
        })
    elif request.method == "PUT":
        data = request.get_json()
        hotel.name = data.get('name', hotel.name)
        hotel.location = data.get('location', hotel.location)
        hotel.meal_basis = data.get('meal_basis', hotel.meal_basis)
        hotel.room_basis = data.get('room_basis', hotel.room_basis)
        hotel.room_type_validity = data.get('room_type_validity', hotel.room_type_validity)

        if 'rates' in data:
            Rate.query.filter_by(hotel_id=id).delete()
            for rate_data in data['rates']:
                new_rate = Rate(
                    hotel_id=id,
                    pax=rate_data['pax'],
                    rate=rate_data['rate']
                )
                db.session.add(new_rate)

        db.session.commit()
        return jsonify({"message": "Hotel updated successfully"})
    elif request.method == "DELETE":
        Rate.query.filter_by(hotel_id=id).delete()
        db.session.delete(hotel)
        db.session.commit()
        return jsonify({"message": "Hotel deleted successfully"})

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
