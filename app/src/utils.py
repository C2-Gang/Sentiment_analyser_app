import os
import zipfile
import pickle
import json


def get_directory():
    directory_path = os.path.realpath(__file__).replace("app/src/utils.py", "")
    if directory_path == "":
        return "./"
    else:
        return directory_path


directory_path = get_directory()


def unzip_file(old_path: str, new_path: str):
    """This function unzips a file.

    :param old_path: old path (for zip)
    :type old_path: str
    :param new_path: new path
    :type new_path: str
    """
    with zipfile.ZipFile(f"{old_path}.zip", "r") as zipref:
        zipref.extractall(new_path)

def dump_json_object(path:str, object):
    """This function allows you to dump an object to json format and store it

    :param path: path to store
    :type path: str
    :param object: object to store
    :type object:
    """
    with open(path, "w") as outfile:
        json.dump(object, outfile)

def load_json_object(path:str):
    """This function allows you to load an object from json format

    :param path: path
    :type path: str
    :return: object
    :rtype:
    """
    with open(path) as json_file:
        object = json.load(json_file)
    return object

def dump_pickle(path: str, object):
    """This function allows you to dump an object to pickle format and store it

    :param path: path to store
    :type path: str
    :param object: object to store
    :type object:
    """
    with open(f"{path}.pickle", 'wb') as handle:
        pickle.dump(object, handle, protocol=pickle.HIGHEST_PROTOCOL)


def load_pickle(path: str):
    """This function allows you to load an object from pickle format

    :param path: path to store
    :type path: str
    :return: object
    :rtype:
    """
    with open(f"{path}.pickle", 'rb') as handle:
        object = pickle.load(handle)
    return object

