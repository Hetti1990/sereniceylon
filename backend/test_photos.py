import unittest
import os
import tempfile
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.app import app, db

class PhotoTestCase(unittest.TestCase):
    def setUp(self):
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        self.client = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])

    def test_get_photos(self):
        response = self.client.get('/api/photos')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
