import json
from pathlib import Path
from files import get_template

class Preferences:
    def __init__(self) -> None:
        self.filepath = Path(__file__).parent/"JSON"/"preferences.json"
        if not self.filepath.exists():
            self.data = get_template("preferences")
            with open(self.filepath, "w") as file:
                json.dump(self.data, file)
        else:
            with open(self.filepath, "r") as file:
                self.data = json.load(self.data)

    # Home Directory Getter and Setter
    @property
    def home_directory(self) -> Path:
        return Path(self.data.get("home_directory"))
    
    @home_directory.setter
    def home_directory(self, __value):
        self.data.update({"home_directory": __value})
        with open(self.filepath, "w") as file:
            json.dump(self.data, file)
    
    # Export Directory Getter and Setter
    @property
    def export_directory(self) -> Path:
        return Path(self.data.get("export_directory"))
    
    @export_directory.setter
    def export_directory(self, __value):
        self.data.update({"export_directory": __value})
        with open(self.filepath, "w") as file:
            json.dump(self.data, file)
            
PREFERENCES = Preferences()