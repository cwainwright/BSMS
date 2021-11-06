"""Timeline class management and functionality"""
from os import path, chdir
from json import load, dump
from typing import Union

from debug import DebugLog
from rhythms import Rhythm, Rest
from bsms_core import projects_directory


debug_log = DebugLog("timeline.py")

"""
rhythm_index:
Stores all rhythms being actively used in project
list of all rhythms as objects used in project
e.g. [rhythmObject1, rhythmObject2,...]

rhythm_list:
rhythms in a list of dictionaries format which can be stored in a JSON format
list  of all rhythms
e.g.[
        {
            "rhythm_id":rhythm_id,
            "rhythm_category":rhythm_category,
            "start_time":start_time,
            "mirror":mirror
        },...
    ]
"""

class Timeline:
    """Timeline class"""
    def __init__(self, project_name, beat_offset=0):
        # Create filepath
        self.project_filepath = projects_directory(project_name)
        self.timeline_filepath = path.join(
            self.project_filepath,
            "timeline.json"
        )
        # Create new empty timeline file if project timeline file not found
        if not path.exists(self.timeline_filepath):
            debug_log.log(
                "Timeline.__init__()",
                "timeline.json missing"
            )
            with open(self.timeline_filepath, "w") as timeline_file:
                data = {
                    "rhythm_list": [Rest(0, beat_offset).dump_data()],
                }
                dump(data, timeline_file, indent=4)
            debug_log.log(
                "Timeline.__init__()",
                "new timeline created"
            )
        # Load rhythm_index and section_index for editing
        self.rhythm_index = []
        self.load()
        debug_log.log(
            "Timeline.__init__()",
            "Timeline initialised"
        )

    def __len__(self):
        return len(self.rhythm_index)

    def load(self):
        """Loads rhythm_index and section_index from timeline.json"""
        # Load RhythmIndex creating each rhythm object from rhythm_list item
        with open(self.timeline_filepath, "r") as timeline_file:
            data = load(timeline_file)
            rhythm_list = data["rhythm_list"]
            for item in rhythm_list:
                if item["rhythm_id"] == "Rest":
                    self.add_rhythm(Rest(
                        start_time = item["start_time"],
                        duration = item["duration"],
                        rhythm_category = item["rhythm_category"]
                    ))
                else:
                    self.add_rhythm(Rhythm(
                        item["rhythm_id"],
                        item["rhythm_category"],
                        item["start_time"],
                        item["mirror"]
                    ))
        debug_log.log(
            "Timeline.load()",
            "Timeline data loaded"
        )

    def save(self):
        """Saves all changes made in the rhythm_index and section_index"""
        with open(self.timeline_filepath, "w") as timeline_file:
            rhythm_list = []
            self.update_rhythm_start_times()
            self.rhythm_index.sort(key = lambda x: x.start_time)
            for item in self.rhythm_index:
                rhythm_list.append(item.dump_data())
            data = {
                "rhythm_list": rhythm_list
            }
            dump(data, timeline_file, indent=4)
        debug_log.log(
            "Timeline.save()",
            "Timeline data saved to timeline.json"
        )


    # Add Rhythms and Rests to Timeline #

    def update_rhythm_start_times(self, start=None, end=None):
        """Update rhythm.start_time for rhythms in range"""
        start_time = float(0)
        if start is None:
            start = 0
        if end is None:
            end = len(self.rhythm_index)
        for item in self.rhythm_index[start:end]:
            item.start_time = start_time
            start_time += item.duration

    def rhythm_index_duration(self):
        """Summates durations of all rhythms and rests in rhythm_index"""
        total_duration = 0
        for item in self.rhythm_index:
            total_duration += item.duration
        return total_duration

    # Add rhythm to rhythm_index
    def add_rhythm(self, item:Union[Rhythm, Rest]):
        """Add new rhythm to timeline"""
        debug_message = "New item added to end of rhythm_index"
        item.start_time = self.rhythm_index_duration()
        self.rhythm_index.append(item)
        self.rhythm_index.sort(key = lambda x: x.start_time)
        debug_log.log(
            "Timeline.add_new_rhythm()",
            debug_message
        )

    # Replace rhythm with new rhythm
    def replace_rhythm_with_rhythm(
        self, target_index, item:Union[Rhythm, Rest]
    ):
        """Replace rhythm in Timeline"""
        try:
            target_rhythm = self.rhythm_index[target_index]
        except IndexError as error:
            debug_log.log(
                "Timeline.remove_rhythm()",
                "Rhythm does not exist in rhythm_index"
            )
            raise Exception("Rhythm does not exist in rhythm_index") from error
        else:
            if item.duration != target_rhythm.duration:
                debug_log.log(
                    "Timeline.replace_rhythm_with_rhythm()",
                    "Error: rhythm durations not equal (%s != %s)" % (
                        item.duration,
                        target_rhythm.duration
                    )
                )
                return False
            item.start_time = target_rhythm.start_time
            self.rhythm_index[target_index] = item
            debug_log.log(
                    "Timeline.replace_rhythm_with_rhythm()",
                    "Index (%s) updated" % target_index
                )
            return True

    # Remove rhythm from rhythm_index
    def remove_rhythm(self, index):
        """Remove rhythm from Timeline"""
        try:
            self.rhythm_index.pop(index)
            debug_log.log(
                "Timeline.remove_rhythm()",
                "Rhythm deleted"
            )
        except IndexError as error:
            debug_log.log(
                "Timeline.remove_rhythm()",
                "Rhythm does not exist in rhythm_index"
            )
            raise Exception("Rhythm does not exist in rhythm_index") from error
        else:
            self.update_rhythm_start_times(start=index)
        return True

    # Move rhythm to new location (and update necessary rhythms)
    def move_rhythm(self, initial_index, end_index):
        """ Move rhythm from initial_index to end_index
            update start_times accordingly """
        # Check indexes are not out of range
        for index in [initial_index, end_index]:
            if index > len(self.rhythm_index) or index < 0:
                error = "index (%i) out of range (0 - %i)" % (
                    index,
                    len(self.rhythm_index)
                )
                debug_log.log(
                    "Timeline.move_rhythm()",
                    error
                )
                raise IndexError(error)
        if (
            initial_index == end_index
        ):
            debug_log.log(
                "Timeline.move_rhythm()",
                "indexes have no effect - skipped"
            )
        elif initial_index > end_index:
            self.rhythm_index.insert(end_index, self.rhythm_index.pop(initial_index))
        elif initial_index < end_index:
            self.rhythm_index.insert(end_index, self.rhythm_index.pop(initial_index))
        self.update_rhythm_start_times()
        debug_log.log(
            "Timeline.move_rhythm()",
            "rhythm moved from %s to %s" % (
                initial_index,
                end_index
            )
        )
        return True

    # Return complete note_data ready for engrave tool
    def compile_note_data(self):
        """Compile notes into single list for engrave tool"""
        debug_log.log(
            "Timeline.compile_note_data()",
            "compiling..."
        )
        note_data = []
        for item in self.rhythm_index:
            for note in item.normalise_notes():
                note_data.append(note)
        return note_data



if __name__ == "__main__":
    chdir(path.join(
        path.expanduser("~"),
        "Documents",
        "BSMS"
        ))
    project_timeline = Timeline("Test", 4)

    print("\nExecuting stage 1")
    print(project_timeline.rhythm_index)
    print(project_timeline.compile_note_data())
    for test_item in project_timeline.rhythm_index:
        print(test_item.duration)

    print("\nExecuting stage 2")
    project_timeline.add_rhythm(
        Rhythm("Stream_1", "[0.5, 0.5, 0.5, 0.5]"),
    )
    project_timeline.add_rhythm(
        Rest(duration=2)
    )
    project_timeline.save()
    print(project_timeline.rhythm_index)
    print(project_timeline.compile_note_data())