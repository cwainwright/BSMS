"""main program script"""
import sys
from os import path, listdir, remove, rmdir

from PyQt5 import QtWidgets

from debug import DebugLog
from bootstrap import setup
from bsms_core import import_song, LibCache
from start_ui_logic import QuickstartLogic, MetadataLogic
from main_ui_logic import MainWindowLogic, InputWindow, DialogWindow

def cleanup(project_directory):
    """clean up half-complete project directories"""
    for file in listdir(project_directory):
        remove(path.join(project_directory, file))
    rmdir(project_directory)

def main():
    """main functions"""
    setup()
    debug_log = DebugLog("main.py")
    debug_log.log(
        "main()",
        "initialising application..."
    )
    app = QtWidgets.QApplication(sys.argv)

    quickstart_window_logic = QuickstartLogic(app=app)
    project_directory = quickstart_window_logic.selected_project
    if not quickstart_window_logic.quit_result:
        sys.exit()
    elif project_directory is None:
        project_name_input = InputWindow("Input Project_Name")
        if not project_name_input.run():
            return
        project_name = project_name_input.user_interface.fieldInput.text()
        song_file_path = QtWidgets.QFileDialog.getOpenFileName(
            filter="Sound File (*.wav; *.flac; *.ogg)"
        )[0]
        if project_name == "" or song_file_path == "":
            return
        import_song_dialog_window = DialogWindow(
            "Ready to import/analyse song"
            + "\nNote: this may take a while"
        )
        if not import_song_dialog_window.run():
            return
        project_directory, beat_offset = import_song(project_name, song_file_path)
        lib_cache_dialog_window = DialogWindow("Ready to create libcache")
        if not lib_cache_dialog_window.run():
            cleanup(project_directory)
            return
        lib_cache = LibCache(project_directory, beat_offset)
        metadata_window_logic = MetadataLogic(lib_cache, app)
        if not metadata_window_logic.run():
            cleanup(project_directory)
            return
    else:
        lib_cache = LibCache(project_directory)
    main_window_logic = MainWindowLogic(lib_cache, app)
    main_window_logic.run()
    if main_window_logic.quit_reason in ["new", "open"]:
        return
    else:
        sys.exit()

while True:
    main()
