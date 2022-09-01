from pathlib import Path
from shutil import rmtree

from PyQt6 import uic
from PyQt6.QtCore import QSize, QThreadPool
from PyQt6.QtWidgets import (
    QFileDialog,
    QInputDialog,
    QMessageBox,
    QProgressDialog,
    QWidget,
)

from analysis import AnalysisWorker
from main_window import MainWindow
from preferences import PREFERENCES
from project import Project


class QuickstartWindow(QWidget):
    def __init__(self):
        super(QuickstartWindow, self).__init__()
        self.threadpool = QThreadPool()
        filepath = Path(__file__).parent / "ui" / "quickstart.ui"
        uic.loadUi(filepath, self)
        self.setFixedSize(self.size())
        self.setup_connections()
        self.populate_recents()
        self.main_windows: list(MainWindow) = []

    def new_project(self) -> bool:

        input_dialog = QInputDialog(self)
        project_name, ok = input_dialog.getText(self, "New Project", "Project Name:")
        if not ok:
            return False
        input_dialog.destroy()

        if (PREFERENCES.project_directory / project_name).exists():
            confirm_dialog = QMessageBox()
            confirm_dialog.setText("Existing Project")
            confirm_dialog.setInformativeText(
                "Would you like to overwrite this project?"
            )
            confirm_dialog.setStandardButtons(
                QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel
            )
            confirm_dialog.setFixedSize(QSize(300, 100))
            ok = confirm_dialog.exec() != 4194304
            if ok:
                rmtree(PREFERENCES.project_directory / project_name)
            else:
                return self.new_project()

        file_selection_dialog = QFileDialog(self)
        filepath, ok = file_selection_dialog.getOpenFileName(
            self, caption="Select Audiofile", filter="*.wav; *.ogg"
        )
        if not ok:
            return False
        file_selection_dialog.destroy()

        progress_bar = QProgressDialog(self)
        progress_bar.setMinimum(0)
        progress_bar.setMaximum(100)
        progress_bar.setFixedSize(progress_bar.size())
        progress_bar.setCancelButton(None)
        progress_bar.open()

        analysis_worker = AnalysisWorker(project_name, filepath)
        analysis_worker.signals.progress.connect(progress_bar.setValue)
        analysis_worker.signals.current_task.connect(progress_bar.setLabelText)
        analysis_worker.signals.finished.connect(self.open_project)
        analysis_worker.signals.finished.connect(progress_bar.destroy)

        self.threadpool.start(analysis_worker)

        return True

    def open_project(self, project: Project = None):
        if project is None:
            file_selection_dialog = QFileDialog(self)
            filepath = file_selection_dialog.getExistingDirectory(
                self, "Select project to open", str(PREFERENCES.project_directory)
            )
            
            if Path(filepath).parent != PREFERENCES.project_directory:
                confirm_dialog = QMessageBox()
                confirm_dialog.setText("Project Directory")
                confirm_dialog.setInformativeText(
                    "Selected project is not located within Projects directory. "
                    + "\nPlease move Project inside the Projects directory and try again."
                )
                confirm_dialog.setDetailedText(
                    f"Project Path: {filepath}"
                    +f"\nProject Directory: {PREFERENCES.project_directory}"
                )
                confirm_dialog.setStandardButtons(
                    QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel
                )
                confirm_dialog.size
                confirm_dialog.setFixedSize(confirm_dialog.size())
                ok = confirm_dialog.exec() != 4194304
                print(ok)
                if ok:
                    return self.open_project()
                else:
                    return

            if filepath == "":
                return False
            project = Project(Path(filepath).name)

        if project.name in [window.project.name for window in self.main_windows]:
            index = [window.project.name for window in self.main_windows].index(
                project.name
            )
            del project
            self.main_windows[index].show()
        else:
            self.main_windows.append(MainWindow(self, project))
            self.main_windows[-1].show()
        self.hide()

    def populate_recents(self):
        self.recents_list_widget.clear()
        for project in PREFERENCES.project_directory.iterdir():
            if project.is_dir():
                self.recents_list_widget.addItem(project.name)

    def setup_connections(self):
        self.new_project_button.clicked.connect(self.new_project)
        self.open_project_button.clicked.connect(lambda: self.open_project())
        self.recents_list_widget.itemDoubleClicked.connect(
            lambda x: self.open_project(Project(x.text()))
        )
