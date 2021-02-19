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
from PySide2.QtWidgets import QFormLayout, QGroupBox, QLabel, QSpinBox, QVBoxLayout, QWidget


class PreferencesDocumentsPage(QWidget):

    preferencesChanged = Signal()


    def __init__(self, parent=None):
        super().__init__(parent)

        # Title
        title = QLabel(self.tr('<strong style="font-size:large;">Documents</strong>'))

        # Recently Opened Documents
        self.spbMaximumRecentDocuments = QSpinBox()
        self.spbMaximumRecentDocuments.setRange(0, 25)
        self.spbMaximumRecentDocuments.setToolTip(self.tr('Maximum number of recently opened documents'))
        self.spbMaximumRecentDocuments.valueChanged.connect(self.onPreferencesChanged)

        recentDocumentsLayout = QFormLayout()
        recentDocumentsLayout.addRow(self.tr('Number of documents'), self.spbMaximumRecentDocuments)

        recentDocumentsGroup = QGroupBox(self.tr('Recently Opened Documents'))
        recentDocumentsGroup.setLayout(recentDocumentsLayout)

        # Main layout
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(title)
        self.layout.addWidget(recentDocumentsGroup)
        self.layout.addStretch()


    def setZeroMargins(self):

        self.layout.setContentsMargins(0, 0, 0, 0)


    def title(self):

        return self.tr('Documents')


    def onPreferencesChanged(self):

        self.preferencesChanged.emit()


    def setMaximumRecentDocuments(self, val):

        self.spbMaximumRecentDocuments.setValue(val)


    def maximumRecentDocuments(self):

        return self.spbMaximumRecentDocuments.value()
