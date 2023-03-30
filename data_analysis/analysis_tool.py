"""!
@package analysis_tool
Documentation for analysis tool.
"""

from bs4 import BeautifulSoup
import plotly.express as px
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
    _index_text = BeautifulSoup(file, "lxml")
_entries = _index_text.find_all("a")[1:]
for entry in _entries:
    _INSTRUCTION_PAGES[entry.get_text()] = entry["href"][1:]

with open(_INSTRUCTIONS_INFO_FILE, "r") as read_file:
    _instructions_info = json.load(read_file)["instructions"]
for item in _instructions_info:
    _INSTRUCTIONS_INFO[item["instruction"]] = {
        "category": item["category"],
        "group": item["group"],
        "description": item["description"],
    }


# HELPERS
def _find_key(name: str) -> str:
    found = False
    key = None
    for df_key in _DFS:
        if df_key == name:
            return df_key
        if df_key.startswith(name):
            if found:
                raise KeyError(f"Found two or more dataframes with names starting with {name}")
            key = df_key
            found = True
    if not found:
        raise KeyError(name)
    return key


# GENERAL FUNCTIONS
def add_df(name: str, df: pd.DataFrame) -> None:
    """!
    Adds a new dataframe to the scope.
        @param name: Name of the dataframe.
        @param df: Dataframe.
    """
    _DFS[name] = df


def get_df(name: str) -> pd.DataFrame:
    """!
    Returns dataframe by name (or its beginning).
        @param name: Name of the dataframe or its beginning.
        @return Dataframe.
    """
    return _DFS[_find_key(name)]


def show_df(name: str, number_of_rows: int = 5) -> None:
    """!
    Shows the dataframe.
        @param name: Name of the dataframe or its beginning.
        @param number_of_rows: Number of rows to show. Default: 5.
    """
    display(_DFS[_find_key(name)].head(number_of_rows))


def head(name: str, number_of_rows: int = 5) -> pd.DataFrame:
    """!
    Returns head of the dataframe.
        @param name: Name of the dataframe or its beginning.
        @param number_of_rows: Number of rows in head. Default: 5.
        @return Head of the dataframe.
    """
    return _DFS[_find_key(name)].head(number_of_rows)


def remove_df(name: str) -> None:
    """!
    Returns dataframe by name (or its beginning).
        @param name: Name of the dataframe or its beginning.
    """
    _DFS.pop(_find_key(name))


def df_len(name: str) -> int:
    """!
    Returns length of the dataframe.
        @param name: Name of the dataframe or its beginning.
        @return Length of the dataframe.
    """
    return len(_DFS[_find_key(name)])


def remove_filename_column(name: str) -> pd.DataFrame:
    """!
    Removes "filename" column from the dataframe.
        @param name: Name of the dataframe or its beginning.
        @return Dataframe without "filename" column.
    """
    df = _DFS[_find_key(name)]
    try:
        df = df.drop("filename", axis=1)
    except KeyError:
        pass
    return df


def initialize_with_archives(archives_folder: str, dataframes_dir: str) -> None:
    """!
    Unzips archives and loads dataframes to the scope.
        @param archives_folder: Path to the folder with archives.
        @param dataframes_dir: Path to the folder in which unzipped dataframes will be placed.
    """
    for archive in os.listdir(archives_folder):
        path = os.path.join(archives_folder, archive)
        with zipfile.ZipFile(path, "r") as zip_ref:
            zip_ref.extractall(dataframes_dir)
        _DFS[archive.split("_")[0]] = pd.read_csv(f"{os.path.join(dataframes_dir, archive)[:-3]}csv")


def dfs_list() -> list[str]:
    """!
    Returns a list of dataframe names in the scope.
        @return List of dataframe names.
    """
    return list(_DFS.keys())


def what_is_instruction(instruction: str) -> None:
    """!
    Shows instruction information in a new tab (if such an instruction was found).
        @param instruction: Instruction.
    """
    try:
        path = f"../x86doc{_INSTRUCTION_PAGES[instruction.upper()]}"
        display(Javascript('window.open("{url}");'.format(url=path)))
    except KeyError:
        print("Instruction is not found.")


# ANALYSIS FUNCTIONS
def total_instruction_usage(name: str, to_dict: bool = True, show: bool = True) -> dict[str, int] | pd.DataFrame:
    """!
    Counts total instruction usage (sum of all values in each column) in the dataframe.
        @param name: Name of the dataframe or its beginning.
        @param to_dict: If True, function returns the result in the form of a dictionary. Default: True.
        @param show: Pretty print a result. Default: True.
        @return Dictionary or dataframe with total instruction usage.
    """
    df = remove_filename_column(_find_key(name))
    total = df.sum()
    total_dict = dict(total)
    if show:
        for instruction in total_dict:
            print(f"{instruction}: {total_dict[instruction]}")
    if to_dict:
        return total_dict
    return total


def divide_into_categories(name: str) -> pd.DataFrame:
    """!
    Divides instructions in the dataframe into categories.
        @param name: Name of the dataframe or its beginning.
        @return Dataframe with instruction categories.
    """
    df = _DFS[_find_key(name)].copy()
    columns = list(df.columns)
    for column in columns:
        column_upper = column.upper()
        if column == "filename":
            continue
        if column_upper in _INSTRUCTIONS_INFO:
            category = _INSTRUCTIONS_INFO[column_upper]["category"]
        elif column_upper[:-1] in _INSTRUCTIONS_INFO:
            category = _INSTRUCTIONS_INFO[column_upper[:-1]]["category"]
        else:
            category = "Other"
        if category not in df.columns:
            df[category] = df[column]
        else:
            df[category] += df[column]
        df.drop(column, axis=1, inplace=True)
    return df


def divide_into_groups(name: str) -> pd.DataFrame:
    """!
    Divides instructions in the dataframe into groups.
        @param name: Name of the dataframe or its beginning.
        @return Dataframe with instruction groups.
    """
    df = _DFS[_find_key(name)].copy()
    columns = list(df.columns)
    for column in columns:
        column_upper = column.upper()
        if column == "filename":
            continue
        if column_upper in _INSTRUCTIONS_INFO:
            group = _INSTRUCTIONS_INFO[column_upper]["group"]
        elif column_upper[:-1] in _INSTRUCTIONS_INFO:
            group = _INSTRUCTIONS_INFO[column_upper[:-1]]["group"]
        else:
            group = "Other"
        if group not in df.columns:
            df[group] = df[column]
        else:
            df[group] += df[column]
        df.drop(column, axis=1, inplace=True)
    return df


def where_instruction(instruction: str, name: str) -> pd.DataFrame:
    """!
    Leaves only those rows in which the instruction occurs a non-zero number of times.
        @param instruction: Instruction.
        @param name: Name of the dataframe or its beginning.
        @return Dataframe with selected rows.
    """
    key = _find_key(name)
    return _DFS[key][_DFS[key][instruction] != 0].reset_index(drop=True)


def where_category(category: str, name: str, divide_df: bool = True) -> pd.DataFrame:
    """!
    Leaves only those rows in which instructions of the category occur a non-zero number of times.
        @param category: Category.
        @param name: Name of the dataframe or its beginning.
        @param divide_df: If True, function will divide instructions in the dataframe into categories. Default: True.
        @return Dataframe with selected rows.
    """
    key = _find_key(name)
    divided_df = divide_into_categories(key)
    mask = divided_df[category] != 0
    if divide_df:
        return divided_df[mask].reset_index(drop=True)
    else:
        return _DFS[key][mask].reset_index(drop=True)


def where_group(group: str, name: str, divide_df: bool = True) -> pd.DataFrame:
    """!
    Leaves only those rows in which instructions of the group occur a non-zero number of times.
        @param group: Group.
        @param name: Name of the dataframe or its beginning.
        @param divide_df: If True, function will divide instructions in the dataframe into groups. Default: True.
        @return Dataframe with selected rows.
    """
    key = _find_key(name)
    divided_df = divide_into_groups(key)
    mask = divided_df[group] != 0
    if divide_df:
        return divided_df[mask].reset_index(drop=True)
    else:
        return _DFS[key][mask].reset_index(drop=True)


def sort_columns_by_sum(name: str, ascending: bool = False) -> pd.DataFrame:
    """!
    Sorts columns in the dataframe by its sums.
        @param name: Name of the dataframe or its beginning.
        @param ascending: If True, the dataframe columns will be sorted in ascending order,
        otherwise - in descending order. Default: False.
        @return Dataframe with sorted columns.
    """
    key = _find_key(name)
    df = _DFS[key]
    occurrences_list: list[(str, int)] = sorted(
        total_instruction_usage(key, show=False).items(), key=lambda elem: elem[1], reverse=not ascending
    )
    occurrences = dict(occurrences_list)
    if "filename" in df:
        return df[["filename"] + list(occurrences.keys())]
    return df[list(occurrences.keys())]


def top_popular(name: str, n: int = 10) -> pd.DataFrame:
    """!
    Leaves in the dataframe top n most popular instructions.
        @param name: Name of the dataframe or its beginning.
        @param n: Number of instructions. Default: 10.
        @return: Dataframe with top n most popular instructions.
    """
    df = sort_columns_by_sum(name)
    if "filename" in df:
        offset = 1
    else:
        offset = 0
    return df[df.columns[: (n + offset)]]


def top_rare(name: str, n: int = 10) -> pd.DataFrame:
    """!
    Leaves in the dataframe top n the rarest instructions.
        @param name: Name of the dataframe or its beginning.
        @param n: Number of instructions. Default: 10.
        @return Dataframe with top n the rarest instructions.
    """
    df = sort_columns_by_sum(name, ascending=True)
    if "filename" in df:
        offset = 1
    else:
        offset = 0
    return df[df.columns[: (n + offset)]]


def total_histogram(
    names: list[str] | None = None, percent: bool = True, ascending: bool = False, width: int = 2000
) -> None:
    """!
    Builds a histogram of the total instruction usage in dataframes with the names given.
        @param names: None or list of dataframe names (or their beginnings).
        If None, all dataframes in the scope will be used. Default: None.
        @param percent: If True, the histogram will be built by percentage, not by absolute values. Default: True.
        @param ascending: If True, the histogram columns will be sorted in ascending order,
        otherwise - in descending order. Default: False.
        @param width: Width of the histogram. Default: 2000.
    """
    if names is None:
        names = dfs_list()
    dfs_for_histogram = dict()
    for name in names:
        key = _find_key(name)
        df = remove_filename_column(key)
        dfs_for_histogram[key] = pd.DataFrame(df.sum(axis=0), columns=[key])
    sums: pd.DataFrame = pd.concat(dfs_for_histogram.values(), join="outer", axis=1).fillna(0).astype(int)
    if "undefined" in sums.index:
        sums.drop(index="undefined", inplace=True)
    sums["sum"] = sums.sum(axis=1)
    sums.sort_values(by="sum", ascending=ascending, inplace=True)
    sums.drop("sum", axis=1, inplace=True)
    if percent:
        fig = px.histogram(sums, x=sums.index, y=sums.columns, barmode="group", histnorm="percent", width=width)
    else:
        fig = px.histogram(sums, x=sums.index, y=sums.columns, barmode="group", width=width)
    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0))
    display(fig)


def total_categories_histogram(
    names: list[str] | None = None, percent: bool = True, ascending: bool = False, width: int = 2000
) -> None:
    """!
    Builds a histogram of the total instruction category usage in dataframes with the names given.
        @param names: None or list of dataframe names (or their beginnings).
        If None, all dataframes in the scope will be used. Default: None.
        @param percent: If True, the histogram will be built by percentage, not by absolute values. Default: True.
        @param ascending: If True, the histogram columns will be sorted in ascending order,
        otherwise - in descending order. Default: False.
        @param width: Width of the histogram. Default: 2000.
    """
    if names is None:
        names = dfs_list()
    cat_names = []
    for name in names:
        cat_name = f"{name}_categories"
        cat_names.append(cat_name)
        add_df(cat_name, divide_into_categories(name))
    total_histogram(names=cat_names, percent=percent, ascending=ascending, width=width)
    for cat_name in cat_names:
        remove_df(cat_name)


def total_groups_histogram(
    names: list[str] | None = None, percent: bool = True, ascending: bool = False, width: int = 2000
) -> None:
    """!
    Builds a histogram of the total instruction group usage in dataframes with the names given.
        @param names: None or list of dataframe names (or their beginnings).
        If None, all dataframes in the scope will be used. Default: None.
        @param percent: If True, the histogram will be built by percentage, not by absolute values. Default: True.
        @param ascending: If True, the histogram columns will be sorted in ascending order,
        otherwise - in descending order. Default: False.
        @param width: Width of the histogram. Default: 2000.
    """
    if names is None:
        names = dfs_list()
    group_names = []
    for name in names:
        group_name = f"{name}_groups"
        group_names.append(group_name)
        add_df(group_name, divide_into_groups(name))
    total_histogram(names=group_names, percent=percent, ascending=ascending, width=width)
    for group_name in group_names:
        remove_df(group_name)
