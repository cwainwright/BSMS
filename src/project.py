from __future__ import annotations

import json
from pathlib import Path
import shutil
from typing import Union

import soundfile
import numpy

from metadata import Metadata
from preferences import PREFERENCES
from timeline import Characteristic, Difficulty, Timeline



class Project:
    def __init__(self, name: str):
        # Create directory if it doesn't exist
        self.name: str = name
        self.filepath: Path = PREFERENCES.project_directory / self.name
        if not self.filepath.exists():
            self.filepath.mkdir(parents=True)

        self.metadata = Metadata(self)
        self.timelines: list(Timeline) = []

        delim = PREFERENCES.timeline_delim
        for file in self.filepath.iterdir():
            if file.suffix == ".timeline":
                characteristic, difficulty = file.stem.split(delim)
                # Try loading timeline
                try:
                    characteristic_index = [member for member in Characteristic.__members__].index(characteristic.upper())
                    characteristic = Characteristic(characteristic_index)

                    difficulty_index = [member for member in Difficulty.__members__].index(difficulty.upper())
                    difficulty = Difficulty(difficulty_index)                
                    
                    self.timelines.append(Timeline(self, characteristic, difficulty))
                # If timeline not recognised throw error
                except ValueError:
                    ValueError(f"{file.stem} characteristic or difficulty not recognised!")

        if len(self.timelines) == 0:
            self.timelines.append(Timeline(self, Characteristic.STANDARD, Difficulty.EASY))
            
        self.characteristic = self.timelines[-1].characteristic
        self.difficulty = self.timelines[-1].difficulty

    @property
    def namelist(self) -> list[str]:
        return [file.name for file in self.filepath.iterdir()]
    
    @property
    def current_timeline(self) -> Timeline:
        index = [timeline.id() for timeline in self.timelines].index((self.characteristic, self.difficulty))
        return self.timelines[index]
 
    def set_timeline(self, characteristic: Union(int, Characteristic), difficulty: Union(int, Difficulty)) -> Timeline:
        if self.current_timeline.empty():
            self.timelines.remove(self.current_timeline)
            
        # Reset Characteristic and Difficulty
        if isinstance(characteristic, int):
            characteristic = Characteristic(characteristic)
        self.characteristic = characteristic
        if isinstance(difficulty, int):
            difficulty = Difficulty(difficulty)
        self.difficulty = difficulty

        # If timeline exists:
        if (characteristic, difficulty) in [timeline.id() for timeline in self.timelines]:
            index = [timeline.id() for timeline in self.timelines].index((characteristic, difficulty))
            return self.timelines[index]

        # If timeline does not exist:
        else:
            self.timelines.append(Timeline(self, characteristic, difficulty))
            return self.timelines[-1]

    def write_json(self, filename: str, data: object, indent: int = None) -> bool:
        with open(self.filepath / filename, "w") as file:
            json.dump(data, file, indent=indent)
        return True

    def read_json(self, filename: str) -> dict:
        with open(self.filepath / filename, "r") as file:
            return json.load(file)

    def write_audio(self, filename: str, data: numpy.array, samplerate: int) -> bool:
        if filename is None:
            filename = self.metadata.get("_songFilename", "song.wav")
        else:
            self.metadata.set("_songFilename", filename)
        soundfile.write(self.filepath / filename, data, samplerate)
        return True

    def read_audio(self, filename: str = None) -> object:
        filename = (
            self.metadata.get("_songFilename", "song.wav")
            if filename is None
            else filename
        )
        return soundfile.read(self.filepath / filename)

    def sub_dir(self, name: str) -> Path:
        if name not in self.filepath.iterdir():
            (self.filepath / name).mkdir()
        return self.filepath / name

    def delete(self) -> None:
        shutil.rmtree(self.filepath)