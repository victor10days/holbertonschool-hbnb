import unittest
from app import create_app

class UserTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app().test_client()

    def test_create_user_valid(self):
        response = self.app.post('/api/v1/users/', json={
            "first_name": "Victor",
            "last_name": "Diaz",
            "email": "victor@email.com"
        })
        self.assertEqual(response.status_code, 201)

    def test_create_user_invalid(self):
        response = self.app.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "",
            "email": "bad"
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.get_json())
