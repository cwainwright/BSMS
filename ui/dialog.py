# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        Dialog.resize(200, 150)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.messageLabel = QtWidgets.QLabel(Dialog)
        self.messageLabel.setObjectName("messageLabel")
        self.gridLayout.addWidget(self.messageLabel, 0, 0, 1, 1)
        self.dialogButtons = QtWidgets.QDialogButtonBox(Dialog)
        self.dialogButtons.setOrientation(QtCore.Qt.Horizontal)
        self.dialogButtons.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.dialogButtons.setObjectName("dialogButtons")
        self.gridLayout.addWidget(self.dialogButtons, 1, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.dialogButtons.accepted.connect(Dialog.accept)
        self.dialogButtons.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.messageLabel.setText(_translate("Dialog", "TextLabel"))