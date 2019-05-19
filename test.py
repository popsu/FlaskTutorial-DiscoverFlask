from project import app
from flask import escape
import unittest


class FlaskTestCase(unittest.TestCase):

    # Ensure that flask was set up correctly
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # Ensure that the login page loads correctly
    def test_login_page_loads(self):
        tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertTrue((b'Please login' in response.data))

    # Ensure login behaves correctly given the correct credentials
    def test_correct_login(self):
        tester = app.test_client(self)
        response = tester.post(
            '/login',
            data={'username': 'admin', 'password': 'admin'},
            follow_redirects=True
        )
        self.assertIn(b'You were just logged in!', response.data)

    # Ensure login behaves correctly given incorrect credentials
    def test_incorrect_login(self):
        tester = app.test_client(self)
        response = tester.post(
            '/login',
            data={'username': 'wrong', 'password': 'wrong'},
            follow_redirects=True
        )
        self.assertIn(b'Invalid credentials. Please try again.', response.data)

    # Ensure logout behaves correctly
    def test_logout(self):
        tester = app.test_client(self)
        tester.post(
            '/login',
            data={'username': 'admin', 'password': 'admin'},
            follow_redirects=True
        )
        response = tester.get('/logout', follow_redirects=True)
        self.assertIn(b'You were just logged out!', response.data)

    # Ensure that the main page requires login
    def test_main_route_requires_login(self):
        tester = app.test_client(self)
        response = tester.get('/', follow_redirects=True)
        self.assertTrue(b'You need to login first.' in response.data)

    # Ensure that the logout page requires login
    def test_logout_route_requires_login(self):
        tester = app.test_client(self)
        response = tester.get('/logout', follow_redirects=True)
        self.assertTrue(b'You need to login first.' in response.data)

    # Ensure that posts show up on the main page
    def test_main_route_shows_posts(self):
        tester = app.test_client(self)
        response = tester.post(
            '/login',
            data={'username': 'admin', 'password': 'admin'},
            follow_redirects=True
        )
        # String -> Markup -> String -> Bytes
        self.assertIn(str(escape("I'm well.")).encode('utf-8'), response.data)


if __name__ == '__main__':
    unittest.main()
