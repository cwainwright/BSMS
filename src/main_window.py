import sys
from pathlib import Path

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem

from project import Project
from robject import RObject_Type

from preferences import PREFERENCES


class MainWindow(QMainWindow):
    def __init__(self, quickstart, project: Project):
        super(MainWindow, self).__init__()
        self.quickstart = quickstart
        self.project = project
        filepath = Path(__file__).parent / "ui" / "main_window.ui"
        uic.loadUi(filepath, self)
        self.setWindowTitle(self.name)
        self.setup_connections()
        self.robject_manager = RObjectManager(self.robject_tree)
        self.robject_manager.populate_tree()

    def show_quickstart(self):
        self.quickstart.populate_recents()
        self.quickstart.show()

    def setup_connections(self):
        self.actionNew.triggered.connect(self.show_quickstart)
        self.robject_filter_combobox.currentIndexChanged.connect(lambda index: self.robject_manager.populate_tree(RObject_Type(index)))

    @property
    def name(self):
        return self.project.name

class RObjectManager:
    def __init__(self, tree_widget: QTreeWidget):
        self.tree_widget = tree_widget
    
    def populate_tree(self, show: RObject_Type = RObject_Type.ANY):
        self.tree_widget.clear()
        print(f"Filtering for {show}")
        for category in PREFERENCES.robject_directory.iterdir():
            if category.is_dir():
                if category.name != "[]" and show in [RObject_Type.ANY, RObject_Type.RHYTHM]:
                    tree_category = QTreeWidgetItem([category.name])
                elif category.name == "[]" and show in [RObject_Type.ANY, RObject_Type.REST]:
                    tree_category = QTreeWidgetItem(["Rests"])
                else:
                    continue
                for robject in category.iterdir():
                    if robject.suffix == ".json":
                        tree_category.addChild(QTreeWidgetItem([robject.name.replace(".json", "")]))
                self.tree_widget.addTopLevelItem(tree_category)
        self.tree_widget.resizeColumnToContents(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow(Project("test"))
    main_window.show()
    sys.exit(app.exec())
