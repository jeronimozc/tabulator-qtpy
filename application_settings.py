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

from PySide2.QtCore import Signal
from PySide2.QtWidgets import QCheckBox, QGroupBox, QLabel, QVBoxLayout, QWidget


class ApplicationSettings(QWidget):

    settingChanged = Signal()


    def __init__(self, parent=None):
        """
        Initializes the ApplicationSettings class.
        """
        super(ApplicationSettings, self).__init__(parent)

        label = QLabel('<strong style="font-size:large;">Application</strong>')

        # Geometries
        self.chkRestoreWindowGeometry = QCheckBox('Save and restore window geometry')
        self.chkRestoreWindowGeometry.stateChanged.connect(self.onSettingChanged)

        self.chkRestoreDialogGeometry = QCheckBox('Save and restore dialog geometry')
        self.chkRestoreDialogGeometry.stateChanged.connect(self.onSettingChanged)

        geometryLayout = QVBoxLayout()
        geometryLayout.addWidget(self.chkRestoreWindowGeometry)
        geometryLayout.addWidget(self.chkRestoreDialogGeometry)

        geometryGroup = QGroupBox('Geometries')
        geometryGroup.setLayout(geometryLayout)

        # Main layout
        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(geometryGroup)
        layout.addStretch()

        self.setLayout(layout)


    def onSettingChanged(self):
        """
        Emits signal that a setting has been changed.
        """
        self.settingChanged.emit()


    def title(self):
        """
        Returns title of the application settings.
        """
        return 'Application'


    def restoreWindowGeometry(self):
        """
        Returns setting whether the main window geometry should be restored.
        """
        return self.chkRestoreWindowGeometry.isChecked()


    def setRestoreWindowGeometry(self, checked):
        """
        Sets setting whether the main window geometry should be restored.
        """
        self.chkRestoreWindowGeometry.setChecked(checked)


    def restoreDialogGeometry(self):
        """
        Returns setting whether the dialog geometry should be restored.
        """
        return self.chkRestoreDialogGeometry.isChecked()


    def setRestoreDialogGeometry(self, checked):
        """
        Sets setting whether the dialog geometry should be restored.
        """
        self.chkRestoreDialogGeometry.setChecked(checked)
