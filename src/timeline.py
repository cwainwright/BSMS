import json
from copy import deepcopy

import files
from preferences import PREFERENCES
from robject import load_robject, restore_robject
from section import Section

TIMELINETEMPLATE = files.get_template("timeline")


class Timeline:
    def __init__(self, project, characteristic: str, difficulty: str):
        self.__project = project
        self.characteristic = characteristic
        self.difficulty = difficulty
        self.sections: list(Section) = []
        self.selected_section: int = None
        self.selected_robject: int = None
        self.robject_backup: dict = []
        if self.filename not in self.__project.namelist:
            with open(self.__project.filepath / self.filename, "w") as file:
                json.dump(TIMELINETEMPLATE, file, indent=4)
        self.load()

    @property
    def filename(self) -> str:
        return f"{self.characteristic}{PREFERENCES.timeline_delim}{self.difficulty}.timeline"

    def __getitem__(self, index: int) -> Section:
        return self.sections[index]

    def load(self):
        """Load Timeline from Project"""
        timeline_file = self.__project.read_json(self.filename)

        # Load main timeline
        for section_data in timeline_file.get("sections", []):
            section = Section(section_data.get("name"))
            for robject_data in section_data.get("contents", []):
                id = robject_data.get("robject_id")
                category = robject_data.get("robject_category")
                mirror = robject_data.get("mirror", False)
                robject = load_robject(id, category, mirror)
                if robject is None:
                    robject = restore_robject(self.robject_backup, id, category, mirror)
                section.add_robject(robject)
            self.add_section(section)

        # Load robject backups
        self.robject_backup = timeline_file.get("robject_backup", [])

    def save(self):
        """Save Timeline to Project"""
        data = deepcopy(TIMELINETEMPLATE)

        # Saving sections
        section_data = []
        for section in self.sections:
            section_data.append(section.dict)
        data.update({"sections": section_data})

        # Saving robject backups
        robject_backup = []
        for section in self.sections:
            for robject in section.contents:
                robject_backup.append(robject.dict)
        data.update({"robject_backup": robject_backup})

        # Save to project
        self.__project.write_json(self.filename, data, indent=2)

    def add_section(self, section: Section) -> int:
        """Add Section to Timeline"""
        self.sections.append(section)
        return len(self.sections)-1

    def new_section(self, name: str) -> int:
        """Add Section to Timeline (without accessing Section type)"""
        return self.add_section(Section(name))

    def remove_section(self, index: int) -> int:
        """Remove Section from Timeline"""
        if index < len(self.sections):
            self.sections.pop(index)
            return True
        return False

    def export_timeline(self) -> dict:
        self.__project.sub_dir("beatmap_data")


if __name__ == "__main__":
    from project import main

    main()
