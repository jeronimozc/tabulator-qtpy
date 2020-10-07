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
from PySide2.QtWidgets import QAction, QHeaderView, QInputDialog, QLineEdit, QMenu, QTableWidget, QTableWidgetItem

from settings import Settings


class DocumentTable(QTableWidget):

    m_settings = Settings()


    def __init__(self, parent=None):
        super(DocumentTable, self).__init__(parent)

        self.setAttribute(Qt.WA_DeleteOnClose)

        # Creates a default document
        self.setColumnCount(self.m_settings.defaultCellColumns)
        self.setRowCount(self.m_settings.defaultCellRows)

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
        self.setColumnCount(self.m_settings.defaultCellColumns)
        self.setRowCount(self.m_settings.defaultCellRows)

        # Set header items
        self.setHorizontalHeaderItems(self.m_settings.defaultHeaderLabelHorizontal)
        self.setVerticalHeaderItems(self.m_settings.defaultHeaderLabelVertical)


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
        if type == Settings.HeaderLabel.Binary:
            return self.numberToBinary(number)
        elif type == Settings.HeaderLabel.Octal:
            return self.numberToOctal(number)
        elif type == Settings.HeaderLabel.Decimal:
            return self.numberToDecimal(number)
        elif type == Settings.HeaderLabel.Hexadecimal:
            return self.numberToHexadecimal(number)
        elif type == Settings.HeaderLabel.Letter:
            return self.numberToLetter(number)
        else:
            return ''


    def numberToBinary(self, number):
        """
        Returns a string equivalent of the number according to the base 2.
        """
        return f'0b{number:b}'


    def numberToOctal(self, number):
        """
        Returns a string equivalent of the number according to the base 8.
        """
        return f'0o{number:o}'


    def numberToDecimal(self, number):
        """
        Returns a string equivalent of the number according to the base 10.
        """
        return f'{number + 1}'


    def numberToHexadecimal(self, number):
        """
        Returns a string equivalent of the number according to the base 16.
        """
        return f'0x{number:X}'


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
        Creates a context menu for the horizontal header.
        """
        index = self.indexAt(pos)

        # Label
        actionLabelLetter = QAction('Letter', self)
        actionLabelLetter.setStatusTip('Change label to a capital letter')
        actionLabelLetter.setToolTip('Change label to a capital letter')
        actionLabelLetter.triggered.connect( lambda: self.onActionLabelHorizontalTriggered(index.column(), Settings.HeaderLabel.Letter) )

        actionLabelNumber = QAction('Number', self)
        actionLabelNumber.setStatusTip('Change label to a decimal number')
        actionLabelNumber.setToolTip('Change label to a decimal number')
        actionLabelNumber.triggered.connect( lambda: self.onActionLabelHorizontalTriggered(index.column(), Settings.HeaderLabel.Decimal) )

        actionLabelCustom = QAction('Custom…', self)
        actionLabelCustom.setStatusTip('Customize label')
        actionLabelCustom.setToolTip('Customize label')
        actionLabelCustom.triggered.connect( lambda: self.onActionLabelHorizontalTriggered(index.column(), Settings.HeaderLabel.Custom) )

        # All labels
        actionLabelLetters = QAction('Letters', self)
        actionLabelLetters.setStatusTip('Change all labels to capital letters')
        actionLabelLetters.setToolTip('Change all labels to capital letters')
        actionLabelLetters.triggered.connect( lambda: self.onActionLabelAllHorizontalTriggered(Settings.HeaderLabel.Letter) )

        actionLabelNumbers = QAction('Numbers', self)
        actionLabelNumbers.setStatusTip('Change all labels to decimal numbers')
        actionLabelNumbers.setToolTip('Change all labels to decimal numbers')
        actionLabelNumbers.triggered.connect( lambda: self.onActionLabelAllHorizontalTriggered(Settings.HeaderLabel.Decimal) )

        # Menus
        menuLabel = QMenu('Label', self)
        menuLabel.setIcon(QIcon.fromTheme('tag', QIcon(':/icons/actions/16/tag.svg')))
        menuLabel.setStatusTip('Change label')
        menuLabel.setToolTip('Change label')
        menuLabel.addAction(actionLabelLetter)
        menuLabel.addAction(actionLabelNumber)
        menuLabel.addAction(actionLabelCustom)
        menuLabel.addSeparator()
        menuLabel.addAction(actionLabelLetters)
        menuLabel.addAction(actionLabelNumbers)

        contextMenu = QMenu(self)
        contextMenu.addMenu(menuLabel)
        contextMenu.exec_(self.mapToGlobal(pos))


    def onActionLabelHorizontalTriggered(self, column, type):
        """
        Updates a specific horizontal header item.
        """
        self.updateHorizontalHeaderItem(column, type)


    def onActionLabelAllHorizontalTriggered(self, type):
        """
        Updates all horizontal header items.
        """
        for column in range(0, self.columnCount()):
            self.updateHorizontalHeaderItem(column, type)


    def updateHorizontalHeaderItem(self, column, type):
        """
        Updates a horizontal header item.
        """
        number = column

        item = self.horizontalHeaderItem(column)

        if type == Settings.HeaderLabel.Custom:

            text, ok = QInputDialog().getText(self, "Horizontal Header Item",
                                              "Label:", QLineEdit.Normal, item.text(),
                                              self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

            if ok and text:
                item.setText(text)
        else:
            item.setText(self.headerItemText(number, type))


    def contextMenuVerticalHeader(self, pos):
        """
        Creates a context menu for the vertical header.
        """
        index = self.indexAt(pos)

        # Label
        actionLabelLetter = QAction('Letter', self)
        actionLabelLetter.setStatusTip('Change label to a capital letter')
        actionLabelLetter.setToolTip('Change label to a capital letter')
        actionLabelLetter.triggered.connect( lambda: self.onActionLabelVerticalTriggered(index.row(), Settings.HeaderLabel.Letter) )

        actionLabelNumber = QAction('Number', self)
        actionLabelNumber.setStatusTip('Change label to a decimal number')
        actionLabelNumber.setToolTip('Change label to a decimal number')
        actionLabelNumber.triggered.connect( lambda: self.onActionLabelVerticalTriggered(index.row(), Settings.HeaderLabel.Decimal) )

        actionLabelCustom = QAction('Custom…', self)
        actionLabelCustom.setStatusTip('Customize label')
        actionLabelCustom.setToolTip('Customize label')
        actionLabelCustom.triggered.connect( lambda: self.onActionLabelVerticalTriggered(index.row(), Settings.HeaderLabel.Custom) )

        # All labels
        actionLabelLetters = QAction('Letters', self)
        actionLabelLetters.setStatusTip('Change all labels to capital letters')
        actionLabelLetters.setToolTip('Change all labels to capital letters')
        actionLabelLetters.triggered.connect( lambda: self.onActionLabelAllVerticalTriggered(Settings.HeaderLabel.Letter) )

        actionLabelNumbers = QAction('Numbers', self)
        actionLabelNumbers.setStatusTip('Change all labels to decimal numbers')
        actionLabelNumbers.setToolTip('Change all labels to decimal numbers')
        actionLabelNumbers.triggered.connect( lambda: self.onActionLabelAllVerticalTriggered(Settings.HeaderLabel.Decimal) )

        # Menus
        menuLabel = QMenu('Label', self)
        menuLabel.setIcon(QIcon.fromTheme('tag', QIcon(':/icons/actions/16/tag.svg')))
        menuLabel.setStatusTip('Change label')
        menuLabel.setToolTip('Change label')
        menuLabel.addAction(actionLabelLetter)
        menuLabel.addAction(actionLabelNumber)
        menuLabel.addAction(actionLabelCustom)
        menuLabel.addSeparator()
        menuLabel.addAction(actionLabelLetters)
        menuLabel.addAction(actionLabelNumbers)

        contextMenu = QMenu(self)
        contextMenu.addMenu(menuLabel)
        contextMenu.exec_(self.mapToGlobal(pos))


    def onActionLabelVerticalTriggered(self, row, type):
        """
        Updates a specific vertical header item.
        """
        self.updateVerticalHeaderItem(row, type)


    def onActionLabelAllVerticalTriggered(self, type):
        """
        Updates all vertical header items.
        """
        for row in range(0, self.rowCount()):
            self.updateVerticalHeaderItem(row, type)


    def updateVerticalHeaderItem(self, row, type):
        """
        Updates a vertical header item.
        """
        number = row

        item = self.verticalHeaderItem(row)

        if type == Settings.HeaderLabel.Custom:

            text, ok = QInputDialog().getText(self, "Vertical Header Item",
                                              "Label:", QLineEdit.Normal, item.text(),
                                              self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

            if ok and text:
                item.setText(text)
        else:
            item.setText(self.headerItemText(number, type))
