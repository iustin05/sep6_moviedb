import unittest
from flask import url_for
from app import create_app
from app.models import User


class RoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['SERVER_NAME'] = 'localhost'
        self.app.config['APPLICATION_ROOT'] = '/'
        self.app.config['PREFERRED_URL_SCHEME'] = 'http'
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def test_home_route(self):
        response = self.client.get(url_for('master.home'))
        self.assertEqual(response.status_code, 200)

    def test_register_route(self):
        response = self.client.post(url_for('master.register'), data=dict(
            email='test@example.com',
            password='password',
            confirm='password'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        user = User.query.filter_by(email='test@example.com').first()
        self.assertIsNotNone(user)

    def test_login_route(self):
        response = self.client.post(url_for('master.login'), data=dict(
            email='test@example.com',
            password='password'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_logout_route(self):
        response = self.client.get(url_for('master.logout'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    # def test_search_route(self):
    #     response = self.client.post(url_for('master.search'), data=dict(
    #         title='Test Movie'
    #     ), follow_redirects=True)
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_movie_detail_route(self):
    #     response = self.client.get(url_for('master.movie_detail', movie_id=1))
    #     self.assertEqual(response.status_code, 200)

    def tearDown(self):
        self.app_context.pop()


if __name__ == '__main__':
    unittest.main()
