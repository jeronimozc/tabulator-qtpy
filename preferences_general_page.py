# This Python file uses the following encoding: utf-8
#
# Copyright 2020-2021 NotNypical, <https://notnypical.github.io>.
#
# This file is part of Tabulator-QtPy, <https://github.com/notnypical/tabulator-qtpy>.
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
from PySide2.QtWidgets import QCheckBox, QFormLayout, QGroupBox, QLabel, QSpinBox, QVBoxLayout, QWidget


class PreferencesGeneralPage(QWidget):

    preferencesChanged = Signal()


    def __init__(self, parent=None):
        super().__init__(parent)

        # Title
        title = QLabel(self.tr('<strong style="font-size:large;">General</strong>'))

        # Content: Geometry & State

        self._chkRestoreApplicationGeometry = QCheckBox(self.tr('Save and restore the application geometry'))
        self._chkRestoreApplicationGeometry.stateChanged.connect(self._onPreferencesChanged)

        self._chkRestoreApplicationState = QCheckBox(self.tr('Save and restore the application state'))
        self._chkRestoreApplicationState.stateChanged.connect(self._onPreferencesChanged)

        geometryStateLayout = QVBoxLayout()
        geometryStateLayout.addWidget(self._chkRestoreApplicationGeometry)
        geometryStateLayout.addWidget(self._chkRestoreApplicationState)

        geometryStateGroup = QGroupBox(self.tr('Geometry && State'))
        geometryStateGroup.setLayout(geometryStateLayout)

        # Content: Recently Opened Documents

        self._spbMaximumRecentDocuments = QSpinBox()
        self._spbMaximumRecentDocuments.setRange(0, 25)
        self._spbMaximumRecentDocuments.setToolTip(self.tr('Maximum number of recently opened documents'))
        self._spbMaximumRecentDocuments.valueChanged.connect(self._onPreferencesChanged)
        self._spbMaximumRecentDocuments.valueChanged[int].connect(self._onMaximumRecentDocumentsChanged)

        self._chkRestoreRecentDocuments = QCheckBox(self.tr('Save and restore documents'))
        self._chkRestoreRecentDocuments.stateChanged.connect(self._onPreferencesChanged)

        recentDocumentsFormLayout = QFormLayout()
        recentDocumentsFormLayout.addRow(self.tr('Number of documents'), self._spbMaximumRecentDocuments)

        recentDocumentsLayout = QVBoxLayout()
        recentDocumentsLayout.addLayout(recentDocumentsFormLayout)
        recentDocumentsLayout.addWidget(self._chkRestoreRecentDocuments)

        recentDocumentsGroup = QGroupBox(self.tr('Recently Opened Documents'))
        recentDocumentsGroup.setLayout(recentDocumentsLayout)

        # Main layout
        self._layout = QVBoxLayout(self)
        self._layout.addWidget(title)
        self._layout.addWidget(geometryStateGroup)
        self._layout.addWidget(recentDocumentsGroup)
        self._layout.addStretch(1)


    def setZeroMargins(self):

        self._layout.setContentsMargins(0, 0, 0, 0)


    def title(self):

        return self.tr('General')


    def _onPreferencesChanged(self):

        self.preferencesChanged.emit()


    def _onMaximumRecentDocumentsChanged(self, val):

        self._chkRestoreRecentDocuments.setEnabled(val > 0)


    def setRestoreApplicationGeometry(self, checked):

        self._chkRestoreApplicationGeometry.setChecked(checked)


    def restoreApplicationGeometry(self):

        return self._chkRestoreApplicationGeometry.isChecked()


    def setRestoreApplicationState(self, checked):

        self._chkRestoreApplicationState.setChecked(checked)


    def restoreApplicationState(self):

        return self._chkRestoreApplicationState.isChecked()


    def setMaximumRecentDocuments(self, val):

        self._spbMaximumRecentDocuments.setValue(val)


    def maximumRecentDocuments(self):

        return self._spbMaximumRecentDocuments.value()


    def setRestoreRecentDocuments(self, checked):

        self._chkRestoreRecentDocuments.setChecked(checked)


    def restoreRecentDocuments(self):

        return self._chkRestoreRecentDocuments.isChecked()
