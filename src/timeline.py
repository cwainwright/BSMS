from copy import deepcopy
from enum import Enum
from typing import List, Tuple

from PyQt6.QtWidgets import QTreeWidget, QTreeWidgetItem

import files
from preferences import PREFERENCES
from robject import load_robject, restore_robject
from section import Section

TIMELINETEMPLATE = files.get_template("timeline")


class Characteristic(Enum):
    STANDARD = 0
    ONESABER = 1
    DEGREES180 = 2
    DEGREES360 = 3


class Difficulty(Enum):
    EASY = 0
    NORMAL = 1
    HARD = 2
    EXPERT = 3
    EXPERTPLUS = 4

    def rank(self):
        return (2 * self.value) - 1


class Timeline:
    def __init__(self, project, characteristic: Characteristic, difficulty: Difficulty):
        self.__project = project
        self.characteristic = characteristic
        self.difficulty = difficulty
        self.sections: list(Section) = []
        self.selected_section: int = None
        self.selected_robject: int = None
        self.robject_backup: dict = []
        if self.filename in self.__project.namelist:
            self.load()
        else:
            intro = Section("Intro").new_rest(
                "Intro Beats", PREFERENCES.start_rest_duration
            )
            self.add_section(intro)

    @property
    def filename(self) -> str:
        return self.__str__() + ".timeline"

    def __len__(self) -> int:
        return len(self.sections)

    def id(self) -> Tuple[Characteristic, Difficulty]:
        return (self.characteristic, self.difficulty)

    def __str__(self) -> str:
        return (
            self.characteristic.name + PREFERENCES.timeline_delim + self.difficulty.name
        )

    def empty(self) -> bool:
        return len(self) == 1 and len(self.sections[0]) == 1

    def load(self):
        """Load Timeline from Project"""
        timeline_file = self.__project.read_json(self.filename)

        # Load robject backups
        self.robject_backup = timeline_file.get("robject_backup", [])

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
        return section

    def new_section(self, name: str) -> int:
        """Add Section to Timeline (without accessing Section type)"""
        return self.add_section(Section(name))

    def remove_section(self, index: int) -> int:
        """Remove Section from Timeline"""
        if index < len(self.sections):
            self.sections.pop(index)
            return True
        return False

    def get_data(self, time: float) -> List[Tuple[float, str, List]]:
        start_time = time
        contents = []
        for section in self.sections:
            contents.append((start_time, section.name, section.apply_time(start_time)))
            start_time += section.duration
        return contents

    def populate_tree(self, tree_widget: QTreeWidget):
        data = self.get_data(0)
        for section in data:
            tree_section = QTreeWidgetItem([str(section[0]), section[1]])
            for robject in section[2]:
                tree_robject = QTreeWidgetItem(
                    [
                        str(robject[0]),
                        robject[1].robject_id,
                        robject[1].robject_category,
                        robject[1].type.name.lower(),
                        str(robject[1].duration),
                    ]
                )
                tree_section.addChild(tree_robject)
            tree_widget.addTopLevelItem(tree_section)
