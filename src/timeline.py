from typing import Union
from json import dumps, loads, load

from directory_operations import logger
from rhythms import Rhythm, Rest, save_rest


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

    def to_dict(self) -> dict:
        """Return Section as Dictionary"""
        return {"name": self.section_type, "contents": [robject.to_dict() for robject in self.contents]}

    def add_robject(self, robject: Union[Rhythm, Rest]) -> bool:
        """Add RObject to Section"""
        self.contents.append(robject)
        return True

    def remove_robject(self, index: int) -> bool:
        """Remove RObject from Section"""
        self.contents.pop(index)
        return True


class Timeline:
    def __init__(self, project):
        self.__project = project
        self.sections = []
        self.load()

    def load(self):
        """Load Timeline from Project"""
        if "timeline.json" in self.__project.read.namelist():
            with self.__project.read.open("timeline.json", "r") as timeline_file:
                for section in loads(timeline_file.read()).get("sections", []):
                    sobject = Section(section.get("name", "default"))
                    for robject in section.get("contents", []):
                        sobject.add_robject(robject)
                    self.add_section(sobject)
        else:
            logger.warning("No timeline.json found in project")
            with self.__project.append.open("timeline.json", "w") as timeline_file:
                timeline_file.write(dumps(timeline_template()).encode("utf-8"), self.__project.name)

    def save(self):
        """Save Timeline to Project"""
        with self.__project.append.open("timeline.json", "w") as timeline_file:
            timeline_file.write(dumps(self.to_dict(), indent=2).encode("utf-8"), self.__project.name)

    def add_section(self, section: Section):
        """Add Section to Timeline"""
        self.sections.append(section)

    def remove_section(self, index: int):
        """Remove Section from Timeline"""
        self.sections.pop(index)
    
    def to_dict(self) -> dict:
        """Return Timeline as Dictionary"""
        dict_timeline = {
            "sections": [section.to_dict() for section in self.sections],
            "rhythms": []
        }
        for section in self.sections:
            for robject in section.contents:
                if isinstance(robject, Rhythm):
                    dict_timeline["rhythms"].append(robject.to_dict())
                elif isinstance(robject, Rest):
                    dict_timeline["rhythms"].append(robject.to_dict())
        return dict_timeline

def timeline_template() -> dict:
    """Return Timeline Template"""
    filepath = "src/modules/templates.json"
    with open(filepath, "r") as template_file:
        return (load(template_file).get("timeline"))

if __name__ == "__main__":
    from project import Project
    project = Project("test")
    project.timeline.add_section(Section("test"))
    project.timeline.save()