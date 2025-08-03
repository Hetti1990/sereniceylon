from app import app, db
from models import Currency, Destination, Hotel, Transport, Sightseeing, EntranceFee

def seed_data():
    with app.app_context():
        # Clean up existing data
        db.drop_all()
        db.create_all()

        # --- Seed Currencies ---
        usd = Currency(code='USD', exchange_rate=1.0) # Base currency
        lkr = Currency(code='LKR', exchange_rate=320.0)
        thb = Currency(code='THB', exchange_rate=36.0)
        db.session.add_all([usd, lkr, thb])
        db.session.commit()

        # --- Seed Destinations ---
        colombo = Destination(country='Sri Lanka', city='Colombo')
        bangkok = Destination(country='Thailand', city='Bangkok')
        db.session.add_all([colombo, bangkok])
        db.session.commit()

        # --- Seed Hotels ---
        galle_face = Hotel(destination_id=colombo.id, name='Galle Face Hotel', address='2 Galle Road, Colombo', rate=150.0, meal_basis='BB', room_basis='Double', room_type_validity='Standard')
        mandarin_oriental = Hotel(destination_id=bangkok.id, name='Mandarin Oriental', address='48 Oriental Ave, Bangkok', rate=250.0, meal_basis='RO', room_basis='King', room_type_validity='Deluxe')
        db.session.add_all([galle_face, mandarin_oriental])
        db.session.commit()

        # --- Seed Transport ---
        airport_transfer_lkr = Transport(destination_id=colombo.id, from_location='Airport', to_location='Galle Face Hotel', mode='Car', cost=5000.0, currency='LKR')
        tuk_tuk_bangkok = Transport(destination_id=bangkok.id, from_location='Hotel', to_location='Grand Palace', mode='Tuk Tuk', cost=200.0, currency='THB')
        db.session.add_all([airport_transfer_lkr, tuk_tuk_bangkok])
        db.session.commit()

        # --- Seed Sightseeing ---
        gangaramaya_temple = Sightseeing(destination_id=colombo.id, name='Gangaramaya Temple', description='A beautiful Buddhist temple.', is_paid=True)
        vimanmek_mansion = Sightseeing(destination_id=bangkok.id, name='Vimanmek Mansion', description='A former royal palace.', is_paid=True)
        lumpini_park = Sightseeing(destination_id=bangkok.id, name='Lumpini Park', description='A large public park.', is_paid=False)
        db.session.add_all([gangaramaya_temple, vimanmek_mansion, lumpini_park])
        db.session.commit()

        # --- Seed Entrance Fees ---
        gangaramaya_fee = EntranceFee(sightseeing_id=gangaramaya_temple.id, cost=10.0, currency='USD')
        vimanmek_fee = EntranceFee(sightseeing_id=vimanmek_mansion.id, cost=500.0, currency='THB')
        db.session.add_all([gangaramaya_fee, vimanmek_fee])
        db.session.commit()

        print("Database seeded successfully.")

if __name__ == '__main__':
    seed_data()
