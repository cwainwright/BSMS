from __future__ import annotations

import json
from pathlib import Path
import shutil

import soundfile
import numpy

from metadata import Metadata
from preferences import PREFERENCES
from timeline import Timeline


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
                try:
                    characteristic, difficulty = file.stem.split(delim)
                except ValueError:
                    characteristic = "Normal"
                    difficulty = file.stem
                self.timelines.append(Timeline(self, characteristic, difficulty))

        if len(self.timelines) == 0:
            self.timelines.append(Timeline(self, "Standard", "Easy"))

        self.timelines[-1][0].new_rest(
            "Intro Beats", PREFERENCES.start_rest_duration
        )

    @property
    def namelist(self) -> list[str]:
        return self.filepath.iterdir()

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


def main():
    from section import Section
    from robject import load_robject

    project = Project(name="test", tempo=128, start_beat=4)
    project.metadata["_songName"] = "hello_world"
    project.metadata["_songFilename"] = "hello_world.wav"
    project.metadata.save()
    index = project.timelines[0].add_section(Section("Chorus"))
    project.timelines[0][index].add_robject(
        load_robject("Gallop", "[0.25, 0.25, 0.5]", True)
    )
    project.timelines[0][index].add_robject(load_robject("1 beat", "[]"))
    project.timelines[0].save()
    input("Press enter to delete test project...")

if __name__ == "__main__":
    main()
