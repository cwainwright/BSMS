import json
from pathlib import Path

def get_template(template:str) -> dict:
    filepath = Path(__file__).parent/"JSON"/"templates.json"
    with open(filepath, "r") as file:
        data = json.load(file).get(template)
    return data

def cleanup(project_directory):
    """clean up half-complete project directories"""
    for file in Path(project_directory).iterdir():
        if Path(file).is_file():
            Path(project_directory, file).unlink()
        else:
            cleanup(file)
    Path(project_directory).rmdir()