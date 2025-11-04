import unittest
from app import create_app

class ReviewApiTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app().test_client()
        # seed data
        u = self.app.post('/api/v1/users', json={
            "email": "r@t.com", "password": "pw", "first_name": "R", "last_name": "T"
        }).get_json()
        a = self.app.post('/api/v1/amenities', json={"name": "Pool"}).get_json()
        p = self.app.post('/api/v1/places', json={
            "name": "Casa", "description": "Nice", "price": 150,
            "latitude": 18.4, "longitude": -66.1,
            "owner_id": u['id'], "amenity_ids": [a['id']]
        }).get_json()
        self.user_id = u['id']
        self.place_id = p['id']

    def test_review_full(self):
        res = self.app.post('/api/v1/reviews', json={
            "text": "Great!", "rating": 5, "user_id": self.user_id, "place_id": self.place_id
        })
        self.assertEqual(res.status_code, 201)
        r = res.get_json()
        rid = r['id']

        res = self.app.get(f'/api/v1/reviews/{rid}')
        self.assertEqual(res.status_code, 200)

        res = self.app.put(f'/api/v1/reviews/{rid}', json={"rating": 4})
        self.assertEqual(res.status_code, 200)

        res = self.app.delete(f'/api/v1/reviews/{rid}')
        self.assertEqual(res.status_code, 204)

if __name__ == '__main__':
    unittest.main()
