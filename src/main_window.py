import sys
from pathlib import Path

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem

from project import Project
from robject import RObject_Type, load_robject

from preferences import PREFERENCES


class MainWindow(QMainWindow):
    def __init__(self, quickstart, project: Project):
        super(MainWindow, self).__init__()
        self.quickstart = quickstart
        self.project = project
        filepath = Path(__file__).parent / "ui" / "main_window.ui"
        uic.loadUi(filepath, self)
        self.setWindowTitle(self.name)

        self.characteristic_combobox.setCurrentIndex(
            self.project.current_timeline.characteristic.value
        )
        self.difficulty_combobox.setCurrentIndex(
            self.project.current_timeline.difficulty.value
        )

        self.robject_manager = RObjectManager()
        self.robject_manager.populate_tree(self.robject_tree)
        self.project.current_timeline.populate_tree(self.timeline_tree)

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
            lambda index: self.robject_manager.populate_tree(
                self.robject_tree, RObject_Type(index)
            )
        )

        # Timeline
        self.characteristic_combobox.currentIndexChanged.connect(
            lambda: self.set_timeline()
        )
        self.difficulty_combobox.currentIndexChanged.connect(
            lambda: self.set_timeline()
        )

    @property
    def name(self):
        return self.project.name

    def set_timeline(self):
        self.project.set_timeline(
            self.characteristic_combobox.currentIndex(),
            self.difficulty_combobox.currentIndex(),
        )
        self.project.current_timeline.populate_tree(self.timeline_tree)


class RObjectManager:
    def populate_tree(
        self, tree_widget: QTreeWidget, show: RObject_Type = RObject_Type.ANY
    ):
        tree_widget.clear()
        for category in PREFERENCES.robject_directory.iterdir():
            if category.is_dir():
                category_robjects = list(category.iterdir())
                duration = load_robject(
                    category_robjects[0].stem, category.name
                ).duration
                if category.name != "[]" and show in [
                    RObject_Type.ANY,
                    RObject_Type.RHYTHM,
                ]:
                    tree_category = QTreeWidgetItem([category.name, str(duration)])
                elif category.name == "[]" and show in [
                    RObject_Type.ANY,
                    RObject_Type.REST,
                ]:
                    tree_category = QTreeWidgetItem(["Rests", str(duration)])
                else:
                    continue
                for robject in category_robjects:
                    if robject.suffix == ".json":
                        tree_category.addChild(
                            QTreeWidgetItem([robject.stem, str(duration)])
                        )
                tree_widget.addTopLevelItem(tree_category)
        tree_widget.resizeColumnToContents(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow(Project("test"))
    main_window.show()
    sys.exit(app.exec())
