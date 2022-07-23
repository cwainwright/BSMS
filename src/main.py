import sys
from tokenize import String

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget

from project import Project
from ui.alert import Ui_Alert
from ui.main_ui import Ui_MainWindow
from ui.quickstart import Ui_QuickstartMenu

class QuickstartWindow(QWidget, Ui_QuickstartMenu):
    def __init__(self):
        super().__init__()
        print("placeholder")

    def get_file_path(self) -> String:
        return '/'
    
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setup_connections()

        # Info
        self.project = Project(self)

        # Create and display quick start menu
        file_path = self.launch_quickstart()

    @property
    def timeline(self):
        return self.project.timeline

    def launch_quickstart(self) -> String:
         # Creating and displaying quickstart
        quickstart_window = QuickstartWindow()
        quickstart_window.show()

    def setup_connections(self):
        pass
        

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
