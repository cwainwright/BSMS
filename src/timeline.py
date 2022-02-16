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
            for section in load(timeline_file).get("sections"):
                self.sections.append(Section(section["name"]))
                for robject in section["contents"]:
                    self.sections[-1].add_robject(Rhythm(*robject))

    def save(self):
        with self.project.zip.open("timeline.json", "w") as timeline_file:
            timeline_file.write(dumps({"sections": [dict(section) for section in self.sections]}))

    def add_section(self, section_name):
        self.sections.append(Section(section_name))
        self.save()
    
    def remove_section(self, section_name):
        self.sections.remove(section_name)
        self.save()

    def add_rhythm(self, section_index, rhythm):
        try:
            self.sections[section_index].add_robject(rhythm)
        except IndexError:
            return False
        return True

    def remove_rhythm(self, section_index, rhythm_index):
        try:
            self.sections[section_index].remove_robject(rhythm_index)
        except IndexError:
            return False
        return True


class Section():
    """Section Object, contains Rhythms and Rests"""
    def __init__(self, section_type: str):
        self.section_type = section_type.split(" ")[0].title()
        self.contents = []

    def __iter__(self) -> list:
        return self.contents

    def __str__(self) -> str:
        return f"{self.section_type}"

    def __repr__(self) -> str:
        return f"Section: {self.section_type}"

    def add_robject(self, rhythm):
        """Add Rhythm to Section"""
        self.contents.append(rhythm)
        return True

    def remove_robject(self, index):
        """Remove Rhythm from Section"""
        self.contents.pop(index)
        return True

    def __dict__(self):
        """Return Section as Dictionary"""
        return {"name": self.section_type, "contents": [dict(rhythm) for rhythm in self.contents]}


timeline_template = load(open("src/templates.json", "r")).get("timeline")