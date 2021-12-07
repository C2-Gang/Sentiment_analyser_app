# -*- coding: utf-8 -*-

from kaggle.api.kaggle_api_extended import KaggleApi
import pandas as pd
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


def get_raw_kaggle(name: str, path_zip_file: str, path_csv_file: str):
    """This function get the competition
    datasets from Kaggle API.

    :param competition_name: name of the competition
    :type competition_name: str
    :param file: name of the dataset
    :type file: str
    :param path_file: path defined to store the .zip
    :type path_file: str
    :return: value to know if dataset has been successfully created
    :rtype: boolean
    """
    try:
        api = authenticate_kaggle_api()
        api.dataset_download_file("lakshmi25npathi/imdb-dataset-of-50k-movie-reviews", 'IMDB Dataset.csv', path_zip_file)
        unzip_file(f"{path_zip_file}/{name}", f"{path_csv_file}")
        print('done')
        return True
    except Exception:
        print("Dataset not found.")
        return False

def generate_raw():
    """This function generates the csv dataset.

    :param file: name of the dataset
    :type file: str
    """
    name = "IMDB%20Dataset.csv"

    path_zip_file = f"{directory_path}data/external"
    path_csv_file = f"{directory_path}data/raw"
    get_raw_kaggle(name, path_zip_file, path_csv_file)