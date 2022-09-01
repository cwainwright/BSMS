from genericpath import isdir
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
        return Path(self.get("home_directory")).expanduser().resolve()
    
    @home_directory.setter
    def home_directory(self, __value:str):
        self.update({"home_directory": __value})
    
    # Project Directory Getter
    @property
    def project_directory(self) -> Path:
        return self.home_directory/"Projects"
    
    # Robject Directory Getter
    @property
    def robject_directory(self) -> Path:
        return self.home_directory/"RObjects"
    
    # Export Directory Getter and Setter
    @property
    def export_directory(self) -> Path:
        return Path(self.get("export_directory")).expanduser().resolve()
    
    @export_directory.setter
    def export_directory(self, __value:str):
        if Path(__value).resolve().isdir():
            self.update({"export_directory": __value})

    @property
    def timeline_delim(self) -> str:
        return self.get("timeline_delim", "_")
    
    @timeline_delim.setter
    def timeline_delim(self, __value:str):
        if __value != "":
            self.update({"timeline_delim": __value})
    
    @property
    def start_rest_duration(self) -> float:
        return self.get("start_rest_duration", 4.0)
    
    @start_rest_duration.setter
    def start_rest_duration(self, __value:float):
        if __value >= 1.0:
            self.update({"start_rest_duration": __value})
    
PREFERENCES = Preferences()