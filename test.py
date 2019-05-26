from project import app, db
from flask import escape
from flask_login import current_user
from flask_testing import TestCase
from project.models import BlogPost, User
import unittest
import coverage
import os


class BaseTestCase(TestCase):
    """A base test case."""

    def create_app(self):
        app.config.from_object('config.TestConfig')
        return app

    def setUp(self) -> None:
        db.create_all()
        db.session.add(User('admin', 'ad@min.com', 'admin'))
        db.session.add(BlogPost('Test post', 'This is a test. Only a test.', 'admin'))
        # db.session.commit()

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()


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
            self.assertTrue(current_user.is_active)


def cov():
    """Runs the unit tests with coverage."""
    cov = coverage.coverage(branch=True, include='project/*')
    cov.start()
    tests = unittest.TestLoader().discover('.')
    unittest.TextTestRunner(verbosity=2).run(tests)
    cov.stop()
    cov.save()
    print('Coverage Summary:')
    cov.report()
    basedir = os.path.abspath(os.path.dirname(__file__))
    covdir = os.path.join(basedir, 'coverage')
    cov.html_report(directory=covdir)
    cov.erase()


if __name__ == '__main__':
    cov()
