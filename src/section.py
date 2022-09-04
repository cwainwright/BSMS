from typing import List, Tuple
from files import get_template

from robject import RObject, Rhythm, Rest, restore_robject


class Section:
    """Section object for organising robjects"""

    def __init__(self, name: str):
        self.name = name.split(" ")[0].title()
        self.contents: list(RObject) = []
        self.selected_index = None

    def __str__(self) -> str:
        return f"{self.name}"

    def __repr__(self) -> str:
        return f"Section: {self.name}"
    
    def __len__(self) -> int:
        return len(self.contents)
    
    @property
    def duration(self) -> dict:
        return sum([robject.duration for robject in self.contents])

    @property
    def dict(self) -> dict:
        """Return Section as Dictionary"""
        contents = []
        for robject in self.contents:
            contents.append(robject.ref)
        return {"name": self.name, "contents": contents}

    def apply_time(self, time: float) -> List[Tuple[float, RObject]]:
        """Apply start time to robjects and return list"""
        start_time = time
        contents = []
        for robject in self.contents:
            contents.append((start_time, robject))
            start_time += robject.duration
        return contents

    def add_robject(self, robject: RObject) -> "Section":
        """Add RObject to Section"""
        self.contents.append(robject)
        return self

    def new_rest(self, robject_id: str, duration: float) -> "Section":
        """Add Rest to Section (without accessing Rest Type)"""
        restore_robject([{
            "robject_id": robject_id,
            "robject_category": "[]",
            "robject_data": {"duration": duration, "note_data": []}
        }], robject_id, "[]")
        return self.add_robject(Rest(robject_id, "[]", duration))

    def new_rhythm(
        self,
        robject_id: str,
        robject_category: str,
        duration: float,
        note_data: list = None,
        mirror: bool = False,
    ) -> "Section":
        """Add Rhythm to Section (without accessing Rhythm Type)"""
        if note_data is None:
            note_data = []
        return self.add_robject(
            Rhythm(robject_id, robject_category, duration, note_data, mirror)
        )

    def remove_robject(self, index: int) -> "Section":
        """Remove RObject from Section"""
        if index < len(self.contents):
            self.contents.pop(index)
        return self
