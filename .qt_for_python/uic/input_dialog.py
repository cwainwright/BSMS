# Form implementation generated from reading ui file '/Users/christopherwainwright/Documents/Git Repositories/BSMS/ui/input_dialog.ui'
#
# Created by: PyQt6 UI code generator 6.2.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_InputDialog(object):
    def setupUi(self, InputDialog):
        InputDialog.setObjectName("InputDialog")
        InputDialog.resize(200, 150)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(InputDialog.sizePolicy().hasHeightForWidth())
        InputDialog.setSizePolicy(sizePolicy)
        self.verticalLayout = QtWidgets.QVBoxLayout(InputDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.messageLabel = QtWidgets.QLabel(InputDialog)
        self.messageLabel.setObjectName("messageLabel")
        self.verticalLayout.addWidget(self.messageLabel)
        self.fieldInput = QtWidgets.QLineEdit(InputDialog)
        self.fieldInput.setObjectName("fieldInput")
        self.verticalLayout.addWidget(self.fieldInput)
        self.inputButtons = QtWidgets.QDialogButtonBox(InputDialog)
        self.inputButtons.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.inputButtons.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.inputButtons.setObjectName("inputButtons")
        self.verticalLayout.addWidget(self.inputButtons)

        self.retranslateUi(InputDialog)
        self.inputButtons.accepted.connect(InputDialog.accept) # type: ignore
        self.inputButtons.rejected.connect(InputDialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(InputDialog)

    def retranslateUi(self, InputDialog):
        _translate = QtCore.QCoreApplication.translate
        InputDialog.setWindowTitle(_translate("InputDialog", "Dialog"))
        self.messageLabel.setText(_translate("InputDialog", "TextLabel"))
