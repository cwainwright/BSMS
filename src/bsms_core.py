"""Core functionality of BSMS:
 - import_song()
 - LibCache
 - finalise()
 - apply_beat_offset()"""

from json import dump, load
from math import ceil
from pathlib import Path
from shutil import copyfile

from librosa import beat, frames_to_time, get_duration, get_samplerate
from librosa import load as libload
from numpy import append, shape, zeros
from soundfile import read, write

from preferences import PREFERENCES

def import_song(project: str = None, file_path: str = None):

    original_song_file, sample_rate = read(file_path)
    librosa_y, librosa_sr = libload(file_path)

    channel_count = shape(original_song_file)[1]
    tempo, beat_frames = beat.beat_track(y=librosa_y, sr=librosa_sr)
    beat_times = frames_to_time(beat_frames, sr=librosa_sr)
    # Finds closest beat after beatTime[0] to sync beatTime[0] to
    time_per_beat = (60/tempo)

    # Synchronisation beats (to sync song to tempo pulse)
    print("synchronising songfile...")
    sync_beats = 1
    while time_per_beat*sync_beats < beat_times[0]:
        sync_beats += 1
    # Calculates additionalTime/Frames needed to sync song to beat
    sync_time = -(beat_times[0] - time_per_beat*sync_beats)
    sync_frame_count = ceil(sync_time*sample_rate)
    print("synchronisation complete")

    # Offset beats (to prevent hotstart)
    # Attempts to maintain the syncronisation to a 4/4 time signature
    print("offsetting songfile...")
    additional_beats = 4-(sync_beats % 4)
    # While hotstart may occour
    # (firstBeatTime + additional sync_time is still less than 2 seconds)
    while beat_times[0]+(time_per_beat*(sync_beats+additional_beats)) < 2:
        # Add 4 beat - beatOffsets
        additional_beats += 4
    additional_frame_count = ceil(
        additional_beats*time_per_beat*sample_rate
    )
    print("offset complete")

    # Generates additional zero-value frames to add to beginning of song file
    print("generating additional frames...")
    frames_offset = zeros(
        [
            additional_frame_count+sync_frame_count,
            channel_count
        ]
    )
    new_song_file = append(frames_offset, original_song_file, axis=0)
    print("additional frames generated")

    # Make project directory if it doesn't already exist
    print("checking for project directory...")
    if project_name not in (PREFERENCES.home_directory/"Projects").iterdir():
        (PREFERENCES.home_directory/"Projects"/project_name).mkdir()
        print("new project directory created")

    # Writes final song file with beat_offset to new "song.wav"
    print("writing updated songfile...")
    write(
        PREFERENCES.home_directory/"Projects"/project_name/"song.wav",
        new_song_file,
        sample_rate
    )
    print("songfile written")
    return additional_beats+sync_beats


def finalise(project_name, image_file_directory):
    """Copies project contents into copy_destination directory"""
    # Input sanitise copy_destination
    project_directory = PREFERENCES.home_directory/"Projects"/project_name
    copy_destination = PREFERENCES.export_directory/project_name
    # If project_name directory is not found, create one
    print("checking for project in copy destination...")
    if not copy_destination.exists():
        Path(copy_destination).mkdir()
        print(
            "project folder created in copy destination"
        )
    # Copy files to directory
    print("copying project files to copy destination...")
    copyfile(
        Path(project_directory, "song.wav"),
        Path(copy_destination, "song.wav")
    )
    for file in Path(
        project_directory,
        "engravedBeatMaps"
    ).iterdir():
        copyfile(
            Path(project_directory, "engravedBeatMaps", file),
            Path(copy_destination, file))
    copyfile(
        image_file_directory,
        Path(copy_destination, "cover.jpg"))
    print("finalise()", "project files copied")
