from zipfile import ZipFile, BadZipfile
from os import path

from timeline import Timeline
from info import Info
from directory_operations import bsms_directory, logger

class Project:
    def __init__(self, name: str):
        self.name = name
        if not path.exists(self.filepath):
            self.info = Info(self)
            self.timeline = Timeline(self)
        elif self.read.testzip() is None:
            self.info = Info(self)
            self.timeline = Timeline(self)
        else:
            logger.error("Project: Zipfile is corrupt")
            raise BadZipfile

    @property
    def filepath(self):
        return bsms_directory("Projects", self.name + ".zip")

    @property
    def write(self) -> ZipFile:
        return ZipFile(self.filepath, "w")

    @property
    def append(self) -> ZipFile:
        return ZipFile(self.filepath, "a")

    @property
    def read(self) -> ZipFile:
        try:
            return ZipFile(self.filepath, "r")
        except FileNotFoundError:
            ZipFile(self.filepath, "w")
            return ZipFile(self.filepath, "r")


if __name__ == "__main__":
    project = Project("test")
    project.info.update({"_songFilename": "hello_world"})