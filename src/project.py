from json import load, dump
from zipfile import ZipFile
from os import path

from src.timeline import Timeline
from src.directory_operations import bsms_directory, logger

class Project:
    def __init__(self, filepath: str):
        with ZipFile(filepath, "r") as zip_file:
            zip_file.extractall(bsms_directory("CurrentProject"))
        self.filepath = bsms_directory("CurrentProject")
        self.info = self.load_info()
        self.timeline = Timeline(self)
            
    def load_info(self) -> dict:
        try:
            logger.info("Loading project info...")
            with open(path.join(self.filepath, "info.json"), "r") as info_file:
                info = dict(load(info_file))
        except FileNotFoundError:
            logger.warning("No info.json found in project")
            self.save_info()
            info = {}
        
        data = {
            "version": info.get("version", "2.0.0"),
            "song_sub_name": info.get("song_sub_name", "songSubName"),
            "song_author_name": info.get("song_author_name", "songAuthorName"),
            "level_author_name": info.get("level_author_name", "levelAuthorName"),
            "beats_per_minute": info.get("tempo", 120.0),
            "song_time_offset": info.get("song_time_offset", 0.0),
            "shuffle": info.get("shuffle", 0.0),
            "shuffle_offset": info.get("shuffle_offset", 0.5),
            "preview_start_time": info.get("preview_start_time", 10.0),
            "preview_duration": info.get("preview_duration", 10.0),
            "song_filename": info.get("song_filename", "song.wav"),
            "cover_image_filename": info.get("cover_image_filename", "cover.jpg"),
            "environment_name": info.get("environment_name", "DefaultEnvironment"),
            "all_directions_environment": info.get(
                "all_directions_environment",
                "GlassDesertEnvironment"
            )
        }
        return data

    def save_info(self):
        logger.info("Saving project info...")
        with open(path.join(self.filepath, "info.json"), "w") as info_file:
            dump(self.info, info_file)