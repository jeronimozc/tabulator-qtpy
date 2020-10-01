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
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QHeaderView, QMenu, QTableWidget, QTableWidgetItem

from settings import Settings


class DocumentTable(QTableWidget):

    m_settings = Settings()


    def __init__(self, parent=None):
        super(DocumentTable, self).__init__(parent)

        self.setAttribute(Qt.WA_DeleteOnClose)

        # Creates a default document
        self.setColumnCount(self.m_settings.newDocumentColumns)
        self.setRowCount(self.m_settings.newDocumentRows)

        # Enable context menus
        hHeaderView = self.horizontalHeader()
        hHeaderView.setContextMenuPolicy(Qt.CustomContextMenu)
        hHeaderView.customContextMenuRequested.connect(self.contextMenuHorizontalHeader)

        vHeaderView = self.verticalHeader()
        vHeaderView.setContextMenuPolicy(Qt.CustomContextMenu)
        vHeaderView.customContextMenuRequested.connect(self.contextMenuVerticalHeader)


    def setSettings(self, settings):
        """
        Sets the user preferences.
        """
        self.m_settings = settings


    def createDocument(self):
        """
        Creates a document.
        """

        # Creates a new document
        self.setColumnCount(self.m_settings.newDocumentColumns)
        self.setRowCount(self.m_settings.newDocumentRows)

        # Set header items
        self.setHorizontalHeaderItems(self.m_settings.horizontalHeaderLabels)
        self.setVerticalHeaderItems(self.m_settings.verticalHeaderLabels)


    def setHorizontalHeaderItems(self, type):
        """
        Sets the horizontal header items.
        """
        for column in range(0, self.columnCount()):

            number = column

            item = QTableWidgetItem()
            item.setTextAlignment(Qt.AlignCenter)
            item.setText(self.headerItemText(number, type))

            self.setHorizontalHeaderItem(column, item)


    def setVerticalHeaderItems(self, type):
        """
        Sets the vertical header items.
        """
        for row in range(0, self.rowCount()):

            number = row

            item = QTableWidgetItem()
            item.setTextAlignment(Qt.AlignCenter)
            item.setText(self.headerItemText(number, type))

            self.setVerticalHeaderItem(row, item)


    def headerItemText(self, number, type):
        """
        Returns the header item text.
        """
        if type == 1:
            return self.numberToDecimal(number)
        elif type == 0:
            return self.numberToLetter(number)
        else:
            return ''


    def numberToDecimal(self, number):
        """
        Returns a string equivalent of the number according to the base 10.
        """
        return f'{number + 1}'


    def numberToLetter(self, number):
        """
        Returns a string equivalent of the number according to the base 26.
        """
        chars = ''
        number += 1

        while number > 0:
            number -= 1
            chars = chr(number % 26 + 65) + chars
            number //= 26

        return chars


    def contextMenuHorizontalHeader(self, pos):
        """
        Creates a context menu for the horizonzal header.
        """
        menuLabel = QMenu('Label', self)
        menuLabel.setIcon(QIcon.fromTheme('tag', QIcon(':/icons/actions/16/tag.svg')))
        menuLabel.setStatusTip('Change label')
        menuLabel.setToolTip('Change label')

        contextMenu = QMenu(self)
        contextMenu.addMenu(menuLabel)
        contextMenu.exec_(self.mapToGlobal(pos))


    def contextMenuVerticalHeader(self, pos):
        """
        Creates a context menu for the vertical header.
        """
        menuLabel = QMenu('Label', self)
        menuLabel.setIcon(QIcon.fromTheme('tag', QIcon(':/icons/actions/16/tag.svg')))
        menuLabel.setStatusTip('Change label')
        menuLabel.setToolTip('Change label')

        contextMenu = QMenu(self)
        contextMenu.addMenu(menuLabel)
        contextMenu.exec_(self.mapToGlobal(pos))
