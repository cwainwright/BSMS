""" Handles initial startup processes checking the file system integrity"""

from pathlib import Path
from preferences import PREFERENCES

def setup():
    """Initial setup function"""
    filepaths = [
        PREFERENCES.home_directory,
        PREFERENCES.export_directory,
        PREFERENCES.home_directory/"Projects",
        PREFERENCES.home_directory/"Rests",
        PREFERENCES.home_directory/"Rhythms"
    ]
    for filepath in filepaths:
        Path(filepath).mkdir(exist_ok=True, parents=True)


if __name__ == "__main__":
    setup()
