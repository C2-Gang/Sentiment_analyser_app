from kaggle.api.kaggle_api_extended import KaggleApi
from src.utils import directory_path, unzip_file


def authenticate_kaggle_api():
    """This function is used for
    Kaggle API authentication.

    :return: Kaggle API
    :rtype:
    """
    api = KaggleApi()
    api.authenticate()
    return api


def get_raw_kaggle(dataset_kaggle: str, path_zip_file: str, path_csv_file: str):
    """This function get the competition
    datasets from Kaggle API.

    :param dataset_kaggle: name of the kaggle dataset
    :type dataset_kaggle: str
    :param file: name of the dataset
    :type file: str
    :param path_file: path defined to store the .zip
    :type path_file: str
    :return: value to know if dataset has been successfully created
    :rtype: boolean
    """
    try:
        api = authenticate_kaggle_api()
        api.dataset_download_files(dataset_kaggle, path_zip_file)

        unzip_file(f"{path_zip_file}/twitter-and-reddit-sentimental-analysis-dataset", f"{path_csv_file}")
        print("done")
        return True
    except Exception:
        print("Dataset not found.")
        return False

def generate_raw():
    """This function generates the csv dataset.

    :param file: name of the dataset
    :type file: str
    """
    dataset_kaggle = "cosmos98/twitter-and-reddit-sentimental-analysis-dataset"
    path_zip_file = f"{directory_path}data/external"
    path_csv_file = f"{directory_path}data/raw"
    get_raw_kaggle(dataset_kaggle, path_zip_file, path_csv_file)