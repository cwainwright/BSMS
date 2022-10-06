import sys
from pathlib import Path

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QInputDialog

from project import Project
from robject import RObject_Type
from robject_manager import RObjectManager

from preferences import PREFERENCES
from section import Section


class MainWindow(QMainWindow):
    def __init__(self, quickstart, project: Project):
        super(MainWindow, self).__init__()
        self.quickstart = quickstart
        self.project = project
        self.robject_manager = RObjectManager()
        filepath = Path(__file__).parent / "ui" / "main_window.ui"
        uic.loadUi(filepath, self)
        self.setWindowTitle(self.name)

        self.characteristic_combobox.setCurrentIndex(
            self.project.current_timeline.characteristic.value
        )
        self.difficulty_combobox.setCurrentIndex(
            self.project.current_timeline.difficulty.value
        )

        # Set and populate trees
        self.robject_manager.set_tree_widget(self.robject_tree)
        self.robject_manager.set_mirror_checkbox(self.mirror_checkbox)
        self.robject_manager.populate_tree()

        self.project.set_tree_widget(self.timeline_tree)
        self.project.current_timeline.populate_tree()

        self.setup_connections()

    def show_quickstart(self):
        self.quickstart.populate_recents()
        self.quickstart.show()

    def setup_connections(self):
        # Actions
        self.actionNew.triggered.connect(self.show_quickstart)
        self.actionOpen.triggered.connect(lambda: self.quickstart.open_project())
        self.actionSave.triggered.connect(self.project.current_timeline.save)
        self.actionClose.triggered.connect(self.close)

        # RObjects
        self.robject_filter_combobox.currentIndexChanged.connect(
            lambda index: self.robject_manager.populate_tree(RObject_Type(index))
        )

        # Timeline
        self.characteristic_combobox.currentIndexChanged.connect(
            lambda: self.set_timeline()
        )
        self.difficulty_combobox.currentIndexChanged.connect(
            lambda: self.set_timeline()
        )
        self.add_robject_button.clicked.connect(
            lambda: self.project.current_timeline.add_robject(
                self.robject_manager.selected_robject
            )
        )
        self.add_section_button.clicked.connect(self.new_section)
        self.remove_object_button.clicked.connect(self.remove_object)
        self.timeline_tree.currentItemChanged.connect(self.project.current_timeline.item_selected)
        self.timeline_tree.itemExpanded.connect(self.project.current_timeline.section_expanded)
        self.timeline_tree.itemCollapsed.connect(self.project.current_timeline.section_collapsed)

    @property
    def name(self):
        return self.project.name

    def set_timeline(self):
        self.project.set_timeline(
            self.characteristic_combobox.currentIndex(),
            self.difficulty_combobox.currentIndex(),
        ).set_tree_widget(self.timeline_tree)
        
    def new_section(self):
        input_dialog = QInputDialog()
        input_dialog.setOkButtonText("Add")
        name, ok = input_dialog.getText(
            self, "New Section", "Section Name:"
        )
        if not ok:
            return -1
        input_dialog.destroy()
        
        self.project.current_timeline.add_section(Section(name))
        return 0
    
    def remove_object(self):
        __index = self.project.current_timeline.current_index
        if __index[0] == -1:
            return -1
        elif __index[1] == -1:
            self.project.current_timeline.remove_section()
        else:
            self.project.current_timeline.remove_robject()
        return 0

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow(None, Project("Apocalypse Please"))
    main_window.show()
    sys.exit(app.exec())
