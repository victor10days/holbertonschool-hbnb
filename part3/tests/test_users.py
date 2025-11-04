import unittest
from app import create_app

class UserApiTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app().test_client()

    def test_create_and_get_user(self):
        # create
        res = self.app.post('/api/v1/users', json={
            "email": "a@b.com", "password": "secret", "first_name": "A", "last_name": "B"
        })
        self.assertEqual(res.status_code, 201)
        user = res.get_json()
        self.assertIn('id', user)
        self.assertNotIn('password', user)

        # get
        uid = user['id']
        res = self.app.get(f'/api/v1/users/{uid}')
        self.assertEqual(res.status_code, 200)

if __name__ == '__main__':
    unittest.main()
