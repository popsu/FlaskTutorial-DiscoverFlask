from tests.base import BaseTestCase


class BlogPostTests(BaseTestCase):

    # Ensure a logged in user can add a new post
    def test_user_can_post(self):
        with self.client:
            self.client.post(
                'login',
                data={'username': 'admin', 'password': 'admin'},
                follow_redirects=True
            )
            response = self.client.post(
                '/',
                data={'title': 'test', 'description': 'test'},
                follow_redirects=True
            )
            self.assert200(response)
            self.assertIn(b'New entry was successfully posted. Thanks', response.data)
