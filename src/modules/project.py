from zipfile import ZipFile, BadZipfile
from os import path
from zipfile import ZipFile

try:
    from src.modules.timeline import Timeline
    from src.modules.info import Info
    from src.modules.directory_operations import bsms_directory, logger
except ModuleNotFoundError:
    from timeline import Timeline
    from info import Info
    from directory_operations import bsms_directory, logger

class Project:
    def __init__(self, name: str):
        self.filepath = bsms_directory("Projects", name + ".zip")
        if self.zipfile.testzip() is None:
            self.info = Info(self)
            # self.timeline = Timeline(self)
        else:
            logger.error("Project: Zipfile is corrupt")
            raise BadZipfile
    
    @property
    def zipfile(self) -> ZipFile:
        return ZipFile(self.filepath)


if __name__ == "__main__":
    project = Project("test")