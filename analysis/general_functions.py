from bs4 import BeautifulSoup
import pandas as pd
import zipfile
import json
import os

from IPython.display import display
from IPython.display import Javascript

_INSTRUCTIONS_INFO_FILE = "../x86-64_instructions.json"
_DFS = dict()
_INSTRUCTION_PAGES = dict()
_INSTRUCTIONS_INFO = dict()

with open("../x86doc/index.html") as file:
    index_text = BeautifulSoup(file, "lxml")
entries = index_text.find_all("a")[1:]
for entry in entries:
    _INSTRUCTION_PAGES[entry.get_text()] = entry["href"][1:]

with open(_INSTRUCTIONS_INFO_FILE, "r") as read_file:
    instructions_info = json.load(read_file)["instructions"]
for item in instructions_info:
    _INSTRUCTIONS_INFO[item["instruction"]] = {
        "category": item["category"],
        "group": item["group"],
        "description": item["description"],
    }


def find_key(name: str) -> str:
    found = False
    key = None
    for df_key in _DFS:
        if df_key == name:
            key = df_key
            break
        if df_key.startswith(name):
            if found:
                raise KeyError(f"Found two or more dataframes with names starting with {name}")
            key = df_key
            found = True
    if not found:
        raise KeyError(name)

    return key


def add_df(name: str, df: pd.DataFrame):
    """
    Adds a new dataframe to the scope.
    :param name: Name of the dataframe.
    :param df: Dataframe.
    """
    _DFS[name] = df


def get_df(name: str) -> pd.DataFrame:
    """
    Returns dataframe by name (or its beginning).
    :param name: Name of the dataframe or its beginning.
    :return: Dataframe.
    """
    return _DFS[_find_key(name)]


def show_df(name: str, number_of_rows: int = 5):
    """
    Shows dataframe by name (or its beginning).
    :param name: Name of the dataframe or its beginning.
    :param number_of_rows: Number of rows to show. Default: 5.
    """
    display(_DFS[_find_key(name)].head(number_of_rows))


def head(name: str, number_of_rows: int = 5) -> pd.DataFrame:
    """
    Returns head of dataframe by name (or its beginning).
    :param name: Name of the dataframe or its beginning.
    :param number_of_rows: Number of rows in head. Default: 5.
    :return: Head of the dataframe.
    """
    return _DFS[_find_key(name)].head(number_of_rows)


def remove_df(name: str):
    """
    Returns dataframe by name (or its beginning).
    :param name: Name of the dataframe or its beginning.
    """
    _DFS.pop(_find_key(name))


def remove_filename_column(name: str) -> pd.DataFrame:
    """
    Removes "filename" column from the dataframe.
    :param name: Name of the dataframe or its beginning.
    :return: Dataframe without "filename" column.
    """
    df = _DFS[_find_key(name)].drop("filename", axis=1)
    return df


def initialize_with_archives(archives_folder: str, dataframes_dir: str):
    """
    Unzips archives and loads dataframes to the scope.
    :param archives_folder: Path to the folder with archives.
    :param dataframes_dir: Path to the folder in which unzipped dataframes will be placed.
    """
    for archive in os.listdir(archives_folder):
        path = os.path.join(archives_folder, archive)
        with zipfile.ZipFile(path, "r") as zip_ref:
            zip_ref.extractall(dataframes_dir)
        _DFS[archive.split("_")[0]] = pd.read_csv(f"{os.path.join(dataframes_dir, archive)[:-3]}csv")


def dfs_list() -> list[str]:
    """
    Returns a list of dataframe names in the scope.
    :return: List of dataframe names.
    """
    return list(_DFS.keys())


def what_is_instruction(instruction: str):
    """
    Shows instruction information in a new tab (if such an instruction was found).
    :param instruction: Instruction.
    """
    try:
        path = f"../x86doc{_INSTRUCTION_PAGES[instruction.upper()]}"
        display(Javascript('window.open("{url}");'.format(url=path)))
    except KeyError:
        print("Instruction is not found.")
