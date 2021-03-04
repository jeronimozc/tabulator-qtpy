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

from PySide2.QtCore import Qt
from PySide2.QtGui import QKeySequence
from PySide2.QtWidgets import QAbstractItemView, QAction, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget


class KeyboardShortcutsPage(QWidget):

    def __init__(self, mainWindow, parent=None):
        super().__init__(parent)

        listHeaderLabels = [self.tr('Name'), self.tr('Shortcut'), self.tr('Description')]

        tableBox = QTableWidget(0, len(listHeaderLabels), self)
        tableBox.setHorizontalHeaderLabels(listHeaderLabels)
        tableBox.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
        tableBox.horizontalHeader().setStretchLastSection(True)
        tableBox.verticalHeader().setVisible(False)
        tableBox.setEditTriggers(QAbstractItemView.NoEditTriggers)
        tableBox.setSelectionMode(QAbstractItemView.NoSelection)
        tableBox.setFocusPolicy(Qt.NoFocus)

        listActionItems = mainWindow.findChildren(QAction)
        for actionItem in listActionItems:

            if not actionItem.shortcut().isEmpty():
                idx = tableBox.rowCount()

                tableBox.setRowCount(idx + 1)
                tableBox.setItem(idx, 0, QTableWidgetItem(actionItem.icon(), actionItem.text()))
                tableBox.setItem(idx, 1, QTableWidgetItem(actionItem.shortcut().toString(QKeySequence.NativeText)))
                tableBox.setItem(idx, 2, QTableWidgetItem(actionItem.data()))

        tableBox.resizeColumnsToContents()

        # Main layout
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(tableBox)


    def title(self):

        return self.tr('Keyboard Shortcuts')


    def setZeroMargins(self):

        self.layout.setContentsMargins(0, 0, 0, 0)
