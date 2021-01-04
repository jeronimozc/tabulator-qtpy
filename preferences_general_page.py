# This Python file uses the following encoding: utf-8
#
# Copyright 2020-2021 NotNypical, <https://notnypical.github.io>.
#
# This file is part of Tabulator-QtPy.
#
# Tabulator-QtPy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Tabulator-QtPy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Tabulator-QtPy.  If not, see <https://www.gnu.org/licenses/>.
#

from PySide2.QtCore import Signal
from PySide2.QtWidgets import QCheckBox, QGroupBox, QLabel, QVBoxLayout, QWidget


class PreferencesGeneralPage(QWidget):

    settingsChanged = Signal()


    def __init__(self, parent=None):
        super().__init__(parent)

        # Title
        title = QLabel(self.tr('<strong style="font-size:large;">General</strong>'))

        # State & Geometries
        self.chkRestoreApplicationState = QCheckBox(self.tr('Save and restore the application state'))
        self.chkRestoreApplicationState.stateChanged.connect(self.onSettingsChanged)

        self.chkRestoreApplicationGeometry = QCheckBox(self.tr('Save and restore application geometry'))
        self.chkRestoreApplicationGeometry.stateChanged.connect(self.onSettingsChanged)

        self.chkRestoreDialogGeometry = QCheckBox(self.tr('Save and restore dialog geometry'))
        self.chkRestoreDialogGeometry.stateChanged.connect(self.onSettingsChanged)

        stateGeometryLayout = QVBoxLayout()
        stateGeometryLayout.addWidget(self.chkRestoreApplicationState)
        stateGeometryLayout.addWidget(self.chkRestoreApplicationGeometry)
        stateGeometryLayout.addWidget(self.chkRestoreDialogGeometry)

        stateGeometryGroup = QGroupBox(self.tr('State && Geometries'))
        stateGeometryGroup.setLayout(stateGeometryLayout)

        # Main layout
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(title)
        self.layout.addWidget(stateGeometryGroup)
        self.layout.addStretch()


    def title(self):

        return self.tr('General')


    def setZeroMargins(self):

        self.layout.setContentsMargins(0, 0, 0, 0)


    def onSettingsChanged(self):

        self.settingsChanged.emit()


    def setRestoreApplicationState(self, checked):

        self.chkRestoreApplicationState.setChecked(checked)


    def restoreApplicationState(self):

        return self.chkRestoreApplicationState.isChecked()


    def setRestoreApplicationGeometry(self, checked):

        self.chkRestoreApplicationGeometry.setChecked(checked)


    def restoreApplicationGeometry(self):

        return self.chkRestoreApplicationGeometry.isChecked()


    def setRestoreDialogGeometry(self, checked):

        self.chkRestoreDialogGeometry.setChecked(checked)


    def restoreDialogGeometry(self):

        return self.chkRestoreDialogGeometry.isChecked()
