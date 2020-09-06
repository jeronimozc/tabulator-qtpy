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

from PySide2.QtCore import Qt
from PySide2.QtGui import QKeySequence
from PySide2.QtWidgets import QAbstractItemView, QAction, QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget


class KeyboardShortcutsPage(QWidget):

    def __init__(self, mainWindow, parent=None):
        """
        Initializes the KeyboardShortcutsPage class.
        """
        super(KeyboardShortcutsPage, self).__init__(parent)

        listHHeaderLabels = ['Name', 'Shortcut', 'Description']

        listShortcutActionItems = []
        listActionItems = mainWindow.findChildren(QAction)
        for actionItem in listActionItems:
            if not actionItem.shortcut().isEmpty():
                listShortcutActionItems.append(actionItem)

        tableBox = QTableWidget(len(listShortcutActionItems), len(listHHeaderLabels), self)
        tableBox.setHorizontalHeaderLabels(listHHeaderLabels)
        tableBox.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
        tableBox.horizontalHeader().setStretchLastSection(True)
        tableBox.verticalHeader().setVisible(False)
        tableBox.setEditTriggers(QAbstractItemView.NoEditTriggers)
        tableBox.setSelectionMode(QAbstractItemView.NoSelection)
        tableBox.setFocusPolicy(Qt.NoFocus)

        for index in range(len(listShortcutActionItems)):
            tableBox.setItem(index, 0, QTableWidgetItem(listShortcutActionItems[index].icon(), listShortcutActionItems[index].text()))
            tableBox.setItem(index, 1, QTableWidgetItem(listShortcutActionItems[index].shortcut().toString(QKeySequence.NativeText)))
            tableBox.setItem(index, 2, QTableWidgetItem(listShortcutActionItems[index].statusTip()))

        # Main layout
        layout = QVBoxLayout()
        layout.addWidget(tableBox, 1)

        self.setLayout(layout)
