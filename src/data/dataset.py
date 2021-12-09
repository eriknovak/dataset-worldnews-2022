import os
import json
import pathlib
from datetime import datetime

# static data location

RAW_DATA_PATH = os.path.join(
    pathlib.Path(__file__).parent.parent.parent.absolute(), "data/raw"
)


def load_dataset(fpath: str = RAW_DATA_PATH):
    """Get all of the articles in a single array

    Args:
        fpath (str): The directory path from which we wish to collect the data.
    """

    articles = []
    # iterate through all of the files and folders
    for file in os.listdir(fpath):
        filepath = os.path.join(fpath, file)
        if os.path.isfile(filepath):
            [concepts, date_start, date_end] = file.split(".")[0].split("-")
            add_attrs = {
                "concepts": concepts.split("&"),
                "date_start": datetime.strptime(date_start, "%Y%m%d"),
                "date_end": datetime.strptime(date_end, "%Y%m%d"),
            }
            # open the file and retrieve all of the article metadata
            with open(filepath, mode="r", encoding="utf8") as file:
                articles = articles + [
                    {**json.loads(line), **add_attrs} for line in file.readlines()
                ]
        else:
            # append the directory articles
            articles = articles + load_dataset(filepath)

    # return the articles
    return articles