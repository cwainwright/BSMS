"""Management of preset Rhythms"""
from copy import deepcopy
from json import dump, load
from os import listdir, mkdir, path
import logging

logging.basicConfig(
    format="%(asctime)s %(levelname)s: %(message)s",
    filename=path.join(
        "logs",
        f"{__name__}.log"
    ),
    filemode="a"
)

logger = logging.getLogger(__name__)

# Each rhythm will be stored within its own JSON file
def rhythm_directory(category = None, rhythm_id = None):
    """Returns rhythm directory"""
    if category is None:
        filepath = path.join(
            path.expanduser('~'),
            "Documents",
            "BSMS",
            "Rhythms"
        )
    elif rhythm_id is None:
        filepath = path.join(
            path.expanduser('~'),
            "Documents",
            "BSMS",
            "Rhythms",
            category
        )
    else:
        filepath = path.join(
            path.expanduser('~'),
            "Documents",
            "BSMS",
            "Rhythms",
            category,
            rhythm_id
        )
    return filepath

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

class RhythmTemplate():
    """Template for Rhythm and Rest Objects"""
    def __init__(
            self,
            rhythm_id,
            rhythm_category,
            start_time,
            mirror,
            duration = None
    ):
        self.rhythm_category = rhythm_category
        self.start_time = start_time
        self.mirror = mirror
        self.duration = duration
        if rhythm_id == "Rest":
            self.rhythm_id = rhythm_id
            self.note_data = []
        else:
            self.rhythm_id = rhythm_id.strip(".json")
            self.rhythm_file_id = rhythm_directory(
                self.rhythm_category,
                self.rhythm_id+".json"
            )

            category_path = rhythm_directory(self.rhythm_category)
            logger.info(
                    msg=f"Checking for: {category_path}"
                )
            if not path.exists(category_path):
                logger.info(
                    msg=f"Category could not be found ({self.rhythm_category})"
                )
                raise FileNotFoundError("Category could not be found")

            logger.info(
                    msg=f"Checking for: {self.rhythm_file_id}"
                )
            if not path.exists(self.rhythm_file_id):
                logger.critical(
                    msg=f"Rhythm could not be found in category ({self.rhythm_id}.json)"
                )
                raise FileNotFoundError("Rhythm could not be found in category")

            with open(self.rhythm_file_id, "r") as rhythm_file:
                rhythm_data = load(rhythm_file)
                self.note_data = rhythm_data["note_data"]
                self.duration = rhythm_data["duration"]

    def get_data_list(self):
        """get list of data for display in timeline tree"""
        start_time_string = "[%s]" % self.start_time
        if self.rhythm_id == "Rest":
            name_string = "%s beats" % self.duration
            type_string = "Rest"
        else:
            name_string = str(self.rhythm_id)
            type_string = "Rhythm"
        if self.rhythm_category is None:
            category_string = "N/A"
        else:
            category_string = str(self.rhythm_category)
        return (
            start_time_string,
            name_string,
            category_string,
            type_string,
            str(float(self.duration))
        )

    def get_start_time(self):
        """return start_time"""
        return self.start_time

    def get_end_time(self):
        """return start_time + duration"""
        return self.start_time + self.duration

    def __normalise(self, data):
        """return normalised items"""
        logger.info(
            msg=f"{str(self.identify())}, normalising..."
        )
        normalised_items = deepcopy(data)
        for item in normalised_items:
            if self.mirror:
                item["_lineIndex"] = 3-item["_lineIndex"]
                if item["_type"] != 3:
                    item["_type"] = 1 - item["_type"]
                if item["_cutDirection"] not in [0, 1, 8]:
                    if item["_cutDirection"]%2==0:
                        item["_cutDirection"] += 1
                    else:
                        item["_cutDirection"] -= 1
            item["_time"] += self.start_time
        return normalised_items

    def normalise_notes(self):
        """return normalised notes"""
        return self.__normalise(self.note_data)

    def identify(self):
        """return rhythm_id and rhythm_category"""
        return (self.rhythm_id, self.rhythm_category)

    def dump_data(self):
        """return additional rhythm information"""
        logger.info(
            msg="returning rhythm data..."
        )
        return {
            "rhythm_id":self.rhythm_id,
            "rhythm_category":self.rhythm_category,
            "start_time":self.start_time,
            "mirror":self.mirror,
            "duration":self.duration
        }

class Rhythm(RhythmTemplate):
    """Storage method of rhythm file"""
    # Initialise on addition into timeline
    def __init__(
        self, rhythm_id, rhythm_category,
        start_time = None, mirror = False
    ):
        super().__init__(rhythm_id, rhythm_category, start_time, mirror)
        logger.info(
            msg=f"Rhythm object initialised ["
            + f"{self.rhythm_id}, {self.rhythm_category}, "
            + f"{self.start_time}, {self.mirror}"
            + "]"
        )

class Rest(RhythmTemplate):
    """Rest - an empty Rhythm"""
    def __init__(
        self, start_time = None, duration = 4, rhythm_category = None
    ):
        super().__init__("Rest", rhythm_category, start_time, False, duration)
        logger.info(
            msg="Rest object initialised ["
            + f"{self.rhythm_id}, {self.rhythm_category}, "
            + f"{self.start_time}, {self.duration}"
            + "]"
        )


# Add additional functions required for Rest to be parsed as empty Rhythm


# Generate unique identifier for rhythm
def generate_rhthm_id(data):
    """generate_rhythm_id (depreciated)"""
    rhythm_id = ""
    # Left, Right, Unused, Bomb
    note_type_data = ["L", "R", "U", "B"]
    for note in data["note_data"]:
        section = str(note["_time"])
        section += str(note["_lineIndex"])
        section += str(note["_lineLayer"])
        section += str(note_type_data[note["_type"]])
        section += str(note["_cutDirection"])
        rhythm_id += section
    logger.info(
        msg="returning ID..."
    )
    return rhythm_id

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
