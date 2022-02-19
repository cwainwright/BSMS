from zipfile import ZipFile
from os import path

try:
    from src.timeline import Timeline, timeline_template
    from src.info import Info, info_template
    from src.directory_operations import bsms_directory, logger
except ModuleNotFoundError:
    from timeline import Timeline, timeline_template
    from info import Info, info_template
    from directory_operations import bsms_directory, logger

class Project:
    def __init__(self, name: str):
        self.filepath = bsms_directory("Projects", name + ".zip")
        self.zip = ZipFile(self.filepath, "a")
        self.info = Info(self)
        self.timeline = Timeline(self)

        self.image_filepath = path.join(self.filepath, self.info["_coverImageFilename"])
        self.song_filepath = path.join(self.filepath, self.info["_songFilename"])


if __name__ == "__main__":
    project = Project("test")