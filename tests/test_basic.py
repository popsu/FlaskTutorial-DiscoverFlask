from flask_login import current_user
from tests.base import BaseTestCase
from flask import escape


class FlaskTestCase(BaseTestCase):

    # Ensure that flask was set up correctly
    def test_index(self):
        response = self.client.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # Ensure that the main page requires login
    def test_main_route_requires_login(self):
        response = self.client.get('/', follow_redirects=True)
        self.assertTrue(b'Please log in to access this page.' in response.data)

    # Ensure that posts show up on the main page
    def test_main_route_shows_posts(self):
        response = self.client.post(
            '/login',
            data={'username': 'admin', 'password': 'admin'},
            follow_redirects=True
        )
        # String -> Markup -> String -> Bytes
        self.assertIn(str(escape('This is a test. Only a test.')).encode('utf-8'), response.data)
