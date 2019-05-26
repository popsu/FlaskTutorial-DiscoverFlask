from tests.base import BaseTestCase
from flask_login import current_user
from flask import request
from project.models import User
from project import bcrypt


class TestUser(BaseTestCase):

    # Ensure user can register
    def test_register_works(self):
        with self.client:
            response = self.client.post(
                '/register',
                data={'username': 'testuser123', 'email': 'test@email.com',
                      'password': 'password123', 'confirm': 'password123'},
                follow_redirects=True
            )
            self.assertIn(b'Account created. Welcome.', response.data)
            self.assertTrue(current_user.name == 'testuser123')
            self.assertTrue(current_user.is_active)
            user = User.query.filter_by(email='test@email.com').first()
            self.assertEqual(str(user), '<name - testuser123>')

    # Ensure id is correct for current/logged in user
    def test_get_by_id(self):
        with self.client:
            self.client.post(
                '/login',
                data={'username': 'admin', 'password': 'admin'},
                follow_redirects=True
            )
            self.assertTrue(current_user.id == 1)
            self.assertFalse(current_user.id == 20)

    def test_check_password(self):
        user = User.query.filter_by(email='ad@min.com').first()
        self.assertTrue(bcrypt.check_password_hash(user.password, 'admin'))
        self.assertFalse(bcrypt.check_password_hash(user.password, 'foobar'))

    # Ensure errors are thrown during an incorrect user registration
    def test_incorrect_user_registration(self):
        with self.client:
            response = self.client.post(
                '/register',
                data={'username': 'testname12', 'email': 'incorrect_email',
                      'password': '123456', 'confirm': 'non-matchin-pw'},
                follow_redirects=True
            )
            self.assertIn(b'Invalid email address.', response.data)
            self.assertIn('/register', request.url)


class UsersViewsTests(BaseTestCase):
    # Ensure that the login page loads correctly
    def test_login_page_loads(self):
        response = self.client.get('/login', content_type='html/text')
        self.assertTrue((b'Please login' in response.data))

    # Ensure login behaves correctly given the correct credentials
    def test_correct_login(self):
        with self.client:
            response = self.client.post(
                '/login',
                data={'username': 'admin', 'password': 'admin'},
                follow_redirects=True
            )
            self.assertIn(b'You were logged in.', response.data)
            self.assertTrue(current_user.name == 'admin')
            self.assertTrue(current_user.is_active)

    # Ensure login behaves correctly given incorrect credentials
    def test_incorrect_login(self):
        response = self.client.post(
            '/login',
            data={'username': 'wrong', 'password': 'wrong'},
            follow_redirects=True
        )
        self.assertIn(b'Invalid Credentials. Please try again.', response.data)

    # Ensure logout behaves correctly
    def test_logout(self):
        with self.client:
            self.client.post(
                '/login',
                data={'username': 'admin', 'password': 'admin'},
                follow_redirects=True
            )
            response = self.client.get('/logout', follow_redirects=True)
            self.assertIn(b'You were logged out.', response.data)
            self.assertFalse(current_user.is_active)

    # Ensure that the logout page requires login
    def test_logout_route_requires_login(self):
        response = self.client.get('/logout', follow_redirects=True)
        self.assertTrue(b'Please log in to access this page.' in response.data)
