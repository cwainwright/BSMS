# Form implementation generated from reading ui file '/Users/christopherwainwright/Documents/Git Repositories/BSMS/ui/metadata_input_dialog.ui'
#
# Created by: PyQt6 UI code generator 6.2.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MetadataDialog(object):
    def setupUi(self, MetadataDialog):
        MetadataDialog.setObjectName("MetadataDialog")
        MetadataDialog.resize(374, 531)
        self.gridLayout = QtWidgets.QGridLayout(MetadataDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.mapInformationContainer = QtWidgets.QGroupBox(MetadataDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mapInformationContainer.sizePolicy().hasHeightForWidth())
        self.mapInformationContainer.setSizePolicy(sizePolicy)
        self.mapInformationContainer.setObjectName("mapInformationContainer")
        self.formLayout = QtWidgets.QFormLayout(self.mapInformationContainer)
        self.formLayout.setObjectName("formLayout")
        self.projectNameLabel = QtWidgets.QLabel(self.mapInformationContainer)
        self.projectNameLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.projectNameLabel.setObjectName("projectNameLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.projectNameLabel)
        self.projectNameInput = QtWidgets.QLineEdit(self.mapInformationContainer)
        self.projectNameInput.setObjectName("projectNameInput")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.projectNameInput)
        self.versionLabel = QtWidgets.QLabel(self.mapInformationContainer)
        self.versionLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.versionLabel.setObjectName("versionLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.versionLabel)
        self.versionInput = QtWidgets.QLineEdit(self.mapInformationContainer)
        self.versionInput.setObjectName("versionInput")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.versionInput)
        self.songSubNameLabel = QtWidgets.QLabel(self.mapInformationContainer)
        self.songSubNameLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.songSubNameLabel.setObjectName("songSubNameLabel")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.ItemRole.LabelRole, self.songSubNameLabel)
        self.songSubNameInput = QtWidgets.QLineEdit(self.mapInformationContainer)
        self.songSubNameInput.setObjectName("songSubNameInput")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.ItemRole.FieldRole, self.songSubNameInput)
        self.songAuthorNameLabel = QtWidgets.QLabel(self.mapInformationContainer)
        self.songAuthorNameLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.songAuthorNameLabel.setObjectName("songAuthorNameLabel")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.ItemRole.LabelRole, self.songAuthorNameLabel)
        self.songAuthorNameInput = QtWidgets.QLineEdit(self.mapInformationContainer)
        self.songAuthorNameInput.setObjectName("songAuthorNameInput")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.ItemRole.FieldRole, self.songAuthorNameInput)
        self.levelAuthorNameLabel = QtWidgets.QLabel(self.mapInformationContainer)
        self.levelAuthorNameLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.levelAuthorNameLabel.setObjectName("levelAuthorNameLabel")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.ItemRole.LabelRole, self.levelAuthorNameLabel)
        self.levelAuthorNameInput = QtWidgets.QLineEdit(self.mapInformationContainer)
        self.levelAuthorNameInput.setObjectName("levelAuthorNameInput")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.ItemRole.FieldRole, self.levelAuthorNameInput)
        self.gridLayout.addWidget(self.mapInformationContainer, 1, 0, 1, 1)
        self.titleLabel = QtWidgets.QLabel(MetadataDialog)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.titleLabel.setFont(font)
        self.titleLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.titleLabel.setObjectName("titleLabel")
        self.gridLayout.addWidget(self.titleLabel, 0, 0, 1, 1)
        self.mapMetadataContainer = QtWidgets.QGroupBox(MetadataDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mapMetadataContainer.sizePolicy().hasHeightForWidth())
        self.mapMetadataContainer.setSizePolicy(sizePolicy)
        self.mapMetadataContainer.setObjectName("mapMetadataContainer")
        self.formLayout_2 = QtWidgets.QFormLayout(self.mapMetadataContainer)
        self.formLayout_2.setObjectName("formLayout_2")
        self.BPMLabel = QtWidgets.QLabel(self.mapMetadataContainer)
        self.BPMLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.BPMLabel.setObjectName("BPMLabel")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.BPMLabel)
        self.BPMSpinbox = QtWidgets.QDoubleSpinBox(self.mapMetadataContainer)
        self.BPMSpinbox.setDecimals(1)
        self.BPMSpinbox.setMaximum(300.0)
        self.BPMSpinbox.setObjectName("BPMSpinbox")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.BPMSpinbox)
        self.songTimeOffsetLabel = QtWidgets.QLabel(self.mapMetadataContainer)
        self.songTimeOffsetLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.songTimeOffsetLabel.setObjectName("songTimeOffsetLabel")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.songTimeOffsetLabel)
        self.songTimeOffsetSpinbox = QtWidgets.QDoubleSpinBox(self.mapMetadataContainer)
        self.songTimeOffsetSpinbox.setDecimals(0)
        self.songTimeOffsetSpinbox.setMaximum(10.0)
        self.songTimeOffsetSpinbox.setObjectName("songTimeOffsetSpinbox")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.songTimeOffsetSpinbox)
        self.shuffleLabel = QtWidgets.QLabel(self.mapMetadataContainer)
        self.shuffleLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.shuffleLabel.setObjectName("shuffleLabel")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.ItemRole.LabelRole, self.shuffleLabel)
        self.shuffleSpinbox = QtWidgets.QDoubleSpinBox(self.mapMetadataContainer)
        self.shuffleSpinbox.setDecimals(1)
        self.shuffleSpinbox.setMaximum(1.0)
        self.shuffleSpinbox.setSingleStep(0.1)
        self.shuffleSpinbox.setObjectName("shuffleSpinbox")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.ItemRole.FieldRole, self.shuffleSpinbox)
        self.shuffleOffsetLabel = QtWidgets.QLabel(self.mapMetadataContainer)
        self.shuffleOffsetLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.shuffleOffsetLabel.setObjectName("shuffleOffsetLabel")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.ItemRole.LabelRole, self.shuffleOffsetLabel)
        self.shuffleOffsetSpinbox = QtWidgets.QDoubleSpinBox(self.mapMetadataContainer)
        self.shuffleOffsetSpinbox.setDecimals(1)
        self.shuffleOffsetSpinbox.setMaximum(2.0)
        self.shuffleOffsetSpinbox.setSingleStep(0.1)
        self.shuffleOffsetSpinbox.setProperty("value", 0.5)
        self.shuffleOffsetSpinbox.setObjectName("shuffleOffsetSpinbox")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.ItemRole.FieldRole, self.shuffleOffsetSpinbox)
        self.previewStartTimeLabel = QtWidgets.QLabel(self.mapMetadataContainer)
        self.previewStartTimeLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.previewStartTimeLabel.setObjectName("previewStartTimeLabel")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.ItemRole.LabelRole, self.previewStartTimeLabel)
        self.previewStartTimeSpinbox = QtWidgets.QSpinBox(self.mapMetadataContainer)
        self.previewStartTimeSpinbox.setObjectName("previewStartTimeSpinbox")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.ItemRole.FieldRole, self.previewStartTimeSpinbox)
        self.previewDurationLabel = QtWidgets.QLabel(self.mapMetadataContainer)
        self.previewDurationLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.previewDurationLabel.setObjectName("previewDurationLabel")
        self.formLayout_2.setWidget(5, QtWidgets.QFormLayout.ItemRole.LabelRole, self.previewDurationLabel)
        self.previewDurationSpinbox = QtWidgets.QSpinBox(self.mapMetadataContainer)
        self.previewDurationSpinbox.setProperty("value", 10)
        self.previewDurationSpinbox.setObjectName("previewDurationSpinbox")
        self.formLayout_2.setWidget(5, QtWidgets.QFormLayout.ItemRole.FieldRole, self.previewDurationSpinbox)
        self.songFilenameLabel = QtWidgets.QLabel(self.mapMetadataContainer)
        self.songFilenameLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.songFilenameLabel.setObjectName("songFilenameLabel")
        self.formLayout_2.setWidget(6, QtWidgets.QFormLayout.ItemRole.LabelRole, self.songFilenameLabel)
        self.songFilenameInput = QtWidgets.QLineEdit(self.mapMetadataContainer)
        self.songFilenameInput.setObjectName("songFilenameInput")
        self.formLayout_2.setWidget(6, QtWidgets.QFormLayout.ItemRole.FieldRole, self.songFilenameInput)
        self.coverImageFilenameLabel = QtWidgets.QLabel(self.mapMetadataContainer)
        self.coverImageFilenameLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.coverImageFilenameLabel.setObjectName("coverImageFilenameLabel")
        self.formLayout_2.setWidget(7, QtWidgets.QFormLayout.ItemRole.LabelRole, self.coverImageFilenameLabel)
        self.coverImageFilenameInput = QtWidgets.QLineEdit(self.mapMetadataContainer)
        self.coverImageFilenameInput.setObjectName("coverImageFilenameInput")
        self.formLayout_2.setWidget(7, QtWidgets.QFormLayout.ItemRole.FieldRole, self.coverImageFilenameInput)
        self.environmentLabel = QtWidgets.QLabel(self.mapMetadataContainer)
        self.environmentLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.environmentLabel.setObjectName("environmentLabel")
        self.formLayout_2.setWidget(8, QtWidgets.QFormLayout.ItemRole.LabelRole, self.environmentLabel)
        self.environmentNameSelector = QtWidgets.QComboBox(self.mapMetadataContainer)
        self.environmentNameSelector.setObjectName("environmentNameSelector")
        self.environmentNameSelector.addItem("")
        self.environmentNameSelector.addItem("")
        self.environmentNameSelector.addItem("")
        self.environmentNameSelector.addItem("")
        self.environmentNameSelector.addItem("")
        self.environmentNameSelector.addItem("")
        self.environmentNameSelector.addItem("")
        self.environmentNameSelector.addItem("")
        self.environmentNameSelector.addItem("")
        self.environmentNameSelector.addItem("")
        self.environmentNameSelector.addItem("")
        self.environmentNameSelector.addItem("")
        self.environmentNameSelector.addItem("")
        self.environmentNameSelector.addItem("")
        self.environmentNameSelector.addItem("")
        self.environmentNameSelector.addItem("")
        self.environmentNameSelector.addItem("")
        self.environmentNameSelector.addItem("")
        self.environmentNameSelector.addItem("")
        self.formLayout_2.setWidget(8, QtWidgets.QFormLayout.ItemRole.FieldRole, self.environmentNameSelector)
        self.allDirectionsEnvironmentNameLabel = QtWidgets.QLabel(self.mapMetadataContainer)
        self.allDirectionsEnvironmentNameLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.allDirectionsEnvironmentNameLabel.setObjectName("allDirectionsEnvironmentNameLabel")
        self.formLayout_2.setWidget(9, QtWidgets.QFormLayout.ItemRole.LabelRole, self.allDirectionsEnvironmentNameLabel)
        self.allDirectionsEnvironmentNameSelector = QtWidgets.QComboBox(self.mapMetadataContainer)
        self.allDirectionsEnvironmentNameSelector.setObjectName("allDirectionsEnvironmentNameSelector")
        self.allDirectionsEnvironmentNameSelector.addItem("")
        self.formLayout_2.setWidget(9, QtWidgets.QFormLayout.ItemRole.FieldRole, self.allDirectionsEnvironmentNameSelector)
        self.gridLayout.addWidget(self.mapMetadataContainer, 4, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(MetadataDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 5, 0, 1, 1)
        self.projectNameLabel.setBuddy(self.projectNameInput)
        self.versionLabel.setBuddy(self.versionInput)
        self.songSubNameLabel.setBuddy(self.songSubNameInput)
        self.songAuthorNameLabel.setBuddy(self.songAuthorNameInput)
        self.levelAuthorNameLabel.setBuddy(self.levelAuthorNameInput)
        self.BPMLabel.setBuddy(self.BPMSpinbox)
        self.songTimeOffsetLabel.setBuddy(self.songTimeOffsetSpinbox)
        self.shuffleLabel.setBuddy(self.shuffleSpinbox)
        self.shuffleOffsetLabel.setBuddy(self.shuffleOffsetSpinbox)
        self.previewStartTimeLabel.setBuddy(self.previewStartTimeSpinbox)
        self.previewDurationLabel.setBuddy(self.previewDurationSpinbox)
        self.songFilenameLabel.setBuddy(self.songFilenameInput)
        self.coverImageFilenameLabel.setBuddy(self.coverImageFilenameInput)
        self.environmentLabel.setBuddy(self.environmentNameSelector)
        self.allDirectionsEnvironmentNameLabel.setBuddy(self.allDirectionsEnvironmentNameSelector)

        self.retranslateUi(MetadataDialog)
        self.buttonBox.accepted.connect(MetadataDialog.accept) # type: ignore
        self.buttonBox.rejected.connect(MetadataDialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MetadataDialog)

    def retranslateUi(self, MetadataDialog):
        _translate = QtCore.QCoreApplication.translate
        MetadataDialog.setWindowTitle(_translate("MetadataDialog", "Dialog"))
        self.mapInformationContainer.setTitle(_translate("MetadataDialog", "Map Information"))
        self.projectNameLabel.setText(_translate("MetadataDialog", "Project Name"))
        self.versionLabel.setText(_translate("MetadataDialog", "Version"))
        self.versionInput.setText(_translate("MetadataDialog", "2.0.0"))
        self.songSubNameLabel.setText(_translate("MetadataDialog", "Song Sub-Name"))
        self.songAuthorNameLabel.setText(_translate("MetadataDialog", "Song Author Name"))
        self.levelAuthorNameLabel.setText(_translate("MetadataDialog", "Level Author Name"))
        self.titleLabel.setText(_translate("MetadataDialog", "Input Project Metadata"))
        self.mapMetadataContainer.setTitle(_translate("MetadataDialog", "Map Metadata"))
        self.BPMLabel.setText(_translate("MetadataDialog", "Beats-Per-Minute (Override)"))
        self.songTimeOffsetLabel.setText(_translate("MetadataDialog", "Song Time Offset"))
        self.shuffleLabel.setText(_translate("MetadataDialog", "Shuffle"))
        self.shuffleOffsetLabel.setText(_translate("MetadataDialog", "Shuffle Offset"))
        self.previewStartTimeLabel.setText(_translate("MetadataDialog", "Preview Start Time"))
        self.previewDurationLabel.setText(_translate("MetadataDialog", "Preview Duration"))
        self.songFilenameLabel.setText(_translate("MetadataDialog", "Song Filename"))
        self.songFilenameInput.setText(_translate("MetadataDialog", "song.wav"))
        self.coverImageFilenameLabel.setText(_translate("MetadataDialog", "Cover Image Filename"))
        self.coverImageFilenameInput.setText(_translate("MetadataDialog", "cover.jpg"))
        self.environmentLabel.setText(_translate("MetadataDialog", "Environment Name"))
        self.environmentNameSelector.setItemText(0, _translate("MetadataDialog", "DefaultEnvironment"))
        self.environmentNameSelector.setItemText(1, _translate("MetadataDialog", "OriginsEnvironment"))
        self.environmentNameSelector.setItemText(2, _translate("MetadataDialog", "TriangleEnvironment"))
        self.environmentNameSelector.setItemText(3, _translate("MetadataDialog", "NiceEnvironment"))
        self.environmentNameSelector.setItemText(4, _translate("MetadataDialog", "BigMirrorEnvironment"))
        self.environmentNameSelector.setItemText(5, _translate("MetadataDialog", "DragonsEnvironment"))
        self.environmentNameSelector.setItemText(6, _translate("MetadataDialog", "KDAEnvironment"))
        self.environmentNameSelector.setItemText(7, _translate("MetadataDialog", "MonstercatEnvironment"))
        self.environmentNameSelector.setItemText(8, _translate("MetadataDialog", "CrabRaveEnvironment"))
        self.environmentNameSelector.setItemText(9, _translate("MetadataDialog", "PanicEnvironment"))
        self.environmentNameSelector.setItemText(10, _translate("MetadataDialog", "RocketEnvironment"))
        self.environmentNameSelector.setItemText(11, _translate("MetadataDialog", "GreenDayEnvironment"))
        self.environmentNameSelector.setItemText(12, _translate("MetadataDialog", "GreenDayGrenadeEnvironment"))
        self.environmentNameSelector.setItemText(13, _translate("MetadataDialog", "TimbalandEnvironment"))
        self.environmentNameSelector.setItemText(14, _translate("MetadataDialog", "FitBeatEnvironment"))
        self.environmentNameSelector.setItemText(15, _translate("MetadataDialog", "LinkinParkEnvironment"))
        self.environmentNameSelector.setItemText(16, _translate("MetadataDialog", "BTSEnvironment"))
        self.environmentNameSelector.setItemText(17, _translate("MetadataDialog", "KaleidoscopeEnvironment"))
        self.environmentNameSelector.setItemText(18, _translate("MetadataDialog", "InterscopeEnvironment"))
        self.allDirectionsEnvironmentNameLabel.setText(_translate("MetadataDialog", "All-Directions Environment Name"))
        self.allDirectionsEnvironmentNameSelector.setItemText(0, _translate("MetadataDialog", "GlassDesertEnvironment"))
