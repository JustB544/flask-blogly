from unittest import TestCase
from app import app
from flask import session
from seed import seed
from models import User, Post

class FlaskTests(TestCase):
    """tests"""
    def setUp(self):
        seed()
    def test_user_route(self):
        with app.test_client() as client:
            resp = client.get('/users')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Johnny Doe', html)
    def test_user_detail(self):
        with app.test_client() as client:
            resp = client.get('/users/1')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Johnny Doe', html)
            self.assertIn('<img src="https://hips.hearstapps.com/hmg-prod/images/dog-puppy-on-garden-royalty-free-image-1586966191.jpg?crop=0.752xw:1.00xh;0.175xw,0&amp;resize=1200:*" />', html)
            self.assertIn('generic name', html)
    def test_edit_route(self):
        with app.test_client() as client:
            resp = client.post('/users/1/edit', data={'first': 'John', 'last': 'Doe', 'src': ''})

            self.assertEqual(resp.status_code, 302)
            user = User.query.get(1)
            self.assertEqual(user.first_name, "John")
    def test_delete_route(self):
        with app.test_client() as client:
            resp = client.post('/users/1/delete')

            self.assertEqual(resp.status_code, 302)
            resp = client.get("/users")
            html = resp.get_data(as_text=True)
            self.assertNotIn("Johnny Doe", html)
    def test_post_route(self):
        with app.test_client() as client:
            resp = client.get('/posts/1')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('generic name', html)
            self.assertIn('my name is generic', html)
    def test_delete_post_route(self):
        with app.test_client() as client:
            resp = client.post('/posts/1/delete')

            self.assertEqual(resp.status_code, 302)
            resp = client.get("/users/1")
            html = resp.get_data(as_text=True)
            self.assertNotIn("generic name", html)

        