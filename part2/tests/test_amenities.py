import unittest
from app import create_app

class AmenityApiTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app().test_client()

    def test_create_list_amenity(self):
        res = self.app.post('/api/v1/amenities', json={"name": "WiFi"})
        self.assertEqual(res.status_code, 201)
        res = self.app.get('/api/v1/amenities')
        self.assertEqual(res.status_code, 200)
        self.assertTrue(any(a['name'] == 'WiFi' for a in res.get_json()))

if __name__ == '__main__':
    unittest.main()
