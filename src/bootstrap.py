""" Handles initial startup processes checking the file system integrity"""
from pathlib import Path
from preferences import PREFERENCES
from robject import restore_robject
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
    for robject in robjects:
        restore_robject(robjects, robject["robject_id"], robject["robject_category"])
        
def main():
    """Main function"""
    setup()
    populate_robjects()
    


if __name__ == "__main__":
    main()
