from json import dumps, load

from rhythms import Rest

try:
    from src.directory_operations import logger
    from src.rhythms import Rhythm, Rest
except ModuleNotFoundError:
    from directory_operations import logger
    from rhythms import Rhythm, Rest


class Timeline:
    def __init__(self, project):
        self.project = project
        self.sections = []
        if "timeline.json" not in self.project.zip.namelist():
            beat_offset = project.info.get("_beatOffset", 0)
            timeline_template.get("sections")[0].get("contents").append(Rest("Sync Rest", beat_offset).get_dict())
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
                    if r["robject_category"] == "Rest":
                        robject = Rest(**r)
                    else:
                        robject = Rhythm(**r)
                    section_object.add_robject(robject)
                self.add_section(section_object)
        return True

    def save(self) -> bool:
        with self.project.zip.open("timeline.json", "w") as timeline_file:
            timeline = timeline_template.update({"sections": [section.to_dict() for section in self.sections]})
            timeline_file.write(dumps(timeline, indent=2).encode("utf-8"))
        return True

    def add_section(self, section) -> bool:
        self.sections.append(section)
        return True
    
    def remove_section(self, section_index) -> bool:
        try:
            self.sections.pop(section_index)
        except IndexError:
            return False
        return True

    def add_rhythm(self, section_index, rhythm) -> bool:
        try:
            self.sections[section_index].add_robject(rhythm)
        except IndexError:
            return False
        return True

    def remove_rhythm(self, section_index, rhythm_index) -> bool:
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

    def to_dict(self) -> dict:
        """Return Section as Dictionary"""
        return {"name": self.section_type, "contents": [dict(rhythm) for rhythm in self.contents]}

    def add_robject(self, rhythm) -> bool:
        """Add Rhythm to Section"""
        self.contents.append(rhythm)
        return True

    def remove_robject(self, index) -> bool:
        """Remove Rhythm from Section"""
        self.contents.pop(index)
        return True


timeline_template = load(open("src/templates.json", "r")).get("timeline")

if __name__ == "__main__":
    from project import Project
    timeline = Timeline(Project("test"))