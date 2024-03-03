import unittest
from unittest.mock import patch
import json
from project1 import app as project1

#Python unittest
class TestServer(unittest.TestCase):

    def setUp(self):
        self.app = project1.test_client()
        self.app.testing = True

    def test_jwks_endpoint(self):
        response = self.app.get('/.well-known/jwks.json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('keys', data)
        self.assertTrue(isinstance(data['keys'], list))

    def test_auth_endpoint(self):
        response = self.app.post('/auth')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('token', data)
        token = data['token']
        # Verify token if needed

if __name__ == '__main__':
    unittest.main()
