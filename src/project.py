from __future__ import annotations
import json

from pathlib import Path
from typing import Any, List

import soundfile
from numpy import array

from directories import bsms_directory
from metadata import METADATATEMPLATE, Metadata
from timeline import TIMELINETEMPLATE, Timeline


class Project:
    def __init__(self, name: str):
        self.name = name
        self.filepath = Path(bsms_directory("Projects", f"{name}"))
        if not self.filepath.exists():
            self.filepath.mkdir()
            
        # Create base project files
        for file in [["timeline.json", TIMELINETEMPLATE], ["metadata.json", METADATATEMPLATE]]:
            if not (self.filepath/file[0]).exists():
                self.write_json(file[0], file[1])
            
        self.metadata = Metadata(self)
        self.timeline = Timeline(self)
    
    def namelist(self) -> List[str]:
        return self.filepath.iterdir()

    def write_json(self, filename: str, data: Any, indent: int=None) -> bool:
        with open(self.filepath/filename, "w") as file:
            json.dump(data, file, indent=indent)
        return True

    def read_json(self, filename: str) -> Any:
        with open(self.filepath/filename, "r") as file:
            return json.load(file)
        
    def write_audio(self, filename: str, data: array, samplerate: int) -> bool:
        filename = self.metadata.get("_songFilename", "song.wav") if filename is None else filename
        soundfile.write(self.filepath/filename, data, samplerate)
        return True
    
    def read_audio(self, filename: str=None) -> object:
        filename = self.metadata.get("_songFilename", "song.wav") if filename is None else filename
        return soundfile.read(self.filepath/filename)

def main():
    project = Project("test")
    project.metadata.update({"_songName": "hello_world"})
    project.metadata.save()
    
if __name__ == "__main__":
    main()
