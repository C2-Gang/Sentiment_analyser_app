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
        """This function test if the site is working: a test that calls the website's url and confirms a code reply of 200.

        """
        response = self.client.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_form(self):
        """This function test if the site is working: a test that calls the website's url and confirms a code reply of 200.

        """
        response = self.client.get('/')
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert 'name="piecetext"' in html

    def test_form_user(self):
        """This function test if the site output is correct (Negative, Neutral or Positive): a test that sends a GET request to the website
        and confirms that the website returns the correct answer.

        """
        response = self.client.get('/handle', data={
            'piecetext': '',
        }, follow_redirects=True)
        error = "error null string."
        assert json.dumps(error)

        response = self.client.get('/handle', data={
            'piecetext': 'heard there was direct line narendra modi which can accessed any average gujju this true',
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        sentiment = "positive"
        assert json.dumps(sentiment)

        response = self.client.get('/handle', data={
            'piecetext': 'geez why every single post this thread downvoted',
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        sentiment = "negative"
        assert json.dumps(sentiment)

        response = self.client.get('/handle', data={
            'piecetext': 'can congress eliminate namo and blame advani',
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        sentiment = "neutral"
        assert json.dumps(sentiment)

    def test_request_time(self):
        """This function calculate if the average response time of the site is below 100 ms per request.

        """
        self.test_form_user()
        assert g.request_time <= 100
        print(g.request_time)

    def test_request_time_1000(self):
        """This function test if the site can handle stress: the average response time of the site should
        be below 100 ms per request, when 1000 requests are sent per second.

        """
        request_time = []
        for i in range(1000):
            self.test_form_user()
            request_time.append(g.request_time)
        average = sum(request_time) / len(request_time)
        assert average <= 100

if __name__ == '__main__':
    unittest.main()
