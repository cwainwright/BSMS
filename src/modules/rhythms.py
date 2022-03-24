"""Management of preset Rhythms"""
from copy import deepcopy
from typing import Union
from json import dump, load
from os import path

try:
    from src.modules.directory_operations import bsms_directory, logger
except ModuleNotFoundError:
    from directory_operations import bsms_directory, logger

"""
Rhythm JSON format
Note: _time key is relative to start of rhythm, not song
{
    note_data: [
        {
            _time: float,
            _lineIndex: int(0 to 3),
            _lineLayer: int(0 to 2),
            _type: int(0, 1, 3),
            _cutDirection: int(0 to 8)
        },...
    ],
    duration: float
}
"""

"""
RObject Timeline Format
{
    "robject_id": str,
    "robject_category": str,
    //Only used for Rhythms
    "mirror": bool
}
"""

# aux_data contains Mirror (bool) or duration
class RObject():
    """Parent class for Rhythm and Rest Objects"""
    def __init__(
            self,
            robject_id: str,
            robject_category: str
    ):
        self.robject_id = robject_id
        self.robject_category = robject_category
        self.note_data = []
    
    def __str__(self) -> str:
        return f"{self.robject_id}, {self.robject_category}"

    def __repr__(self) -> str:
        return f"{self.note_data}"

    def __iter__(self) -> list:
        return [self.robject_id, self.robject_category]


class Rhythm(RObject):
    """Rhythm Object"""
    def __init__(self, robject_id, robject_category):
        super().__init__(robject_id, robject_category)
        self.mirror = False
        self.note_data = []
        self.duration = 4

        # Load method overwrites default note_data and duration
        self.loaded = self.load()

    def load(self) -> bool:
        """Load Rhythm data from JSON"""
        try:
            with open(bsms_directory("Rhythms", self.robject_category, f"{self.robject_id}.json"), "r") as rhythm_file:
                rhythm_data = dict(load(rhythm_file))
        except FileNotFoundError:
            logger.critical(f"Rhythm file {self.robject_id} {self.robject_category} not found")
            return False
        logger.info(f"Rhythm file {self.robject_id} {self.robject_category} loaded")
        self.note_data = rhythm_data.get("note_data")
        self.duration = rhythm_data.get("duration")
        return True

    def to_dict(self) -> dict:
        """Return RObject as dictionary"""
        return {
            "robject_id": self.robject_id,
            "robject_category": self.robject_category,
            "mirror": self.mirror
        }

    def set_mirror(self, value: bool) -> bool:
        """setter for mirror"""
        self.mirror = value
        return True


class Rest(RObject):
    """Rest Object"""
    def __init__(self, robject_id: str, robject_category: str = "Default"):
        super().__init__(robject_id, robject_category)
        self.note_data = []
        self.duration = 4

        # Load method overwrites default duration
        self.loaded = self.load()

    def load(self) -> bool:
        """Load Rest data from JSON"""
        try:
            with open(bsms_directory("Rests", self.robject_category, f"{self.robject_id}.json"), "r") as rest_file:
                rest_data = dict(load(rest_file))
        except FileNotFoundError:
            try:
                if self.robject_category == "Default":
                    with open(bsms_directory("Rests", "Custom", f"{self.robject_id}.json"), "r") as rest_file:
                        rest_data = dict(load(rest_file))
                elif self.robject_category == "Custom":
                    with open(bsms_directory("Rests", "Default", f"{self.robject_id}.json"), "r") as rest_file:
                        rest_data = dict(load(rest_file))
                else:
                    logger.warning(f"Rest Category {self.robject_category} not recognised")
                    return False
            except FileNotFoundError:
                logger.warning(f"Rest file {self.robject_id} {self.robject_category} not found")
                return False
        logger.info(f"Rhythm file {self.robject_id} {self.robject_category} loaded")
        self.note_data = rest_data.get("note_data")
        self.duration = rest_data.get("duration")
        return True

    def to_dict(self) -> dict:
        return {"robject_id": self.robject_id, "robject_category": self.robject_category}

    def set_mirror(self, value: bool) -> bool:
        """Pseudo-setter for mirror"""
        return False



# Save newly created Rest
def save_rest(duration: float):
    """Save Rest to JSON"""
    rest_data = {
        "note_data": [],
        "duration": duration
    }
    with open(bsms_directory("Rests", "Custom", f"{duration} beats.json"), "w") as rest_file:
        dump(rest_data, rest_file)
    logger.info(
        msg="Rest saved to Custom directory"
    )
    return True

# Save newly created Rhythm
def save_rhythm(rhythm_id, note_data, duration):
    """Save Rhythm to JSON"""
    rhythm_data = {
        "note_data": note_data,
        "duration": duration
    }
    rhythm_category = str(rhythm_intervals(note_data, duration))
    with open(bsms_directory("Rhythms", rhythm_category, rhythm_id), "w") as rhythm_file:
        dump(rhythm_data, rhythm_file)
    logger.info(
        msg=f"Rhythm saved to {rhythm_category} directory"
    )
    return True

# Constructs a Rhythm or Rest and returns it
def construct_robject(robject_id: str, robject_category: str, mirror: bool = None) -> Union[Rhythm, Rest]:
    if mirror is None:
        robject = Rest(robject_id, robject_category)
    else:
        robject = Rhythm(robject_id, robject_category)
    return robject

# Finds intervals between each note in a rhythm
def rhythm_intervals(note_data: list, duration: float) -> list:
    """return rhythm_intervals"""
    copied_data = deepcopy(note_data)
    copied_data.append({"_time": duration})
    intervals = []
    if len(copied_data) > 1:
        for index in range(1, len(copied_data)):
            interval = (
                float(copied_data[index]["_time"])
                - float(copied_data[index-1]["_time"])
            )
            if interval != 0:
                intervals.append(
                    interval
                )
        copied_data.pop()
        logger.info(
            msg="returning intervals..."
        )
    else:
        intervals.append(duration)
    return intervals


if __name__ == "__main__":
    rest_one = construct_robject("1 Beats", "Default")
    rest_two = construct_robject("3 Beats", "Custom")
    rhythm_one = construct_robject("Croissant", "[0.5, 0.5, 0.5, 0.5]", True)

    print(rest_one.to_dict())
    print(rest_one.note_data, rest_one.duration)
    print(rest_two.to_dict())
    print(rest_two.note_data, rest_two.duration)
    print(rhythm_one.to_dict())
    print(rhythm_one.note_data, rhythm_one.duration)

    rhythm_one.set_mirror(True)

    print(rhythm_one.to_dict())
