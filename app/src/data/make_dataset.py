from kaggle.api.kaggle_api_extended import KaggleApi
from src.utils import directory_path, unzip_file


def authenticate_kaggle_api():
    """This function is used for
    Kaggle API authentication.
    """
    api = KaggleApi()
    api.authenticate()
    return api


def get_raw_kaggle(path_zip_file: str, path_csv_file: str):
    """This function get the competition
    datasets from Kaggle API.

    :param competition_name: name of the competition
    :type competition_name: str
    :param file: name of the dataset
    :type file: str
    :param path_file: path defined to store the .zip
    :type path_file: str
    """
    api = authenticate_kaggle_api()
    api.dataset_download_files("cosmos98/twitter-and-reddit-sentimental-analysis-dataset", path_zip_file)

    unzip_file(f"{path_zip_file}/twitter-and-reddit-sentimental-analysis-dataset", f"{path_csv_file}")
    print("done")

def generate_raw():
    """This function generates the csv dataset.

    :param file: name of the dataset
    :type file: str
    """

    path_zip_file = f"{directory_path}data/external"
    path_csv_file = f"{directory_path}data/raw"
    get_raw_kaggle(path_zip_file, path_csv_file)