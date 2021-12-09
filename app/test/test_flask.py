import unittest
from flask import g
from app import app
import json

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.appctx = self.app.app_context()
        self.appctx.push()
        self.client = self.app.test_client()

    def tearDown(self):
        self.appctx.pop()
        self.app = None
        self.appctx = None
        self.client = None

    def test_home_page_200(self):
        response = self.client.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_form(self):
        response = self.client.get('/')
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert 'name="text"' in html

    def test_form_user(self):
        response = self.client.get('/handle', data={
            'piecetext': '',
        }, follow_redirects=True)
        error = {"sentiment": "error null string."}
        assert json.dumps(error)

        response = self.client.get('/handle', data={
            'piecetext': 'phrase positive',
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 400)
        sentiment = {"sentiment": "Positive"}
        assert json.dumps(sentiment)

        response = self.client.get('/handle', data={
            'piecetext': 'phrase Negative',
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 400)
        sentiment = {"sentiment": "Negative"}
        assert json.dumps(sentiment)

        response = self.client.get('/handle', data={
            'piecetext': 'phrase neutre',
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 400)
        sentiment = {"sentiment": "Neutral"}
        assert json.dumps(sentiment)

    def test_request_time(self):
        self.test_form_user()
        assert g.request_time <= 100
        print(g.request_time)

    def test_request_time_1000(self):
        request_time = []
        for i in range(1000):
            self.test_form_user()
            request_time.append(g.request_time)
        average = sum(request_time) / len(request_time)
        assert average <= 100

if __name__ == '__main__':
    unittest.main()
