import unittest
from src.data.make_dataset import get_raw_kaggle
from src.utils import directory_path, unzip_file
from src.features.build_features import clean_text, join_words_processing, preprocessing, clean_stopwords


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
            "This movie is **** worst movie I ever seen. @hans <br>",
            ), "this movie is **** worst movie i ever seen. ")

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



if __name__ == '__main__':
    unittest.main()