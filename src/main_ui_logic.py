"""Bridge gap between program logic and gui"""
import sys
from copy import deepcopy
from json import dump, load
from os import listdir, path
import logging

from PyQt5 import QtCore, QtWidgets

import engrave
from bsms_core import finalise
from dialog_window_logic import (
    AlertWindow,
    DialogWindow,
    InputWindow,
    RestInputWindow
)
from rhythms import (
    Rest,
    Rhythm,
    get_rhythm_duration,
    rhythm_directory,
    rhythm_load,
    rhythm_save
)
from timeline import Timeline
from ui.main_ui import Ui_MainWindow

logging.basicConfig(
    format="%(asctime)s %(levelname)s: %(message)s",
    filename=path.join(
        "logs",
        f"{__name__}.log"
    ),
    filemode="a"
)

logger = logging.getLogger(__name__)

# Window Class
class MainWindow:
    """create main window"""
    def __init__(self):
        self.window = QtWidgets.QMainWindow()
        self.user_interface = Ui_MainWindow()
        self.user_interface.setupUi(self.window)

# Logic Classes
class MainWindowLogic:
    """Logic for MainWindow"""
    def __init__(self, lib_cache, app=None):
        if app is None:
            self.app = QtWidgets.QApplication(sys.argv)
        else:
            self.app = app
        self.main_window = MainWindow()
        self.lib_cache = lib_cache
        self.selected_item = None
        self.quit_reason = None

        main_ui = self.main_window.user_interface
        # Initialise logic bridge objects
        self.rhythm_tab_logic = RhythmTabLogic(main_ui)
        self.rest_tab_logic = RestTabLogic(main_ui)
        self.timeline_tab_logic = TimelineTabLogic(
            self.lib_cache,
            main_ui
        )
        self.info_tab_logic = InfoTabLogic(self.lib_cache, main_ui)

        # Connections
        # rhythm_tab_logic
        main_ui.rhythmTree.itemClicked.connect(self.rhythm_tab_logic.item_selected)
        main_ui.newRhythm.clicked.connect(self.rhythm_tab_logic.new_selected)
        main_ui.editRhythm.clicked.connect(self.rhythm_tab_logic.edit_selected)
        main_ui.importRhythm.clicked.connect(self.rhythm_tab_logic.import_selected)
        main_ui.presetsTabs.currentChanged.connect(self.rhythm_tab_logic.refresh_selected)
        main_ui.refreshRhythms.clicked.connect(self.rhythm_tab_logic.refresh_selected)

        # rest_tab_logic
        main_ui.restTree.itemClicked.connect(self.rest_tab_logic.item_selected)
        main_ui.customRest.clicked.connect(self.rest_tab_logic.custom_selected)
        main_ui.editRest.clicked.connect(self.rest_tab_logic.edit_selected)
        main_ui.deleteRest.clicked.connect(self.rest_tab_logic.delete_selected)
        main_ui.presetsTabs.currentChanged.connect(self.rest_tab_logic.refresh_selected)
        main_ui.refreshRests.clicked.connect(self.rest_tab_logic.refresh_selected)

        # timeline_tab_logic
        main_ui.add.clicked.connect(lambda: self.timeline_tab_logic.add_item(
            [self.rhythm_tab_logic.selected_rhythm, self.rest_tab_logic.selected_rest]
        ))
        main_ui.remove.clicked.connect(self.timeline_tab_logic.remove_item)
        main_ui.up.clicked.connect(self.timeline_tab_logic.up_selected)
        main_ui.down.clicked.connect(self.timeline_tab_logic.down_selected)

        # info_tab_logic
        main_ui.cancel.clicked.connect(self.info_tab_logic.cancel_selected)
        main_ui.apply.clicked.connect(self.info_tab_logic.apply_selected)

        # menu_actions
        main_ui.actionNew.triggered.connect(lambda: self.return_to_menu("new"))
        main_ui.actionOpen.triggered.connect(lambda: self.return_to_menu("open"))
        main_ui.actionCreateRhythm.triggered.connect(self.rhythm_tab_logic.new_selected)
        main_ui.actionImportRhythm.triggered.connect(self.rhythm_tab_logic.import_selected)
        main_ui.actionSave.triggered.connect(self.timeline_tab_logic.save_selected)
        main_ui.actionBeatmap.triggered.connect(self.timeline_tab_logic.engrave_beatmap)
        main_ui.actionInfo.triggered.connect(self.timeline_tab_logic.engrave_info)
        main_ui.actionFinalise.triggered.connect(self.finalise_process)

    def finalise_process(self):
        """finalise"""
        image_filepath = QtWidgets.QFileDialog.getOpenFileName(
            filter="JPEG (*.jpg)"
        )[0]
        if image_filepath == "":
            completion_confirmation_window = AlertWindow(
                "Process failed, "
                + "\n No valid cover image was provided"
                )
        else:
            finalise(
                self.lib_cache.project_name,
                image_filepath
            )
            completion_confirmation_window = AlertWindow("Process complete!")
        completion_confirmation_window.run()

    def return_to_menu(self, quit_reason):
        """return to main_menu"""
        self.quit_reason = quit_reason
        self.main_window.window.close()
        return True

    def run(self):
        """Run app"""
        self.main_window.window.show()
        self.app.exec_()
        if self.timeline_tab_logic.changes_made:
            save_dialog = DialogWindow("Changes have been made: do you want to save?")
            if save_dialog.run():
                self.timeline_tab_logic.save_selected()
        return True

class RhythmTabLogic:
    """join logic and GUI for RhythmTab"""
    def __init__(self, main_ui):
        self.i_tree = {}
        self.e_tree = main_ui.rhythmTree
        self.selected_category = None
        self.selected_rhythmid = None
        self.selected_direction = None
        self.selected_rhythm = None
        self.refresh_selected()

    def populate_internal(self):
        """populate internal tree (i_tree)"""
        self.i_tree.clear()
        for category in listdir(rhythm_directory()):
            if category != ".DS_Store":
                category_contents = []
                for rhythm_id in listdir(rhythm_directory(category)):
                    if rhythm_id != ".DS_Store":
                        category_contents.append(rhythm_id)
                self.i_tree.update({category: category_contents})

    def populate_external(self):
        """populate external tree (e_tree)"""
        self.e_tree.clear()
        for category in self.i_tree.items():
            category_item = QtWidgets.QTreeWidgetItem([
                category[0],
                str(get_rhythm_duration(category[1][0], category[0]))
            ])
            for rhythm in category[1]:
                rhythm_item = QtWidgets.QTreeWidgetItem([rhythm.strip(".json")])
                for direction in ["Left", "Right"]:
                    direction_item = QtWidgets.QTreeWidgetItem([direction])
                    rhythm_item.addChild(direction_item)
                category_item.addChild(rhythm_item)
            self.e_tree.addTopLevelItem(category_item)
        self.e_tree.resizeColumnToContents(0)
        self.e_tree.resizeColumnToContents(1)

    def refresh_selected(self):
        """refresh both internal and external trees"""
        self.populate_internal()
        self.populate_external()
        self.selected_category = None
        self.selected_rhythmid = None
        self.selected_direction = None
        self.selected_rhythm = None

    def item_selected(self, item):
        """gets item selected, if item is direction sets vars"""
        if item.childCount() == 0:
            self.selected_category = item.parent().parent().text(0)
            self.selected_rhythmid = item.parent().text(0)
            self.selected_direction = item.text(0)
            self.selected_rhythm = Rhythm(
                self.selected_rhythmid,
                self.selected_category,
                mirror={"Left":False, "Right":True}[self.selected_direction]
            )
        else:
            self.selected_category = None
            self.selected_rhythmid = None
            self.selected_direction = None
            self.selected_rhythm = None

    def new_selected(self):
        """calls feature_not_ready function with new() as parameter"""
        feature_not_ready_alert = AlertWindow(
            message="new() function is not yet ready"
        )
        feature_not_ready_alert.run()

    def edit_selected(self):
        """calls feature_not_ready function with edit() as parameter"""
        feature_not_ready_alert = AlertWindow(
            message="edit() function is not yet ready"
        )
        feature_not_ready_alert.run()

    def import_selected(self):
        """asks user for rhythm to import"""
        filepath = QtWidgets.QFileDialog.getOpenFileName(
            filter="JSON Files (*.json)"
        )[0]
        if filepath is None or filepath == "":
            logger.log(
                "RhythmTabLogic.import_selected()",
                "no file selected: import cancelled"
            )
            return False
        rhythm_load_result = rhythm_load(filepath)
        if not rhythm_load_result[0]:
            overwrite_confirmation = DialogWindow("Rhythm already detected: overwrite?")
            if not overwrite_confirmation.run():
                logger.log(
                    "RhythmTabLogic.import_selected()",
                    "cancel selected: import cancelled"
                )
                return False
        rhythm_save(**rhythm_load_result[1])
        self.refresh_selected()
        logger.log(
            "RhythmTabLogic.import_selected()",
            "import successful"
        )
        return True

class RestTabLogic:
    """join logic and GUI for RhythmTab"""
    def __init__(self, main_ui):
        self.i_tree = {}
        self.e_tree = main_ui.restTree
        self.selected_category = None
        self.selected_restid = None
        self.selected_duration = None
        self.selected_rest = None
        self.json_filepath = path.join(path.dirname(__file__), "rests.json")
        self.refresh_selected()

    def populate_internal(self):
        """populate internal tree (i_tree)"""
        self.i_tree.clear()
        with open(self.json_filepath, "r") as rests_json:
            self.i_tree = load(rests_json)

    def populate_external(self):
        """populate external tree (e_tree)"""
        self.e_tree.clear()
        for category in self.i_tree.items():
            category_item = QtWidgets.QTreeWidgetItem([
                category[0],
            ])
            for rest in category[1]:
                rest_item = QtWidgets.QTreeWidgetItem([rest["Name"], str(rest["Duration"])])
                category_item.addChild(rest_item)
            self.e_tree.addTopLevelItem(category_item)
        self.e_tree.resizeColumnToContents(0)
        self.e_tree.resizeColumnToContents(1)

    def item_selected(self, item):
        """gets item selected, if item is rest sets vars"""
        if item.childCount() == 0 and item.parent() is not None:
            self.selected_category = item.parent().text(0)
            self.selected_restid = item.text(0)
            self.selected_duration = float(item.text(1))
            self.selected_rest = Rest(
                duration=self.selected_duration,
                rhythm_category=self.selected_category
            )
        else:
            self.selected_category = None
            self.selected_restid = None
            self.selected_duration = None
            self.selected_rest = None

    def refresh_selected(self):
        """refresh both internal and external trees"""
        self.populate_internal()
        self.populate_external()
        self.selected_category = None
        self.selected_restid = None
        self.selected_duration = None
        self.selected_rest = None


    def custom_selected(self):
        """adds in new rest"""
        custom_rest_input = RestInputWindow("Input Rest Data:")
        if custom_rest_input.run():
            # Gather up-to-date json contents
            self.populate_internal()
            rest = custom_rest_input.get_information()
            if rest in self.i_tree["Custom"]:
                custom_rest_input.change_title_text(
                    "Duplicate item was found\nPlease try again:"
                )
            else:
                self.i_tree["Custom"].append(rest)
            with open(self.json_filepath, "w") as rests_json:
                dump(self.i_tree, rests_json, indent=4)
            self.refresh_selected()
        else:
            logger.log(
                "RestTabLogic.custom_selected()",
                "cancel selected: creation of custom rest cancelled"
            )

    def edit_selected(self):
        """edits rest"""
        if self.e_tree.selectedItems() == []:
            return
        if self.selected_category in [None, "Defaults"]:
            edit_alert = AlertWindow(
                "Item is a default or category: it cannot be edited"
            )
            edit_alert.run()
            return
        custom_rest_input = RestInputWindow("Edit Rest Data:")
        rest = {
            "Name":self.selected_restid,
            "Duration":self.selected_duration
        }
        custom_rest_input.set_information(rest)
        index = self.i_tree["Custom"].index(rest)
        if custom_rest_input.run():
            rest = custom_rest_input.get_information()
            self.i_tree["Custom"][index]=rest
        with open(self.json_filepath, "w") as rests_json:
            dump(self.i_tree, rests_json, indent=4)
        self.refresh_selected()

    def delete_selected(self):
        """deletes rest"""
        if self.e_tree.selectedItems() == []:
            return
        if self.selected_category in [None, "Defaults"]:
            delete_alert = AlertWindow(
                "Item is a default or category: it cannot be deleted"
            )
            delete_alert.run()
            return
        # Gather up-to-date json contents
        self.populate_internal()
        rest = {
            "Name":self.selected_restid,
            "Duration":self.selected_duration
        }
        self.i_tree["Custom"].remove(rest)
        with open(self.json_filepath, "w") as rests_json:
            dump(self.i_tree, rests_json, indent=4)
        self.refresh_selected()

class TimelineTabLogic:
    """join logic and GUI for TimelineTab"""
    def __init__(self, lib_cache, main_ui):
        self.main_ui = main_ui
        self.lib_cache = lib_cache
        self.project_name = lib_cache.project_name
        self.i_list = Timeline(self.project_name, lib_cache.beat_offset)
        self.e_list = main_ui.timelineList
        self.selected_index = None
        self.json_filepath = path.join(path.dirname(__file__), "rests.json")
        self.refresh()
        self.changes_made = False

    def refresh(self):
        """refresh contents of external"""
        self.e_list.clear()
        for item in self.i_list.rhythm_index:
            item_list = item.get_data_list()
            self.e_list.addTopLevelItem(
                QtWidgets.QTreeWidgetItem(
                    item_list
                )
            )
        for column in range(0, 4):
            self.e_list.resizeColumnToContents(column)
        self.changes_made = True

    def add_item(self, items):
        """add selected item to timeline"""
        item = deepcopy(items[self.main_ui.presetsTabs.currentIndex()])
        if isinstance(item, (Rhythm, Rest)):
            self.i_list.add_rhythm(item)
            self.refresh()

    def remove_item(self):
        """remove selected item from timeline"""
        self.selected_index = self.main_ui.timelineList.currentIndex().row()
        if self.selected_index not in [None, -1]:
            self.i_list.remove_rhythm(self.selected_index)
            self.refresh()

    def save_selected(self):
        """save timeline"""
        self.i_list.save()
        self.changes_made = False

    def up_selected(self):
        """move selected item up in timeline"""
        self.selected_index = self.main_ui.timelineList.currentIndex().row()
        if 0 < self.selected_index <= len(self.i_list):
            self.i_list.move_rhythm(
                self.selected_index,
                self.selected_index-1
            )
        self.refresh()

    def down_selected(self):
        """move selected item down in timeline"""
        self.selected_index = self.main_ui.timelineList.currentIndex().row()
        if 0 <= self.selected_index <= len(self.i_list)-1:
            self.i_list.move_rhythm(
                self.selected_index,
                self.selected_index+1
            )
        self.refresh()

    def engrave_beatmap(self):
        """engrave beatmap from rhythms and rests in timeline"""
        input_window = InputWindow("Input beatmap difficulty")
        if not input_window.run():
            return
        difficulty = input_window.user_interface.fieldInput.text()
        if difficulty == "":
            difficulty = "Expert"
        engrave.beatmap(
            project_name=self.project_name,
            version=self.lib_cache.load_cache()["version"],
            map_type="",
            map_difficulty=difficulty,
            beat_map_notes=self.i_list.compile_note_data()
        )
        completion_confirmation_window = AlertWindow("Process complete!")
        completion_confirmation_window.run()

    def engrave_info(self):
        """engrave info file from lib_cache"""
        engrave.info(
            project_name = self.project_name,
            lib_cache = self.lib_cache
        )
        completion_confirmation_window = AlertWindow("Process complete!")
        completion_confirmation_window.run()

class InfoTabLogic:
    """join logic and GUI for InfoTab"""
    def __init__(self, lib_cache, info_form):
        self.lib_cache = lib_cache
        self.iterate_text_info = {
            "project_name":info_form.projectNameInput,
            "version":info_form.versionInput,
            "song_sub_name":info_form.songSubNameInput,
            "song_author_name":info_form.songAuthorNameInput,
            "level_author_name":info_form.levelAuthorNameInput,
            "song_filename":info_form.songFilenameInput,
            "cover_filename":info_form.coverImageFilenameInput
        }
        self.iterate_value_info = {
            "tempo":info_form.BPMSpinbox,
            "song_time_offset":info_form.songTimeOffsetSpinbox,
            "shuffle":info_form.shuffleSpinbox,
            "shuffle_offset":info_form.shuffleOffsetSpinbox,
            "preview_start_time":info_form.previewStartTimeSpinbox,
            "preview_duration":info_form.previewDurationSpinbox
        }
        self.iterate_combobox_info = {
            "environment_name":info_form.environmentNameSelector,
            "all_directions_environment_name":info_form.allDirectionsEnvironmentNameSelector
        }
        self.populate()

    def populate(self):
        """update info tab contents"""
        lib_cache_data = self.lib_cache.load_cache()
        for value_name, value in self.iterate_text_info.items():
            if value_name in lib_cache_data:
                value.setText(str(lib_cache_data[value_name]))
            else:
                logger.log(
                    "InfoTabLogic.populate()",
                    "text could not be found %s" % value_name
                )
        for value_name, value in self.iterate_value_info.items():
            if value_name in lib_cache_data:
                value.setValue(lib_cache_data[value_name])
            else:
                logger.log(
                    "InfoTabLogic.populate()",
                    "text could not be found %s" % value_name
                )
        for value_name, value in self.iterate_combobox_info.items():
            if value_name in lib_cache_data:
                index = value.findText(lib_cache_data[value_name], QtCore.Qt.MatchFixedString)
                if index != -1:
                    value.setCurrentIndex(index)
            else:
                logger.log(
                    "InfoTabLogic.populate()",
                    "text could not be found %s" % value_name
                )

    def cancel_selected(self):
        """update info tab contents"""
        self.populate()

    def apply_selected(self):
        """update libcache with info tab contents"""
        for value_name, value in self.iterate_text_info.items():
            self.lib_cache.update_cache({value_name:value.text()})
        for value_name, value in self.iterate_value_info.items():
            self.lib_cache.update_cache({value_name:value.value()})
        for value_name, value in self.iterate_combobox_info.items():
            self.lib_cache.update_cache({value_name:value.currentText()})
