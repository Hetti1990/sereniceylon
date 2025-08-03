from app import app, db
from models import Currency, Destination, Hotel, Sightseeing

def seed_data():
    with app.app_context():
        # Drop all tables and recreate them
        db.drop_all()
        db.create_all()

        # Seed Currencies
        usd = Currency(code='USD', exchange_rate=1.0)
        lkr = Currency(code='LKR', exchange_rate=320.0)
        thb = Currency(code='THB', exchange_rate=36.0)
        db.session.add_all([usd, lkr, thb])
        db.session.commit()

        # Seed Destinations
        maldives = Destination(country='Maldives', city='Malé', description='A tropical nation in the Indian Ocean.', currency_code='USD')
        sri_lanka = Destination(country='Sri Lanka', city='Colombo', description='An island country in South Asia.', currency_code='LKR')
        thailand = Destination(country='Thailand', city='Bangkok', description='A Southeast Asian country.', currency_code='THB')
        db.session.add_all([maldives, sri_lanka, thailand])
        db.session.commit()

        # Seed Hotels
        hotel1 = Hotel(destination_id=maldives.id, name='Maldives Resort', address='123 Ocean View', rate=500.0, currency='USD')
        hotel2 = Hotel(destination_id=sri_lanka.id, name='Colombo Grand', address='456 Galle Road', rate=15000.0, currency='LKR')
        hotel3 = Hotel(destination_id=thailand.id, name='Bangkok Palace', address='789 Sukhumvit Road', rate=3000.0, currency='THB')
        db.session.add_all([hotel1, hotel2, hotel3])

        # Seed Sightseeing
        sight1 = Sightseeing(destination_id=maldives.id, name='Scuba Diving', description='Explore the coral reefs.', is_paid=True, cost=150.0)
        sight2 = Sightseeing(destination_id=sri_lanka.id, name='Galle Fort', description='A historic fortress.', is_paid=False)
        sight3 = Sightseeing(destination_id=thailand.id, name='Grand Palace', description='A complex of buildings at the heart of Bangkok.', is_paid=True, cost=500.0)
        db.session.add_all([sight1, sight2, sight3])

        db.session.commit()
        print("Database seeded!")

if __name__ == '__main__':
    seed_data()
