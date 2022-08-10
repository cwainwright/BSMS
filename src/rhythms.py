from fcntl import F_SEAL_SEAL
from re import L
from preferences import PREFERENCES
import json

"""Management of preset Rhythms"""

class RObject():
    """Parent class for Rhythm and Rest Objects"""
    def __init__(
            self,
            robject_id: str,
            robject_category: str,
            duration: float,
            note_data: list,
            mirror: bool
    ):
        self.robject_id = robject_id
        self.robject_category = robject_category
        self.duration = duration
        self.note_data = [] if note_data is None else note_data
        self.mirror = mirror
    
    def __str__(self) -> str:
        return f"{self.robject_id}, {self.robject_category}"

    def __repr__(self) -> str:
        return f"{self.note_data}"

    def __iter__(self) -> list:
        return [self.robject_id, self.robject_category]

class Rhythm(RObject):
    """Rhythm Object"""
    def __init__(
            self,
            robject_id: str,
            robject_category: str,
            duration: float,
            note_data: list,
            mirror: bool,
    ):
        super().__init__(robject_id, robject_category, duration, note_data, mirror)
        
class Rest(RObject):
    """Rest Object"""
    def __init__(
            self,
            robject_id: str,
            robject_category: str,
            duration: float,
    ):
        super().__init__(robject_id, robject_category, duration, None, False)
        
def load_robject(robject_id: str, robject_category: str, mirror: bool = False) -> RObject:
    """Load Rhythm Object from JSON file"""
    filepath = PREFERENCES.home_directory/robject_category/robject_id+".json"
    with open(filepath, "r") as file:
        data = json.load(file)
    if robject_category = "[]":
        robject = Rest(
            robject_id,
            robject_category,
            data.get("duration")   
        )
    else:
        robject = Rhythm(
            robject_id,
            robject_category,
            data.get("duration"),
            data.get("note_data"),
            mirror
        )
    return robject