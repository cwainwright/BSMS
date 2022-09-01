import json
from enum import Enum

from preferences import PREFERENCES

class RObject_Type(Enum):
    ANY = 0
    RHYTHM = 1
    REST = 2

class RObject():
    """Parent class/protocol for Rhythm and Rest Objects"""
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
        return self.note_data
    
    def type(self) -> RObject_Type:
        if self.robject_category == "[]":
            return RObject_Type.REST
        else:
            return RObject_Type.RHYTHM
        
    
    @property
    def ref(self) -> dict:
        """Reference dictionary

        Returns:
            dict: reference robject data (for use in timeline sections)
        """
        return {
            "robject_id": self.robject_id,
            "robject_category": self.robject_category,
            "mirror": self.mirror
        }
    
    @property
    def dict(self) -> dict:
        """Data dictionary

        Returns:
            dict: full robject data (for use when restoring RObject)
        """
        return {
            "robject_id": self.robject_id,
            "robject_category": self.robject_category,
            "robject_data": {
                "note_data": self.note_data,
                "duration": self.duration
            }
        }

class Rhythm(RObject):
    """Rhythm Object"""
    def __init__(
        self,
        robject_id: str,
        robject_category: str,
        duration: float,
        note_data: list,
        mirror: bool
    ):
        super().__init__(robject_id, robject_category, duration, note_data, mirror)
        
class Rest(RObject):
    """Rest Object"""
    def __init__(
        self,
        robject_id: str,
        robject_category: str,
        duration: float
    ):
        super().__init__(robject_id, robject_category, duration, None, False)
        
def load_robject(robject_id: str, robject_category: str, mirror: bool = False) -> RObject:
    """Load robject from JSON file"""
    filepath = PREFERENCES.robject_directory/robject_category/(robject_id+".json")
    if filepath.exists():
        with open(filepath, "r") as file:
            data = json.load(file)
        if robject_category in ("[]", "Rest"):
            robject = Rest(
                robject_id,
                "[]",
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
    return None

def restore_robject(robjects, robject_id, robject_category, mirror=False) -> RObject:
        """Restore Robject from Backup"""
        for robject in robjects:
            if all([
                robject.get("robject_id") == robject_id,
                robject.get("robject_category") == robject_category
            ]):
                    
                robject_data = robject.get("robject_data")
                category_filepath = PREFERENCES.robject_directory/robject_category
                if not category_filepath.exists():
                    (category_filepath).mkdir()
                with open(category_filepath/(robject_id+".json"), "w") as file:
                    json.dump(robject_data, file)
                return load_robject(robject_id, robject_category, mirror)
        raise Exception("No backup found for RObject")

if __name__ == "__main__":
    print(RObject_Type(0))
    print(RObject_Type(1))
    print(RObject_Type(2))