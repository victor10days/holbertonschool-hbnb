import unittest
from app import create_app

class PlaceApiTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app().test_client()
        # seed a user + amenity
        u = self.app.post('/api/v1/users', json={
            "email": "x@y.com", "password": "pw", "first_name": "X", "last_name": "Y"
        }).get_json()
        self.user_id = u['id']
        a = self.app.post('/api/v1/amenities', json={"name": "AC"}).get_json()
        self.amenity_id = a['id']

    def test_place_crud(self):
        res = self.app.post('/api/v1/places', json={
            "name": "Loft", "description": "Cozy", "price": 100,
            "latitude": 18.4, "longitude": -66.1,
            "owner_id": self.user_id, "amenity_ids": [self.amenity_id]
        })
        self.assertEqual(res.status_code, 201)
        place = res.get_json()
        pid = place['id']
        self.assertIn('owner', place)
        self.assertIn('amenities', place)

        res = self.app.put(f'/api/v1/places/{pid}', json={"price": 120})
        self.assertEqual(res.status_code, 200)

if __name__ == '__main__':
    unittest.main()
