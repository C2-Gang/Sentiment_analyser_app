import unittest
from src.data.make_dataset import get_raw_kaggle
from src.utils import directory_path, unzip_file
from src.features.build_features import clean_html, join_words_processing, preprocessing


class TestML(unittest.TestCase):
    def test_make_dataset(self):
        self.assertEqual(get_raw_kaggle(
            "IMDB%20Dataset.csv",
            f"{directory_path}data/external",
            f"{directory_path}data/raw"
        ), True, "Should be True")

        self.assertEqual(get_raw_kaggle(
            "Dataset.csv",
            f"{directory_path}data/external",
            f"{directory_path}data/raw"
        ), False, "Should be False")

    def test_clean_labels(self):
        self.assertEqual(clean_html(
            "<br> <br>This movie is 1 of the worst movie I ever seen.",
            ), " This movie is 1 of the worst movie I ever seen.")

        self.assertEqual(clean_html(
            "This movie is 1 of the worst movie I ever seen.",
            ), "This movie is 1 of the worst movie I ever seen.")

    def test_preprocessing(self):
        self.assertEqual(preprocessing(
            "This movie is 1 of the worst movie I ever seen",
            ), [['movie', '1', 'worst', 'movie', 'ever', 'seen']] )

    def test_join_words_processing(self):
        self.assertEqual(join_words_processing(
            [['movie', '1', 'worst', 'movie', 'ever', 'seen']],
        ), "movie worst movie ever seen")



if __name__ == '__main__':
    unittest.main()