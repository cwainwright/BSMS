"""Engrave toolset"""
from json import dump
from os import listdir, mkdir, path

def beatmap(
    project_name,
    version="2.0.0",
    map_type: str = "",
    map_difficulty: str = "Expert",
    beat_map_notes: list = None,
    beat_map_obstacles: list = None,
    beat_map_events: list = None
):
    """Engrave beatmap.dat file"""
    if beat_map_notes is None:
        beat_map_notes = []
    if beat_map_obstacles is None:
        beat_map_obstacles = []
    if beat_map_events is None:
        beat_map_events = []
    # Checks
    # If engraved beatmap directory is not found, create one
    if not path.exists(
        bsms_directory("Finalised", project_name)
    ):
        print("engravedBeatMaps directory missing")
        mkdir(bsms_directory("Finalised", project_name))
        print("new engravedBeatMaps directory created")
    # If beat_map already exists ask user whether they want to overwrite
    if map_type+map_difficulty+".dat" in listdir(
        bsms_directory("Finalised", project_name)
    ):
        print("duplicate beatmap detected")
        overwrite_confirmation_window = DialogWindow(
            "A beatmap of the same difficulty (%s) \n" % map_difficulty
            + "and type (%s) " % map_type
            + "was discovered; overwrite? "
        )
        if not overwrite_confirmation_window.run():
            return

    # Notes
    # Initialise note list to append to
    notes = []
    note_errors = []
    print("checking note values are valid...")
    for note in beat_map_notes:
        # Checks for false in RangeChecks
        note_range_check = [
            note["_lineIndex"] >= 0 and note["_lineIndex"] <= 3,
            note["_lineLayer"] >= 0 and note["_lineLayer"] <= 2,
            note["_type"] >= 0 and note["_type"] <= 3 and note["_type"] != 2,
            note["_cutDirection"] >= 0 and note["_cutDirection"] <= 8
        ]
        if all(note_range_check):
            notes.append(note)
        else:
            note_errors.append({note: note_range_check})
    print(f"{len(note_errors)}  errors encountered")
    if len(note_errors) > 0:
        print(f"note errors encountered: {note_errors}")

    # Obstacles
    # Initialise obstacle list to append to
    obstacles = []
    obstacle_errors = []
    print("checking obstacle values are valid...")
    for obstacle in beat_map_obstacles:
        # Checks for false in RangeChecks
        obstacle_range_check = [
            obstacle["_lineIndex"] >= 0 and obstacle["_lineIndex"] <= 3,
            obstacle["_type"] >= 0 and obstacle["_type"] <= 1,
            obstacle["_duration"] >= 0 and obstacle["_duration"] >= 3,
            obstacle["_width"] >= 0 and obstacle["_width"] <= 4
        ]
        if all(obstacle_range_check):
            obstacles.append(obstacle)
        else:
            obstacle_errors.append({obstacle: obstacle_range_check})
    print(f"{len(obstacle_errors)} errors encountered")
    if len(obstacle_errors) > 0:
        print(f"obstacle errors encountered: {obstacle_errors}")

    # Events
    # Initialise event list to append to
    events = []
    event_errors = []
    print("checking event values are valid...")
    # Checks event will be valid before formatting
    for event in beat_map_events:
        event_range_check = [
            event["_type"] in [0, 1, 2, 3, 4]
            and event["_value"] in [0, 1, 2, 3, 5, 6, 7],
            event["_type"] == 5
            and event["_value"] == 0 or event["_value"] == 1,
            event["_type"] == 14 or event["_type"] == 15
            and event["_value"] >= 0 and event["_value"] <= 7,
            event["_type"] in [8, 9, 10, 12, 13]
        ]
        if any(event_range_check):
            events.append(event)
        else:
            event_errors.append({event: event_range_check})
    print(f"{len(event_errors)} errors encountered")
    if len(event_errors) > 0:
        print(f"event errors encountered: {event_errors}")

    # Engrave
    print(f"dumping beatmap data to {map_type + map_difficulty}.dat...")
    with open(
        bsms_directory(
            "Finalised", project_name, map_type+map_difficulty+".dat"
        ), "w") as beat_map_file:
        dump({
            "_version": version,
            "_notes": notes,
            "_obstacles": obstacles,
            "_events": events
        }, beat_map_file, indent=4)
    print("dumped beatmap data to .dat...")

def info(project_name, lib_cache):
    """Engrave info.dat file"""
    # Checks
    # If engraved beatmap directory is not found, create one
    if not path.exists(
        bsms_directory("Finalised", project_name)
    ):
        print("engravedBeatMaps directory missing")
        mkdir(bsms_directory("Finalised", project_name))
        print("new engravedBeatMaps directory created")
    # If Info already exists ask user whether they want to overwrite
    if "Info.dat" in listdir(
        bsms_directory("Finalised", project_name)
    ):
        print("Info.dat detected")
        overwrite_confirmation_window = DialogWindow(
            "An Info.dat file was discovered; overwrite?"
        )
        if not overwrite_confirmation_window.run():
            return

    # Defaults
    lib_cache_data = lib_cache.load_cache()
    version = lib_cache_data.get("version", "2.0.0")
    song_sub_name=lib_cache_data.get("song_sub_name", "songSubName")
    song_author_name=lib_cache_data.get("song_author_name", "songAuthorName")
    level_author_name=lib_cache_data.get("level_author_name", "levelAuthorName")
    beats_per_minute=lib_cache_data.get("tempo", 120.0)
    song_time_offset=lib_cache_data.get("song_time_offset", 0.0)
    shuffle=lib_cache_data.get("shuffle", 0.0)
    shuffle_offset=lib_cache_data.get("shuffle_offset", 0.5)
    preview_start_time=lib_cache_data.get("preview_start_time", 10.0)
    preview_duration=lib_cache_data.get("preview_duration", 10.0)
    song_filename=lib_cache_data.get("song_filename", "song.wav")
    cover_image_filename=lib_cache_data.get("cover_image_filename", "cover.jpg")
    environment_name=lib_cache_data.get("environment_name", "DefaultEnvironment")
    all_directions_environment=lib_cache_data.get(
        "all_directions_environment",
        "GlassDesertEnvironment"
    )

    # BeatMapSet
    standard = []
    print("info()", "")
    for beat_map in listdir(
        bsms_directory("Finalised", project_name)
    ):
        if beat_map != "Info.dat":
            if beat_map in [
                "Easy.dat",
                "Normal.dat",
                "Hard.dat",
                "Expert.dat",
                "ExpertPlus.dat"
            ]:
                difficulty = beat_map.split(".")[0]
                difficulty_rank = {
                    "Easy": 1,
                    "Normal": 3,
                    "Hard": 5,
                    "Expert": 7,
                    "ExpertPlus": 9
                }[difficulty]
            else:
                print(
                    msg=f"Difficulty of beatmap {beat_map}"
                    + "could not be identified")
                custom_difficulty_confirmation = DialogWindow(
                    f"Difficulty of beatmap {beat_map} "
                    + "\ncould not be identified."
                    + "\nWould you like to enter custom"
                    + "\ndifficulty and difficulty rank?"
                )
                if custom_difficulty_confirmation.run():
                    custom_difficulty_input = InputWindow(
                        "Input custom difficulty:"
                    )
                    custom_difficulty_rank_input = InputWindow(
                        "Input custom difficulty rank:"
                    )
                    if custom_difficulty_input.run():
                        difficulty = custom_difficulty_input.user_interface.fieldInput.text()
                    else:
                        return
                    if custom_difficulty_rank_input.run():
                        difficulty_rank = custom_difficulty_rank_input.user_interface.fieldInput.text()
                    else:
                        return
                else:
                    return
            standard.append({
                "_difficulty": difficulty,
                "_difficultyRank": difficulty_rank,
                "_beatmapFilename": beat_map,
                "_noteJumpMovementSpeed": 0.0,
                "_noteJumpStartBeatOffset": 0.0
            })
    # Engrave
    with open(
        bsms_directory("Finalised", project_name, "Info.dat"), "w"
    ) as info_file:
        dump(
            {
                "_version": version,
                "_songName": project_name,
                "_songSubName": song_sub_name,
                "_songAuthorName": song_author_name,
                "_levelAuthorName": level_author_name,
                "_beatsPerMinute": beats_per_minute,
                "_songTimeOffset": song_time_offset,
                "_shuffle": shuffle,
                "_shufflePeriod": shuffle_offset,
                "_previewStartTime": preview_start_time,
                "_previewDuration": preview_duration,
                "_songFilename": song_filename,
                "_coverImageFilename": cover_image_filename,
                "_environmentName": environment_name,
                "_allDirectionsEnvironmentName": all_directions_environment,
                "_difficultyBeatmapSets": [{
                    "_beatmapCharacteristicName": "Standard",
                    "_difficultyBeatmaps": standard
                }]
            },
            info_file,
            indent=4
        )
