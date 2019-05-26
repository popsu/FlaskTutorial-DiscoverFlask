from tests.base import BaseTestCase
from flask_login import current_user
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

