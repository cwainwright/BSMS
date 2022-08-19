import json
from pathlib import Path
from typing import Any
from files import get_template

class Preferences:
    def __init__(self) -> None:
        self.filepath = Path(__file__).parent/"JSON"/"preferences.json"
        self.data = get_template("preferences")
        self.last_update = self.filepath.stat().st_mtime
        if not self.filepath.exists():
            with open(self.filepath, "w") as file:
                json.dump(self.data, file)
        else:
            with open(self.filepath, "r") as file:
                self.data = json.load(file)

    def get(self, __key: Any, __default: Any=None) -> Any:
        if self.last_update < self.filepath.stat().st_mtime:
            with open(self.filepath, "r") as file:
                self.data = json.load(file)
            self.last_update = self.filepath.stat().st_mtime
        return self.data.get(__key, __default)
    
    def update(self, info: dict) -> None:
        self.data.update(info)
        with open(self.filepath, "w") as file:
            json.dump(self.data, file)
        self.last_update = self.filepath.stat().st_mtime
        

    # Home Directory Getter and Setter
    @property
    def home_directory(self) -> Path:
        if str(self.get("home_directory")).startswith("~"):
            filepath = Path(str(self.get("home_directory")).replace("~", str(Path.home())))
        else:
            filepath = Path(self.get("home_directory"))
        return filepath
    
    @home_directory.setter
    def home_directory(self, __value:str):
        if __value.startswith(Path.home()):
            __value = __value.replace()(Path.home(), "~")
        self.update({"home_directory": __value})
        with open(self.filepath, "w") as file:
            json.dump(self.data, file)
    
    # Project Directory Getter
    @property
    def project_directory(self) -> Path:
        return self.home_directory/"Projects"
    
    # Robject Directory Getter
    @property
    def robject_directory(self) -> Path:
        return self.home_directory/"Robjects"
    
    # Export Directory Getter and Setter
    @property
    def export_directory(self) -> Path:
        return Path(self.get("export_directory"))
    
    @export_directory.setter
    def export_directory(self, __value:str):
        self.update({"export_directory": __value})
        with open(self.filepath, "w") as file:
            json.dump(self.data, file)
            
PREFERENCES = Preferences()