import logging
from os import path

from PyQt5 import QtWidgets

from ui.alert import Ui_Alert
from ui.dialog import Ui_Dialog
from ui.input_dialog import Ui_InputDialog
from ui.rest_input import Ui_RestInput
from directory_operations import logger

class TemplateDialogWindow:
    """superclass to dialog window classes below"""
    def __init__(self, message, title, Ui_Build):
        self.window = QtWidgets.QDialog()
        self.window.setWindowTitle(title)
        self.user_interface = Ui_Build()
        self.user_interface.setupUi(self.window)
        self.user_interface.messageLabel.setText(message)
        self.window.adjustSize()

    def run(self):
        """run window"""
        return self.window.exec_()

class AlertWindow(TemplateDialogWindow):
    """create disposable alert window"""
    def __init__(self, message, title="alert"):
        super().__init__(message, title, Ui_Alert)

class DialogWindow(TemplateDialogWindow):
    """create disposable dialog window"""
    def __init__(self, message, title="dialog"):
        super().__init__(message, title, Ui_Dialog)

class InputWindow(TemplateDialogWindow):
    """create disposable input window"""
    def __init__(self, message, title="input", default_answer=""):
        super().__init__(message, title, Ui_InputDialog)
        self.user_interface.fieldInput.setText(default_answer)

class RestInputWindow(TemplateDialogWindow):
    """create disposable rest input window"""
    def __init__(self, message, title="rest"):
        super().__init__(message, title, Ui_RestInput)

    def set_information(self, rest):
        """set defaults"""
        name = rest["Name"]
        duration = rest["Duration"]
        self.user_interface.nameEdit.setText(name)
        self.user_interface.durationSpinBox.setValue(duration)

    def get_information(self):
        """get user input"""
        name = self.user_interface.nameEdit.text()
        duration = float(self.user_interface.durationSpinBox.value())
        return {
                "Name":name,
                "Duration":duration
            }

if __name__ == "__main__":
    app = QtWidgets.QApplication(["my_app"])
    rest_input_window = RestInputWindow("rest input")
    # rest_input_window.run()