from json import dumps, load
from os import path

try:
    from src.directory_operations import logger
    from src.project import Project
    from src.rhythms import Rhythm
except ModuleNotFoundError:
    from directory_operations import logger
    from rhythms import Rhythm


class Timeline:
    def __init__(self, project):
        self.project = project
        self.sections = []
        if "timeline.json" not in self.project.zip.namelist():
            with self.project.zip.open("timeline.json", "w") as timeline_file:
                timeline_file.write(dumps(timeline_template, indent=2).encode("utf-8"))

    def load(self):
        with self.project.zip.open("timeline.json", "r") as timeline_file:
            self.sections = load(timeline_file).get("sections")

    def save(self):
        with self.project.zip.open("timeline.json", "w") as timeline_file:
            timeline_file.write(dumps({"sections": self.sections}))

    def add_section(self, section_name):
        self.sections.append({"name": section_name, "rhythms": []})
        self.save()
    
    def remove_section(self, section_name):
        self.sections.remove(section_name)

timeline_template = load(open("src/templates.json", "r")).get("timeline")