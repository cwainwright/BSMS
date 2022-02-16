"""Management of preset Rhythms"""
from copy import deepcopy
from json import dump, load
from os import listdir, mkdir, path

from directory_operations import logger, rhythm_directory, rest_directory

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

class RObject():
    """Template for Rhythm and Rest Objects"""
    def __init__(
            self,
            rhythm_id,
            rhythm_category,
            mirror = False,
            duration = None
    ):
        self.rhythm_id = rhythm_id
        self.rhythm_category = rhythm_category
        self.mirror = mirror
        self.duration = duration
        self.note_data = []

    def __dict__(self) -> dict:
        """Return RObject as dictionary"""
        return {"rhythm_id": self.rhythm_id, "rhythm_category": self.rhythm_category, "mirror": self.mirror}

    def __str__(self) -> str:
        return f"{self.rhythm_id}, {self.rhythm_category}"

    def __repr__(self) -> str:
        return f"{self.note_data}"

    def __iter__(self) -> list:
        return [self.rhythm_id, self.rhythm_category]



class Rhythm(RObject):
    """Rhythm Object"""
    def __init__(self, rhythm_id, rhythm_category, mirror, rhythm_data = None):
        super().__init__(rhythm_id, rhythm_category, mirror)
        if rhythm_data is None:
            self.rhythm_data = self.load_data()
        else:
            self.rhythm_data = rhythm_data

    def update_data(self, rhythm_data) -> bool:
        """Update Rhythm data"""
        self.rhythm_data = rhythm_data
        return self.save_data()

    def load_data(self) -> dict:
        """Load Rhythm data from JSON"""
        try:
            with open(rhythm_directory(self.rhythm_category, self.rhythm_id), "r") as rhythm_file:
                rhythm_data = dict(load(rhythm_file))
        except FileNotFoundError:
            logger.critical(f"Rhythm file {self.rhythm_id + self.rhythm_category} not found")
            raise FileNotFoundError
        logger.info(f"Rhythm file {self.rhythm_id + self.rhythm_category} loaded")
        return rhythm_data

    def save_data(self) -> bool:
        """Save Rhythm data to JSON"""
        with open(rhythm_directory(self.rhythm_category, self.rhythm_id), "w") as rhythm_file:
            dump(self.rhythm_data, rhythm_file)
        return True


class Rest(RObject):
    """Rest Object"""
    def __init__(self, rest_id, duration):
        super().__init__(rest_id, "Rest", mirror=False, duration=duration)
        self.rhythm_data = self.load_data()

    def load_data(self) -> dict:
        return {"note_data": [], "duration": self.duration}

    def save_data(self) -> bool:
        with open(rest_directory(self.rhythm_id), "w") as rest_file:
            dump(self.rhythm_data, rest_file)
        return True


# Finds intervals between each rhythm
def rhythm_intervals(data, duration):
    """return rhythm_intervals"""
    copied_data = deepcopy(data)
    copied_data.append({"_time": duration})
    intervals = []
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
    return intervals

# Imports rhythm
# Gathering metadata and organising
# into category based on intervals between notes
def rhythm_load(filepath=None):
    """rhythm load function"""
    with open(filepath, "r") as rhythm_import_file:
        rhythm_data = load(rhythm_import_file)

    # If note_data exists, sort it ready for upcoming functions
    if rhythm_data["note_data"] != []:
        sorted(rhythm_data["note_data"], key=lambda note: note.get("_time"))
    rhythm_id = filepath.split("/")[-1]
    rhythm_category = str(rhythm_intervals(
        rhythm_data["note_data"],
        rhythm_data["duration"]
    ))
    # If category generated does not already exist, create new directory
    if rhythm_category not in listdir(rhythm_directory()):
        logger.info(
            msg="rhythm_category does not exist - creating new directory..."
        )
        mkdir(rhythm_directory(rhythm_category))
        return (
            True,
            {
                "rhythm_id":rhythm_id,
                "rhythm_category":rhythm_category,
                "rhythm_data":rhythm_data
            }
        )
    # If rhythm already exists in category, pause import
    elif rhythm_id in listdir(rhythm_directory(rhythm_category)):
        return (
            False,
            {
                "rhythm_id":rhythm_id,
                "rhythm_category":rhythm_category,
                "rhythm_data":rhythm_data
            }
        )
    else:
        return (
            True,
            {
                "rhythm_id":rhythm_id,
                "rhythm_category":rhythm_category,
                "rhythm_data":rhythm_data
            }
        )

def rhythm_save(rhythm_id, rhythm_category, rhythm_data):
    """rhythm save function"""
    # Otherwise import rhythm using category and
    # ID obtained from previous functions
    rhythm_file_id = rhythm_directory(rhythm_category, rhythm_id)
    with open(rhythm_file_id, "w") as rhythm_file:
        dump(rhythm_data, rhythm_file, indent=4)
    logger.info(
        msg="Rhythm sucessfully imported"
    )
    return True

# Get duration of rhythm file
def get_rhythm_duration(rhythm_id, rhythm_category):
    """return rhythm duration"""
    rhythm_file_id = path.join(
        path.expanduser('~'),
        "Documents", "BSMS", "Rhythms",
        rhythm_category,
        rhythm_id
    )
    logger.info(
        msg="Searching for %s" % rhythm_file_id
    )
    with open(rhythm_file_id, "r") as rhythm_file:
        rhythm_data = load(rhythm_file)
    logger.info(
        msg="returning Rhythm duration..."
    )
    return float(rhythm_data["duration"])
