# This Python file uses the following encoding: utf-8
#
# Copyright 2020 NotNypical, <https://notnypical.github.io>.
#
# This file is part of pyTabulator.
#
# pyTabulator is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyTabulator is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyTabulator.  If not, see <https://www.gnu.org/licenses/>.
#

from PySide2.QtCore import QByteArray, QRect, QSettings
from PySide2.QtWidgets import (QApplication, QCheckBox, QDialog, QDialogButtonBox, QGroupBox, QHBoxLayout, QLabel,
                               QListWidget, QStackedWidget, QVBoxLayout, QWidget)


class PreferencesDialog(QDialog):

    saveSettings = False


    def __init__(self, parent=None):
        """
        Initializes the PreferencesDialog class.
        """
        super(PreferencesDialog, self).__init__(parent)

        # Settings box
        self.stackApplication = QWidget()

        self.stackApplicationPage()

        stackedBox = QStackedWidget()
        stackedBox.addWidget(self.stackApplication)
        stackedBox.setCurrentIndex(0)

        listBox = QListWidget()
        listBox.addItem('Application')
        listBox.setCurrentRow(stackedBox.currentIndex())
        listBox.currentRowChanged.connect(stackedBox.setCurrentIndex)

        settingsBox = QHBoxLayout()
        settingsBox.addWidget(listBox, 1)
        settingsBox.addWidget(stackedBox, 3)

        # Button box
        buttonBox = QDialogButtonBox(QDialogButtonBox.RestoreDefaults | QDialogButtonBox.Ok | QDialogButtonBox.Apply | QDialogButtonBox.Cancel)
        self.buttonApply = buttonBox.button(QDialogButtonBox.Apply)
        buttonBox.button(QDialogButtonBox.RestoreDefaults).clicked.connect(self.onButtonDefaultsClicked)
        buttonBox.accepted.connect(self.onButtonOkClicked)
        buttonBox.button(QDialogButtonBox.Apply).clicked.connect(self.onButtonApplyClicked)
        buttonBox.rejected.connect(self.close)

        # Main layout
        layout = QVBoxLayout()
        layout.addLayout(settingsBox, 1)
        layout.addWidget(buttonBox)

        self.setLayout(layout)

        self.readSettings()


    def stackApplicationPage(self):
        """
        Displays the application settings page.
        """
        label = QLabel('<strong style="font-size:large">Application</strong>')

        # Geometries
        self.checkboxGeometryWindowRestore = QCheckBox('Save and restore window geometry', self)
        self.checkboxGeometryWindowRestore.stateChanged.connect(self.onSettingsChanged)

        self.checkboxGeometryDialogRestore = QCheckBox('Save and restore dialog geometry', self)
        self.checkboxGeometryDialogRestore.stateChanged.connect(self.onSettingsChanged)

        geometryLayout = QVBoxLayout()
        geometryLayout.addWidget(self.checkboxGeometryWindowRestore)
        geometryLayout.addWidget(self.checkboxGeometryDialogRestore)

        geometryGroup = QGroupBox('Geometries')
        geometryGroup.setLayout(geometryLayout)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(geometryGroup)
        layout.addStretch()

        self.stackApplication.setLayout(layout)


    def windowGeometry(self):
        """
        Returns the geometry of the widget.
        """
        return self.saveGeometry()


    def setWindowGeometry(self, geometry):
        """
        Sets the geometry of the widget.
        """
        if geometry:
            self.restoreGeometry(geometry)
        else:
            availableGeometry = QRect(QApplication.desktop().availableGeometry(self))
            self.resize(availableGeometry.width() / 2, availableGeometry.height() / 2)
            self.move((availableGeometry.width() - self.width()) / 2, (availableGeometry.height() - self.height()) / 2)


    def readSettings(self):
        """
        Restores user preferences and other dialog properties.
        """
        settings = QSettings()

        # Update UI: Application
        self.checkboxGeometryWindowRestore.setChecked(self.valueToBool(settings.value('Settings/restoreWindowGeometry', True)))
        self.checkboxGeometryDialogRestore.setChecked(self.valueToBool(settings.value('Settings/restoreDialogGeometry', True)))

        # Update UI: Button
        self.buttonApply.setEnabled(False)


    def writeSettings(self):
        """
        Saves user preferences and other dialog properties.
        """
        settings = QSettings()

        # Store user preferences
        if self.saveSettings:

            # Application
            settings.setValue('Settings/restoreWindowGeometry', self.checkboxGeometryWindowRestore.isChecked())
            settings.setValue('Settings/restoreDialogGeometry', self.checkboxGeometryDialogRestore.isChecked())

            # Update UI: Button
            self.buttonApply.setEnabled(False)
            self.saveSettings = False


    @staticmethod
    def valueToBool(value):
        """
        Converts a specified value to an equivalent Boolean value.

        Args:
            value (bool): The specified value.

        Returns:
            bool: The equivalent Boolean value.
        """
        return value.lower() == 'true' if isinstance(value, str) else bool(value)


    def closeEvent(self, event):
        """
        Processes the close event.

        Args:
            event (QCloseEvent): The close event.
        """
        self.writeSettings()
        event.accept()


    def onSettingsChanged(self):
        """
        Enables the apply button if settings have been changed.
        """
        self.buttonApply.setEnabled(True)


    def onButtonDefaultsClicked(self):
        """
        Restores default values of user preferences.
        """

        # Application
        self.checkboxGeometryWindowRestore.setChecked(True)
        self.checkboxGeometryDialogRestore.setChecked(True)


    def onButtonOkClicked(self):
        """
        Fires the Close event to terminate the dialog with saving user preferences.
        """
        self.saveSettings = True
        self.close()


    def onButtonApplyClicked(self):
        """
        Saves user preferences.
        """
        self.saveSettings = True
        self.writeSettings()
