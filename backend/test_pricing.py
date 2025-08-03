import unittest
import os
from app import app, db
from models import Currency, Destination, Hotel, Transport, Sightseeing, EntranceFee
from pricing import calculate_total_cost
from seed_data import seed_data

class PricingTestCase(unittest.TestCase):
    def setUp(self):
        """Set up a new app context and a blank database for each test."""
        self.app = app
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        seed_data()

    def tearDown(self):
        """Clean up the database and app context after each test."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_simple_itinerary_usd(self):
        """Test a simple itinerary with all costs calculated in USD."""
        itinerary_details = {
            "hotels": [{"id": 1, "nights": 2}],
            "transports": [],
            "sightseeing": [{"id": 1, "pax": 2, "include_entrance_fee": True}],
            "pax": 2
        }
        total_cost = calculate_total_cost(itinerary_details, 'USD')
        # Hotel: 150 * 2 = 300
        # Sightseeing: 10 * 2 = 20
        # Total: 320
        self.assertAlmostEqual(total_cost, 320.0)

    def test_multi_currency_itinerary_lkr(self):
        """Test an itinerary with costs in different currencies, converted to LKR."""
        itinerary_details = {
            "hotels": [{"id": 2, "nights": 1}], # Mandarin Oriental, $250
            "transports": [{"id": 2}], # Tuk Tuk, 200 THB
            "sightseeing": [{"id": 2, "pax": 1, "include_entrance_fee": True}], # Vimanmek, 500 THB
            "pax": 1
        }
        total_cost = calculate_total_cost(itinerary_details, 'LKR')
        # Hotel: 250 USD -> 250 * 320 = 80000 LKR
        # Transport: 200 THB -> (200 / 36) * 320 = 1777.77 LKR
        # Sightseeing: 500 THB -> (500 / 36) * 320 = 4444.44 LKR
        # Total: 80000 + 1777.77 + 4444.44 = 86222.21
        self.assertAlmostEqual(total_cost, 86222.22, places=2)

    def test_itinerary_with_free_sightseeing(self):
        """Test an itinerary that includes a free sightseeing activity."""
        itinerary_details = {
            "hotels": [{"id": 1, "nights": 1}], # Galle Face, $150
            "sightseeing": [{"id": 3, "pax": 2, "include_entrance_fee": True}], # Lumpini Park (free)
            "pax": 2
        }
        total_cost = calculate_total_cost(itinerary_details, 'USD')
        # Hotel: 150 * 1 = 150
        # Sightseeing: 0
        # Total: 150
        self.assertAlmostEqual(total_cost, 150.0)

    def test_invalid_currency(self):
        """Test that a ValueError is raised for an invalid currency code."""
        itinerary_details = {}
        with self.assertRaises(ValueError):
            calculate_total_cost(itinerary_details, 'XYZ')

    def test_empty_itinerary(self):
        """Test that an empty itinerary has a total cost of zero."""
        itinerary_details = {}
        total_cost = calculate_total_cost(itinerary_details, 'USD')
        self.assertAlmostEqual(total_cost, 0.0)

if __name__ == '__main__':
    unittest.main()
