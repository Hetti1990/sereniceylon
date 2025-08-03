import unittest
import json
from app import app, db
from models import Transport, Destination

class TransportTestCase(unittest.TestCase):

    def setUp(self):
        """Set up a new test client and configure the app for testing."""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()
            # Add some test destinations
            maldives = Destination(country='Maldives', city='Malé')
            sri_lanka = Destination(country='Sri Lanka', city='Colombo')
            thailand = Destination(country='Thailand', city='Bangkok')
            db.session.add_all([maldives, sri_lanka, thailand])
            db.session.commit()
            self.maldives_id = maldives.id
            self.sri_lanka_id = sri_lanka.id
            self.thailand_id = thailand.id

    def tearDown(self):
        """Clean up the database after each test."""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_add_transport_thailand(self):
        """Test adding a valid transport for Thailand."""
        res = self.app.post('/transport',
                            data=json.dumps({
                                'destination_id': self.thailand_id,
                                'from_location': 'Airport',
                                'to_location': 'Hotel',
                                'mode': 'Car',
                                'trip_cost': 1000,
                                'currency': 'THB',
                                'pricing_model': 'trip'
                            }),
                            content_type='application/json')
        self.assertEqual(res.status_code, 201)
        data = json.loads(res.data)
        self.assertEqual(data['message'], 'Transport added successfully')

    def test_add_transport_maldives(self):
        """Test adding a valid transport for Maldives."""
        res = self.app.post('/transport',
                            data=json.dumps({
                                'destination_id': self.maldives_id,
                                'from_location': 'Airport',
                                'to_location': 'Resort',
                                'mode': 'Sea Plane',
                                'per_person_cost': 450,
                                'currency': 'USD',
                                'pricing_model': 'per_person'
                            }),
                            content_type='application/json')
        self.assertEqual(res.status_code, 201)
        data = json.loads(res.data)
        self.assertEqual(data['message'], 'Transport added successfully')

    def test_add_transport_maldives_invalid_mode(self):
        """Test adding a transport for Maldives with an invalid mode."""
        res = self.app.post('/transport',
                            data=json.dumps({
                                'destination_id': self.maldives_id,
                                'from_location': 'Airport',
                                'to_location': 'Resort',
                                'mode': 'Car',
                                'per_person_cost': 450,
                                'currency': 'USD',
                                'pricing_model': 'per_person'
                            }),
                            content_type='application/json')
        self.assertEqual(res.status_code, 400)
        data = json.loads(res.data)
        self.assertEqual(data['error'], "Invalid transport mode for Maldives. Must be 'Speed Boat' or 'Sea Plane'.")

    def test_add_transport_maldives_invalid_pricing(self):
        """Test adding a transport for Maldives with an invalid pricing model."""
        res = self.app.post('/transport',
                            data=json.dumps({
                                'destination_id': self.maldives_id,
                                'from_location': 'Airport',
                                'to_location': 'Resort',
                                'mode': 'Sea Plane',
                                'trip_cost': 450,
                                'currency': 'USD',
                                'pricing_model': 'trip'
                            }),
                            content_type='application/json')
        self.assertEqual(res.status_code, 400)
        data = json.loads(res.data)
        self.assertEqual(data['error'], "Invalid pricing model for Maldives. Must be 'per_person'.")

    def test_get_all_transport(self):
        """Test getting all transport routes."""
        # First, add a transport to the database
        self.app.post('/transport',
                      data=json.dumps({
                          'destination_id': self.thailand_id,
                          'from_location': 'Airport',
                          'to_location': 'Hotel',
                          'mode': 'Car',
                          'trip_cost': 1000,
                          'currency': 'THB',
                          'pricing_model': 'trip'
                      }),
                      content_type='application/json')

        res = self.app.get('/transport')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(len(data), 1)

    def test_update_transport(self):
        """Test updating a transport route."""
        # Add a transport first
        res = self.app.post('/transport',
                            data=json.dumps({
                                'destination_id': self.thailand_id,
                                'from_location': 'Airport',
                                'to_location': 'Hotel',
                                'mode': 'Car',
                                'trip_cost': 1000,
                                'currency': 'THB',
                                'pricing_model': 'trip'
                            }),
                            content_type='application/json')
        transport_id = json.loads(res.data)['id']

        # Now update it
        res = self.app.put(f'/transport/{transport_id}',
                           data=json.dumps({'trip_cost': 1200}),
                           content_type='application/json')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['message'], 'Transport updated successfully')

    def test_delete_transport(self):
        """Test deleting a transport route."""
        # Add a transport first
        res = self.app.post('/transport',
                            data=json.dumps({
                                'destination_id': self.thailand_id,
                                'from_location': 'Airport',
                                'to_location': 'Hotel',
                                'mode': 'Car',
                                'trip_cost': 1000,
                                'currency': 'THB',
                                'pricing_model': 'trip'
                            }),
                            content_type='application/json')
        transport_id = json.loads(res.data)['id']

        # Now delete it
        res = self.app.delete(f'/transport/{transport_id}')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['message'], 'Transport deleted successfully')

    def test_get_transport_by_destination(self):
        """Test getting transport routes for a specific destination."""
        # Add a transport for Thailand
        self.app.post('/transport',
                      data=json.dumps({
                          'destination_id': self.thailand_id,
                          'from_location': 'Airport',
                          'to_location': 'Hotel',
                          'mode': 'Car',
                          'trip_cost': 1000,
                          'currency': 'THB',
                          'pricing_model': 'trip'
                      }),
                      content_type='application/json')

        # Add a transport for Maldives
        self.app.post('/transport',
                      data=json.dumps({
                          'destination_id': self.maldives_id,
                          'from_location': 'Airport',
                          'to_location': 'Resort',
                          'mode': 'Sea Plane',
                          'per_person_cost': 450,
                          'currency': 'USD',
                          'pricing_model': 'per_person'
                      }),
                      content_type='application/json')

        res = self.app.get(f'/transport/destination/{self.thailand_id}')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['destination_id'], self.thailand_id)

if __name__ == "__main__":
    unittest.main()
