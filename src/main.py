import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget

from project import Project
from timeline import Timeline
from ui.alert import Ui_Alert
from ui.main_ui import Ui_MainWindow
from ui.quickstart import Ui_QuickstartMenu

class MainWindow(QMainWindow, Ui_MainWindow, Project):
    def __init__(self, project=None, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setup_connections()

        # Lists of rhythms and rests

        
        # Timeline
        self.timeline = Timeline(self)

        # Info
        self.info = Project(self)
        

if __name__ == '__main__':
    # Get filepath argument if given
    try:
        filepath = sys.argv[1]
    except IndexError:
        filepath = None
    print(filepath)
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
