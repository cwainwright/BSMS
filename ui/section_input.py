# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'section_input.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(255, 96)
        self.formLayout = QtWidgets.QFormLayout(Dialog)
        self.formLayout.setObjectName("formLayout")
        self.sectionLabel = QtWidgets.QLabel(Dialog)
        self.sectionLabel.setObjectName("sectionLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.sectionLabel)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.sectionLineEdit = QtWidgets.QLineEdit(Dialog)
        self.sectionLineEdit.setObjectName("sectionLineEdit")
        self.horizontalLayout.addWidget(self.sectionLineEdit)
        self.sectionComboBox = QtWidgets.QComboBox(Dialog)
        self.sectionComboBox.setEnabled(True)
        self.sectionComboBox.setMaximumSize(QtCore.QSize(32, 32))
        self.sectionComboBox.setObjectName("sectionComboBox")
        self.sectionComboBox.addItem("")
        self.sectionComboBox.addItem("")
        self.sectionComboBox.addItem("")
        self.sectionComboBox.addItem("")
        self.sectionComboBox.addItem("")
        self.sectionComboBox.addItem("")
        self.sectionComboBox.addItem("")
        self.horizontalLayout.addWidget(self.sectionComboBox)
        self.formLayout.setLayout(0, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.SpanningRole, self.buttonBox)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept) # type: ignore
        self.buttonBox.rejected.connect(Dialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.sectionLabel.setText(_translate("Dialog", "Section"))
        self.sectionComboBox.setItemText(0, _translate("Dialog", "Intro"))
        self.sectionComboBox.setItemText(1, _translate("Dialog", "Verse"))
        self.sectionComboBox.setItemText(2, _translate("Dialog", "Pre-Chorus"))
        self.sectionComboBox.setItemText(3, _translate("Dialog", "Chorus"))
        self.sectionComboBox.setItemText(4, _translate("Dialog", "Bridge"))
        self.sectionComboBox.setItemText(5, _translate("Dialog", "Outro"))
        self.sectionComboBox.setItemText(6, _translate("Dialog", "Custom"))
