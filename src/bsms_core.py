"""Core functionality of BSMS:
 - import_song()
 - LibCache
 - finalise()
 - apply_beat_offset()"""

import logging
from json import dump, load
from math import ceil
from os import listdir, mkdir, path
from shutil import copyfile

from librosa import beat, frames_to_time, get_duration, get_samplerate
from librosa import load as libload
from numpy import append, shape, zeros
from soundfile import read, write

from directory_operations import bsms_directory

logging.basicConfig(
    format="%(asctime)s %(levelname)s: %(message)s",
    filename=path.join(
        "logs",
        f"{__name__}.log"
    ),
    filemode="a"
)

logger = logging.getLogger(__name__)

def projects_directory(project_name=None):
    """returns projects directory"""
    if project_name is None:
        return bsms_directory("Projects")
    return path.join(projects_directory(), project_name)

#   #   #   #   Import Song #   #   #   #
def import_song(project_name: str = None, file_path: str = None):
    """ Project initialisation:
        Parameters: project_name, file_path
        Returns: project_name and beat_offset"""
    # Check for parameter presence and ask if none given
    if project_name is None:
        project_name = input("\nProject Name: ")
    if file_path is None:
        file_path = input("Filepath to song file to import: ").strip("\"")

    # Load original_song_file
    logger.info(msg="loading original songfile...")
    original_song_file, sample_rate = read(file_path)
    librosa_y, librosa_sr = libload(file_path)
    logger.info(msg="songfile loaded")

    # Gathers basic data required for inital analysis
    logger.info(msg="analysing original songfile...")
    channel_count = shape(original_song_file)[1]
    tempo, beat_frames = beat.beat_track(y=librosa_y, sr=librosa_sr)
    beat_times = frames_to_time(beat_frames, sr=librosa_sr)
    # Finds closest beat after beatTime[0] to sync beatTime[0] to
    time_per_beat = (60/tempo)
    logger.info(msg="analysis complete")

    # Synchronisation beats (to sync song to tempo pulse)
    logger.info(msg="synchronising songfile...")
    sync_beats = 1
    while time_per_beat*sync_beats < beat_times[0]:
        sync_beats += 1
    # Calculates additionalTime/Frames needed to sync song to beat
    sync_time = -(beat_times[0] - time_per_beat*sync_beats)
    sync_frame_count = ceil(sync_time*sample_rate)
    logger.info(msg="synchronisation complete")

    # Offset beats (to prevent hotstart)
    # Attempts to maintain the syncronisation to a 4/4 time signature
    logger.info(msg="offsetting songfile...")
    additional_beats = 4-(sync_beats % 4)
    # While hotstart may occour
    # (firstBeatTime + additional sync_time is still less than 2 seconds)
    while beat_times[0]+(time_per_beat*(sync_beats+additional_beats)) < 2:
        # Add 4 beat - beatOffsets
        additional_beats += 4
    additional_frame_count = ceil(
        additional_beats*time_per_beat*sample_rate
    )
    logger.info(msg="offset complete")

    # Generates additional zero-value frames to add to beginning of song file
    logger.info(msg="generating additional frames...")
    frames_offset = zeros(
        [
            additional_frame_count+sync_frame_count,
            channel_count
        ]
    )
    new_song_file = append(frames_offset, original_song_file, axis=0)
    logger.info(msg="additional frames generated")

    # Make project directory if it doesn't already exist
    logger.info(msg="checking for project directory...")
    if project_name not in listdir(projects_directory()):
        mkdir(projects_directory(project_name))
        logger.info(msg="new project directory created")

    # Writes final song file with beat_offset to new "song.wav"
    logger.info(msg="writing updated songfile...")
    write(
        path.join(projects_directory(project_name), "song.wav"),
        data=new_song_file,
        samplerate=sample_rate
    )
    logger.info(msg="songfile written")
    return (projects_directory(project_name), additional_beats+sync_beats)

#   #   #   #   Libcache    #   #   #   #
class LibCache:
    """Abstraction of libCache into a class"""
    def __init__(self, project_directory, beat_offset=0):
        # Create basic song attributes
        self.project_directory = project_directory
        self.project_name = path.split(project_directory)[1]
        self.lib_cache_directory = path.join(project_directory, "lib_cache.json")
        self.songfile_directory = path.join(project_directory, "song.wav")
        self.beat_offset = beat_offset
        # Check for existence of lib_cache.json in project directory
        logger.info(
            msg="checking for lib_cache.json..."
        )
        if not path.exists(self.lib_cache_directory):
            self.new_cache(self.analyse())
        elif "analysed" not in self.load_cache():
            self.update_cache(self.analyse())
        logger.info(
            msg="LibCache initialised"
        )

    def analyse(self):
        """Analyse song"""
        logger.info(
            msg="loading songfile..."
        )
        librosa_y, librosa_sr = libload(self.songfile_directory)
        # Librosa extracts useful data from the song
        logger.info(
            msg="analysing songfile..."
        )
        sample_rate = get_samplerate(self.songfile_directory)
        tempo = beat.beat_track(y=librosa_y, sr=librosa_sr)[0]
        duration = get_duration(y=librosa_y, sr=librosa_sr)
        logger.info(
            msg="songfile analysed"
        )
        return {
            "project_name":self.project_name,
            "song_filename": "song.wav",
            "tempo": tempo,
            "sample_rate": sample_rate,
            "duration": duration,
            "beat_offset": self.beat_offset,
            "analysed":True
        }

    def load_cache(self):
        """"load cache contents"""
        with open(self.lib_cache_directory, "r") as lib_cache_file:
            logger.info(
                msg="lib_cache.json loaded"
            )
            return load(lib_cache_file)

    def update_cache(self, data):
        """update cache contents"""
        lib_cache_data = self.load_cache()
        for value_name, value in data.items():
            print(value_name, value)
            lib_cache_data.update({value_name: value})
        with open(self.lib_cache_directory, "w") as lib_cache_file:
            dump(lib_cache_data, lib_cache_file, indent=4)
        logger.info(
            msg="lib_cache.json updated"
        )

    def new_cache(self, data):
        """create new cache"""
        lib_cache_data = {}
        for value_name, value in data.items():
            lib_cache_data.update({value_name: value})
        with open(self.lib_cache_directory, "w") as lib_cache_file:
            dump(lib_cache_data, lib_cache_file, indent=4)
        logger.info(
            msg="lib_cache.json created"
        )

def finalise(project_name, image_file_directory):
    """Copies project contents into copy_destination directory"""
    # Input sanitise copy_destination
    project_directory = projects_directory(project_name)
    copy_destination = path.join(
        bsms_directory("Finalised Projects"),
        project_name
    )
    # If project_name directory is not found, create one
    logger.info(msg="checking for project in copy destination...")
    if project_name not in listdir(bsms_directory("Finalised Projects")):
        mkdir(copy_destination)
        logger.info(
            msg="project folder created in copy destination"
        )
    # Copy files to directory
    logger.info(msg="copying project files to copy destination...")
    copyfile(
        path.join(project_directory, "song.wav"),
        path.join(copy_destination, "song.wav"))
    for file in listdir(path.join(
        project_directory,
        "engravedBeatMaps"
    )):
        copyfile(
            path.join(project_directory, "engravedBeatMaps", file),
            path.join(copy_destination, file))
    copyfile(
        image_file_directory,
        path.join(copy_destination, "cover.jpg"))
    logger.info("finalise()", "project files copied")
