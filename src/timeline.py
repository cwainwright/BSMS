from json import dump, load
from os import path

from src.directory_operations import logger
from src.project import Project
from src.rhythms import Rhythm


class Timeline:
    def __init__(self, project: Project):
        self.project = project
        self.sections = []
        self.length = None
    
    def load(self):
        try:
            with open(path.join(self.project.filepath, "timeline.json"), "r") as timeline_file:
                timeline = dict(load(timeline_file))
            logger.info("Timeline loaded")
            return timeline
        except FileNotFoundError:
            logger.warning("Timeline file not found")
            return {"sections": [], "length": 0.0}

    def save(self):
        logger.info("Saving timeline...")
        with open(path.join(self.project.filepath, "timeline.json"), "w") as timeline_file:
            dump({"sections": self.sections, "length": self.length}, timeline_file)
    
    def add_section(self, name: str, index: int):
        section = {"name": name, "rhythms": []}
        self.sections.append(section)
        return True

    def add_rhythm(self, rhythm: Rhythm, section_index: int):
        self.sections[section_index]["rhythms"].append(rhythm)
        return True
