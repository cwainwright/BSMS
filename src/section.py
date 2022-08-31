from typing import Union

from robject import Rhythm, Rest


class Section:
    """Section object for organising robjects"""

    def __init__(self, section_name: str):
        self.section_name = section_name.split(" ")[0].title()
        self.contents: list(Union(Rhythm, Rest)) = []
        self.selected_index = None

    def __iter__(self) -> list:
        return self.contents

    def __str__(self) -> str:
        return f"{self.section_name}"

    def __repr__(self) -> str:
        return f"Section: {self.section_name}"

    @property
    def dict(self) -> dict:
        """Return Section as Dictionary"""
        contents = []
        for robject in self.contents:
            contents.append(robject.ref)
        return {"name": self.section_name, "contents": contents}

    def add_robject(self, robject: Union[Rhythm, Rest]) -> bool:
        """Add RObject to Section"""
        self.contents.append(robject)
        return True

    def new_rest(self, robject_id: str, duration: float) -> bool:
        """Add Rest to Section (without accessing Rest Type)"""
        return self.add_robject(Rest(robject_id, "[]", duration))

    def new_rhythm(
        self,
        robject_id: str,
        robject_category: str,
        duration: float,
        note_data: list = None,
        mirror: bool = False,
    ) -> bool:
        """Add Rhythm to Section (without accessing Rhythm Type)"""
        if note_data is None:
            note_data = []
        return self.add_robject(
            Rhythm(robject_id, robject_category, duration, note_data, mirror)
        )

    def remove_robject(self, index: int) -> bool:
        """Remove RObject from Section"""
        if index < len(self.contents):
            self.contents.pop(index)
            return True
        return False
