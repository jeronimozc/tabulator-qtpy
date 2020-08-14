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
from PySide2.QtWidgets import QApplication, QDialog, QDialogButtonBox, QVBoxLayout


class PreferencesDialog(QDialog):

    def __init__(self, parent=None):
        """
        Initializes the PreferencesDialog class.
        """
        super(PreferencesDialog, self).__init__(parent)

        self.organizationName = QApplication.organizationName()
        self.organizationDomain = QApplication.organizationDomain()
        self.applicationName = QApplication.applicationName()
        self.applicationDescription = 'A CSV editor written in Qt for Python.'
        self.applicationVersion = QApplication.applicationVersion()

        self.setWindowTitle(f'Preferences')

        self.setupUI()

        self.readSettings()


    def setupUI(self):
        """
        Setup user interface.
        """

        # Button box
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.RestoreDefaults | QDialogButtonBox.Ok | QDialogButtonBox.Apply | QDialogButtonBox.Cancel)
        self.buttonBox.button(QDialogButtonBox.RestoreDefaults).clicked.connect(self.onButtonDefaultsClicked)
        self.buttonBox.accepted.connect(self.onButtonOkClicked)
        self.buttonBox.button(QDialogButtonBox.Apply).clicked.connect(self.onButtonApplyClicked)
        self.buttonBox.button(QDialogButtonBox.Apply).setEnabled(False)
        self.buttonBox.rejected.connect(self.onButtonCancelClicked)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.buttonBox)

        self.setLayout(layout)


    def readSettings(self):
        """
        Restores user preferences and other application settings.
        """
        settings = QSettings()

        geometry = settings.value('PreferencesDialog/geometry', QByteArray())
        if geometry:
            # Restore dialog geometry
            self.restoreGeometry(geometry)
        else:
            # Center dialog
            availableGeometry = QRect(QApplication.desktop().availableGeometry(self))
            self.resize(availableGeometry.width() / 3, availableGeometry.height() / 3);
            self.move((availableGeometry.width() - self.width()) / 2, (availableGeometry.height() - self.height()) / 2);


    def writeSettings(self):
        """
        Saves user preferences and other application settings.
        """
        settings = QSettings()

        settings.setValue('PreferencesDialog/geometry', self.saveGeometry())


    def closeEvent(self, event):
        """
        Processes the close event.

        Args:
            event (QCloseEvent): The close event.
        """

        self.writeSettings()
        event.accept()


    def onButtonDefaultsClicked(self):
        """
        Restores the default values of the user preferences.
        """
        pass


    def onButtonOkClicked(self):
        """
        Fires the Close event to terminate the dialog with saving the user preferences.
        """

        self.writeSettings()
        self.close()


    def onButtonApplyClicked(self):
        """
        Saves the user preferences.
        """

        self.writeSettings()


    def onButtonCancelClicked(self):
        """
        Fires the Close event to terminate the dialog without saving the user preferences.
        """

        self.close()
