from json import dumps, load

from rhythms import Rest, construct_robject

try:
    from src.directory_operations import logger
    from src.rhythms import Rhythm, Rest, save_rest
except ModuleNotFoundError:
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

    def add_robject(self, robject) -> bool:
        """Add RObject to Section"""
        self.contents.append(robject)
        return True

    def remove_robject(self, index) -> bool:
        """Remove RObject from Section"""
        self.contents.pop(index)
        return True


class Timeline:
    def __init__(self, project):
        self.project = project
        self.sections = []
        if "timeline.json" not in self.project.zip.namelist():
            beat_offset = project.info.get("_beatOffset", 0)
            save_rest(beat_offset)
            timeline_template.get("sections")[0].get("contents").append(Rest(f"{beat_offset} beats", "Custom").to_dict())
            with self.project.zip.open("timeline.json", "w") as timeline_file:
                timeline_file.write(dumps(timeline_template, indent=2).encode("utf-8"))
        self.load()

    def load(self) -> bool:
        with self.project.zip.open("timeline.json", "r") as timeline_file:
            print(timeline_file)
            timeline_dict = load(timeline_file)
            for section in timeline_dict.get("sections"):
                section_object = Section(section.get("name"))
                for r in section.get("contents", []):
                    robject = construct_robject(r.get("robject_id"), r.get("robject_category"), r.get("mirror", None))
                    section_object.add_robject(robject)
                self.add_section(section_object)
        return True

    def save(self) -> bool:
        with self.project.zip.open("timeline.json", "w") as timeline_file:
            timeline = timeline_template.update({"sections": [section.to_dict() for section in self.sections]})
            timeline_file.write(dumps(timeline, indent=2).encode("utf-8"))
        return True

    def get_section(self, section_index: int) -> Section:
        return self.sections[section_index]

    def add_section(self, section: Section) -> bool:
        self.sections.append(section)
        return True
    
    def remove_section(self, section: Section) -> bool:
        try:
            self.sections.remove(section)
        except ValueError:
            return False
        return True

    def pop_section(self, section_index: int) -> bool:
        try:
            self.sections.pop(section_index)
        except IndexError:
            return False
        return True


timeline_template = load(open("src/templates.json", "r")).get("timeline")

if __name__ == "__main__":
    from project import Project
    timeline = Timeline(Project("test"))
    print(timeline.get_section(0))
    print(timeline.get_section(0).to_dict())