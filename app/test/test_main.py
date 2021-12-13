import unittest
from src.data.make_dataset import get_raw_kaggle
from src.utils import directory_path, unzip_file
from src.features.build_features import clean_text, join_words_processing, preprocessing, clean_stopwords
from flask import g
from app import app
import ast


class TestML(unittest.TestCase):
    def test_make_dataset(self):
        """This function test the creation of the dataset from kaggle.

        """
        self.assertEqual(get_raw_kaggle(
            "cosmos98/twitter-and-reddit-sentimental-analysis-dataset",
            f"{directory_path}data/external",
            f"{directory_path}data/raw"
        ), True, "Should be True")

        self.assertEqual(get_raw_kaggle(
            "boubidibadiboup",
            f"{directory_path}data/external",
            f"{directory_path}data/raw"
        ), False, "Should be False")



    def test_clean_text(self):
        """This function test the cleaning of the text.

        """
        self.assertEqual(clean_text(
            "This movie is 4now 1 of the worst movie I ever seen. @hans https://stepheniemeyer.com/the-twilight-saga/",
            ), "this movie is 4now 1 of the worst movie i ever seen. ")

        self.assertEqual(clean_text(
            "This movie is maybe worst movie I ever seen. @hans <br>",
            ), "this movie is maybe worst movie i ever seen. ")

    def test_clean_stopwords(self):
        """This function test the cleaning with stopwords.

        """
        self.assertEqual(clean_stopwords(
            [['this', 'movie', 'is', '1', 'of', 'the', 'worst', 'movie', 'i', 'ever', 'watched']],
            ), [['movie', '1', 'worst', 'movie','ever', 'watched']])

        self.assertEqual(clean_stopwords(
            [['a', 'perfect', 'movie', 'i', 'love', 'it']],
            ), [['perfect', 'movie', 'love']])

    def test_preprocessing(self):
        """This function test preprocessing.

        """
        self.assertEqual(preprocessing(
            "Tbh This movie is the worst movie I ever seen. I won't let it win a oscar omdb",
            ), [['honest', 'movie', 'worst', 'movie', 'ever', 'seen'], ['let','win', 'oscar', 'dead','body']] )

        self.assertEqual(preprocessing(
            "This movie is 1 of the worst movie I ever seen. I won't let it win a oscar omdb",
            ), [['movie', 'worst', 'movie', 'ever', 'seen'], ['let','win', 'oscar', 'dead','body']] )


    def test_join_words_processing(self):
        """This function test join words processing.

        """
        self.assertEqual(join_words_processing(
            [['movie', '1', 'worst', 'movie', 'ever', 'seen']],
        ), "movie 1 worst movie ever seen")

        self.assertEqual(join_words_processing(
            [[]],
        ), "")


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

    def test_text_sentiment(self):
        """This function test if the site output is correct (Negative, Neutral or Positive): a test that sends a GET request to the website
        and confirms that the website returns the correct answer.

        """

        response = self.client.get('/json_handle?piecetext=')
        expected_result = {'text': '', 'sentiment': 'empty ! Try again'}
        assert ast.literal_eval(response.data.decode("utf-8")) == expected_result

        text = 'heard there was direct line narendra modi which can accessed any average gujju this true'
        response = self.client.get('/json_handle?piecetext=heard+there+was+direct+line+narendra+modi+which+can+accessed+any+average+gujju+this+true')
        expected_result = {'text': text, 'sentiment': 'positive'}
        assert ast.literal_eval(response.data.decode("utf-8")) == expected_result

        text = 'geez why every single post this thread downvoted'
        response = self.client.get(f'/json_handle?piecetext=geez+why+every+single+post+this+thread+downvoted')
        expected_result = {'text': text, 'sentiment': 'negative'}
        assert ast.literal_eval(response.data.decode("utf-8")) == expected_result

        text = 'can congress eliminate namo and blame advani'
        response = self.client.get(f'/json_handle?piecetext=can+congress+eliminate+namo+and+blame+advani')
        expected_result = {'text': text, 'sentiment': 'neutral'}
        assert ast.literal_eval(response.data.decode("utf-8")) == expected_result


    def test_request_time(self):
        """This function calculate if the average response time of the site is below 100 ms per request.

        """
        self.test_text_sentiment()
        assert g.request_time <= 100
        print(g.request_time)

    def test_request_time_1000(self):
        """This function test if the site can handle stress: the average response time of the site should
        be below 100 ms per request, when 1000 requests are sent per second.

        """
        request_time = []
        for i in range(1000):
            self.test_text_sentiment()
            request_time.append(g.request_time)
        average = sum(request_time) / len(request_time)
        assert average <= 100


if __name__ == '__main__':
    unittest.main()