""" Handles initial startup processes checking the file system integrity"""
from pathlib import Path
from preferences import PREFERENCES
import json

def setup():
    """Initial setup function"""
    filepaths = [
        PREFERENCES.home_directory,
        PREFERENCES.export_directory,
        PREFERENCES.home_directory/"Projects",
        PREFERENCES.home_directory/"RObjects"
    ]
    for filepath in filepaths:
        Path(filepath).mkdir(exist_ok=True, parents=True)
        
def populate_robjects():
    """Populates the RObjects directory with the default RObjects"""
    with open(Path(__file__).parent/"JSON"/"robjects.json") as f:
        robjects = json.load(f)
    for rhythm in robjects:
        category_filepath = PREFERENCES.robject_directory/rhythm["robject_category"]
        if not (category_filepath.exists()):
            category_filepath.mkdir()
        with open(PREFERENCES.robject_directory/rhythm["robject_category"]/(rhythm["robject_id"]+".json"), "w") as file:
            json.dump(rhythm["robject_data"], file)
        
def main():
    """Main function"""
    setup()
    populate_robjects()
    


if __name__ == "__main__":
    main()
5