"""start menu and metadata windows"""
import sys
from os import listdir, path

from PyQt5 import QtCore, QtWidgets

from bootstrap import bsms_directory
from dialog_window_logic import AlertWindow
from ui.metadata_input_dialog import Ui_MetadataDialog
from ui.quickstart import Ui_QuickstartMenu


# Window Classes
class TemplateWindow:
    """Template window"""

    def __init__(self, title, Ui_Build):
        self.window = QtWidgets.QDialog()
        self.window.setWindowTitle(title)
        self.user_interface = Ui_Build()
        self.user_interface.setupUi(self.window)

    def run(self):
        """run window"""
        return self.window.exec_()


class QuickstartWindow(TemplateWindow):
    """Quickstart window"""

    def __init__(self):
        super().__init__("Quickstart", Ui_QuickstartMenu)


class MetadataWindow(TemplateWindow):
    """Metadata window"""

    def __init__(self):
        super().__init__("Metadata", Ui_MetadataDialog)

# Logic Classes


class QuickstartLogic:
    """Logic for Quickstart"""

    def __init__(self, app=None):
        if app is None:
            app = QtWidgets.QApplication(sys.argv)
        self.quickstart_window = QuickstartWindow()
        self.i_list = []
        self.e_list = self.quickstart_window.user_interface.recentsListWidget
        self.selected_index = None
        self.selected_item = None
        self.selected_project = None
        self.quit_result = False
        self.project_directory = bsms_directory("Projects")
        self.refresh_selected()
        quickstart_ui = self.quickstart_window.user_interface
        # Connections
        quickstart_ui.newProjectButton.clicked.connect(self.new_selected)
        quickstart_ui.openProjectButton.clicked.connect(self.open_selected)
        quickstart_ui.rhythmEditorButton.clicked.connect(
            self.rhythm_editor_selected)
        quickstart_ui.recentsListWidget.itemClicked.connect(self.item_selected)
        quickstart_ui.recentsListWidget.itemDoubleClicked.connect(
            self.item_double_clicked)

        # Run app
        self.quickstart_window.window.exec_()

    def populate_internal(self):
        """populate internal list"""
        self.i_list.clear()
        for file in listdir(self.project_directory):
            file_path = path.join(self.project_directory, file)
            if path.isdir(file_path):
                self.i_list.append(file_path)
        sorted(self.i_list, key=path.getmtime)

    def populate_external(self):
        """populate external list"""
        self.e_list.clear()
        self.e_list.addItems(self.i_list)

    def refresh_selected(self):
        """populate internal and external list"""
        self.populate_internal()
        self.populate_external()
        self.selected_index = None
        self.selected_item = None

    def item_selected(self, item):
        """item selected"""
        self.selected_index = self.e_list.currentRow()
        self.selected_item = item.text()

    def item_double_clicked(self, item):
        """item doubleclicked"""
        self.item_selected(item)
        self.open_selected(self.selected_item)

    def new_selected(self):
        """new selected"""
        self.quit_result = True
        self.quickstart_window.window.close()

    def open_selected(self, project_directory=None):
        """open selected"""
        if project_directory in [None, False]:
            lib_cache_directory = QtWidgets.QFileDialog.getOpenFileName(
                filter="lib_cache Files (lib_cache.json)"
            )[0]
            if lib_cache_directory == "":
                return
            project_directory = path.split(lib_cache_directory)[0]
        self.selected_project = project_directory
        self.quit_result = True
        self.quickstart_window.window.close()

    def rhythm_editor_selected(self):
        """rhythm editor incomplete alert"""
        feature_not_ready_alert = AlertWindow(
            "rhythm editor:"
            + "\nfeature incomplete",
            "feature incomplete"
        )
        feature_not_ready_alert.run()


class MetadataLogic:
    """Logic for Metadata input"""

    def __init__(self, lib_cache, app=None):
        if app is None:
            app = QtWidgets.QApplication(sys.argv)
        self.lib_cache = lib_cache
        self.song_data = self.lib_cache.load_cache()
        print(self.song_data)
        self.metadata_window = MetadataWindow()
        metadata_ui = self.metadata_window.user_interface

        self.iterate_text_info = {
            "project_name": metadata_ui.projectNameInput,
            "version": metadata_ui.versionInput,
            "song_sub_name": metadata_ui.songSubNameInput,
            "song_author_name": metadata_ui.songAuthorNameInput,
            "level_author_name": metadata_ui.levelAuthorNameInput,
            "song_filename": metadata_ui.songFilenameInput,
            "cover_filename": metadata_ui.coverImageFilenameInput
        }
        self.iterate_value_info = {
            "tempo": metadata_ui.BPMSpinbox,
            "song_time_offset": metadata_ui.songTimeOffsetSpinbox,
            "shuffle": metadata_ui.shuffleSpinbox,
            "shuffle_offset": metadata_ui.shuffleOffsetSpinbox,
            "preview_start_time": metadata_ui.previewStartTimeSpinbox,
            "preview_duration": metadata_ui.previewDurationSpinbox
        }
        self.iterate_combobox_info = {
            "environment_name": metadata_ui.environmentNameSelector,
            "all_directions_environment_name": metadata_ui.allDirectionsEnvironmentNameSelector
        }
        self.fill_in_entries()

    def fill_in_entries(self):
        """populate entries with info from lib_cache"""
        for value_name, value in self.iterate_text_info.items():
            if value_name in self.song_data:
                value.setText(self.song_data[value_name])
        for value_name, value in self.iterate_value_info.items():
            if value_name in self.song_data:
                value.setValue(self.song_data[value_name])
        for value_name, value in self.iterate_combobox_info.items():
            if value_name in self.song_data:
                index = value.findText(
                    self.song_data[value_name], QtCore.Qt.MatchFixedString)
                if index != -1:
                    value.setCurrentIndex(index)

    def update_from_entries(self):
        """update lib_cache from entries"""
        for value_name, value in self.iterate_text_info.items():
            self.song_data.update({value_name: value.text()})
        for value_name, value in self.iterate_value_info.items():
            self.song_data.update({value_name: value.value()})
        for value_name, value in self.iterate_combobox_info.items():
            self.song_data.update({value_name: value.currentText()})
        self.lib_cache.update_cache(self.song_data)

    def run(self):
        """run window"""
        if self.metadata_window.window.exec_():
            self.update_from_entries()
            return True
        return False


if __name__ == "__main__":
    quickstart_window_logic = QuickstartLogic()
