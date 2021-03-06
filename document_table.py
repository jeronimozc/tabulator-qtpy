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

from PySide2.QtCore import QFileInfo, Qt
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QAction, QDialog, QMenu, QTableWidget, QTableWidgetItem

from document_table_header_dialog import DocumentTableHeaderDialog
from preferences import Preferences


class DocumentTable(QTableWidget):

    _preferences = Preferences()
    sequenceNumber = 0


    def __init__(self, parent=None):
        super(DocumentTable, self).__init__(parent)

        self.setAttribute(Qt.WA_DeleteOnClose)

        self.m_url = ""
        self.isUntitled = True

        # Creates a default document
        self.setColumnCount(self._preferences.defaultCellCountColumn())
        self.setRowCount(self._preferences.defaultCellCountRow())

        # Enable context menus
        hHeaderView = self.horizontalHeader()
        hHeaderView.setContextMenuPolicy(Qt.CustomContextMenu)
        hHeaderView.customContextMenuRequested.connect(self.contextMenuHorizontalHeader)

        vHeaderView = self.verticalHeader()
        vHeaderView.setContextMenuPolicy(Qt.CustomContextMenu)
        vHeaderView.customContextMenuRequested.connect(self.contextMenuVerticalHeader)


    def setPreferences(self, preferences):
        """
        Sets the user preferences.
        """
        self._preferences = preferences


    def newDocument(self):
        """
        Creates a new document.
        """
        DocumentTable.sequenceNumber += 1

        self.m_url = 'Untitled'
        if DocumentTable.sequenceNumber > 1:
            self.m_url += f' ({DocumentTable.sequenceNumber})'
        self.isUntitled = True

        self.setColumnCount(self._preferences.defaultCellCountColumn())
        self.setRowCount(self._preferences.defaultCellCountRow())

        # Set header items
        self.setHorizontalHeaderItems(self._preferences.defaultHeaderLabelHorizontal())
        self.setVerticalHeaderItems(self._preferences.defaultHeaderLabelVertical())

        self.setWindowTitle(self.documentName())


    def loadDocument(self, url):
        """
        Loads an existing document.
        """
        self.m_url = url
        self.isUntitled = False

        # Set header items
        self.setHorizontalHeaderItems(self._preferences.defaultHeaderLabelHorizontal())
        self.setVerticalHeaderItems(self._preferences.defaultHeaderLabelVertical())

        self.setWindowTitle(self.documentName())

        return True


    def documentPath(self):
        """
        Returns the canonical path of the document.
        """
        return QFileInfo(self.m_url).canonicalFilePath()


    def documentName(self):
        """
        Returns the name of the document.
        """
        return QFileInfo(self.m_url).fileName()


    def setHorizontalHeaderItems(self, type):
        """
        Sets the horizontal header items.
        """
        parameter = self.headerItemDefaultParameter(type)

        for column in range(0, self.columnCount()):

            number = column

            item = QTableWidgetItem()
            item.setTextAlignment(Qt.AlignCenter)
            item.setText(self.headerItemText(number, type, parameter))

            self.setHorizontalHeaderItem(column, item)


    def setVerticalHeaderItems(self, type):
        """
        Sets the vertical header items.
        """
        parameter = self.headerItemDefaultParameter(type)

        for row in range(0, self.rowCount()):

            number = row

            item = QTableWidgetItem()
            item.setTextAlignment(Qt.AlignCenter)
            item.setText(self.headerItemText(number, type, parameter))

            self.setVerticalHeaderItem(row, item)


    def headerItemText(self, number, type, parameter):
        """
        Returns the header item text.
        """
        if type == Preferences.HeaderLabel.Custom:
            return self.numberToCustom(number, parameter)
        elif type == Preferences.HeaderLabel.Binary:
            return self.numberToBinary(number, parameter)
        elif type == Preferences.HeaderLabel.Octal:
            return self.numberToOctal(number, parameter)
        elif type == Preferences.HeaderLabel.Decimal:
            return self.numberToDecimal(number, parameter)
        elif type == Preferences.HeaderLabel.Hexadecimal:
            return self.numberToHexadecimal(number, parameter)
        elif type == Preferences.HeaderLabel.Letter:
            return self.numberToLetter(number, parameter)
        else:
            return ''


    def headerItemDefaultParameter(self, type):
        """
        Returns a default parameter that matches the type of the header label.
        """
        if type == Preferences.HeaderLabel.Binary:
            return '0b'
        elif type == Preferences.HeaderLabel.Octal:
            return '0o'
        elif type == Preferences.HeaderLabel.Decimal:
            return '1'
        elif type == Preferences.HeaderLabel.Hexadecimal:
            return '0x'
        elif type == Preferences.HeaderLabel.Letter:
            return 'upper'
        else:
            return ''


    def numberToCustom(self, number, parameter):
        """
        Returns a string equivalent of the user-defined text.
        """
        return parameter.replace('#', str(number + 1))


    def numberToBinary(self, number, parameter):
        """
        Returns a string equivalent of the number according to the base 2.
        """
        return f'{parameter}{number:b}'


    def numberToOctal(self, number, parameter):
        """
        Returns a string equivalent of the number according to the base 8.
        """
        return f'{parameter}{number:o}'


    def numberToDecimal(self, number, parameter):
        """
        Returns a string equivalent of the number according to the base 10.
        """
        return f'{number + int(parameter)}'


    def numberToHexadecimal(self, number, parameter):
        """
        Returns a string equivalent of the number according to the base 16.
        """
        return f'{parameter}{number:X}'


    def numberToLetter(self, number, parameter):
        """
        Returns a string equivalent of the number according to the base 26.
        """
        chars = ''
        number += 1

        while number > 0:
            number -= 1
            chars = chr(number % 26 + 65) + chars
            number //= 26

        return chars.upper() if parameter == 'upper' else chars.lower()


    def contextMenuHorizontalHeader(self, pos):
        """
        Creates a context menu for the horizontal header.
        """
        index = self.indexAt(pos)

        # Label
        actionLabelLetter = QAction('Letter', self)
        actionLabelLetter.setStatusTip('Change label to a capital letter')
        actionLabelLetter.setToolTip('Change label to a capital letter')
        actionLabelLetter.triggered.connect( lambda: self.onActionLabelHorizontalTriggered(index.column(), Preferences.HeaderLabel.Letter) )

        actionLabelNumber = QAction('Number', self)
        actionLabelNumber.setStatusTip('Change label to a decimal number')
        actionLabelNumber.setToolTip('Change label to a decimal number')
        actionLabelNumber.triggered.connect( lambda: self.onActionLabelHorizontalTriggered(index.column(), Preferences.HeaderLabel.Decimal) )

        actionLabelCustom = QAction('Custom???', self)
        actionLabelCustom.setStatusTip('Change label to a user-defined text')
        actionLabelCustom.setToolTip('Change label to a user-defined text')
        actionLabelCustom.triggered.connect( lambda: self.onActionLabelHorizontalTriggered(index.column(), Preferences.HeaderLabel.Custom) )

        actionLabelLetters = QAction('Letters', self)
        actionLabelLetters.setStatusTip('Change all labels to capital letters')
        actionLabelLetters.setToolTip('Change all labels to capital letters')
        actionLabelLetters.triggered.connect( lambda: self.onActionLabelAllHorizontalTriggered(Preferences.HeaderLabel.Letter) )

        actionLabelNumbers = QAction('Numbers', self)
        actionLabelNumbers.setStatusTip('Change all labels to decimal numbers')
        actionLabelNumbers.setToolTip('Change all labels to decimal numbers')
        actionLabelNumbers.triggered.connect( lambda: self.onActionLabelAllHorizontalTriggered(Preferences.HeaderLabel.Decimal) )

        actionLabelCustoms = QAction('Custom???', self)
        actionLabelCustoms.setStatusTip('Change all labels to user-defined texts')
        actionLabelCustoms.setToolTip('Change all labels to user-defined texts')
        actionLabelCustoms.triggered.connect( lambda: self.onActionLabelAllHorizontalTriggered(Preferences.HeaderLabel.Custom) )

        # Context menu
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
        menuLabel.addAction(actionLabelCustoms)

        contextMenu = QMenu(self)
        contextMenu.addMenu(menuLabel)
        contextMenu.exec_(self.mapToGlobal(pos))


    def onActionLabelHorizontalTriggered(self, column, type):
        """
        Updates a specific horizontal header item.
        """
        parameter = self.headerItemDefaultParameter(type)

        if type == Preferences.HeaderLabel.Custom:

            documentTableHeaderDialog = DocumentTableHeaderDialog('horizontal', column, self)
            documentTableHeaderDialog.setWindowTitle(f'Horizontal Header Item')

            if documentTableHeaderDialog.exec_() == QDialog.Accepted:
                type = documentTableHeaderDialog.headerLabelType()
                parameter = documentTableHeaderDialog.headerLabelParameter()
            else:
                return

        self.updateHorizontalHeaderItem(column, type, parameter)


    def onActionLabelAllHorizontalTriggered(self, type):
        """
        Updates all horizontal header items.
        """
        parameter = self.headerItemDefaultParameter(type)

        if type == Preferences.HeaderLabel.Custom:

            documentTableHeaderDialog = DocumentTableHeaderDialog('horizontal', -1, self)
            documentTableHeaderDialog.setWindowTitle(f'Horizontal Header Items')

            if documentTableHeaderDialog.exec_() == QDialog.Accepted:
                type = documentTableHeaderDialog.headerLabelType()
                parameter = documentTableHeaderDialog.headerLabelParameter()
            else:
                return

        for column in range(0, self.columnCount()):
            self.updateHorizontalHeaderItem(column, type, parameter)


    def updateHorizontalHeaderItem(self, column, type, parameter):
        """
        Updates a horizontal header item.
        """
        number = column

        item = self.horizontalHeaderItem(column)
        item.setText(self.headerItemText(number, type, parameter))


    def contextMenuVerticalHeader(self, pos):
        """
        Creates a context menu for the vertical header.
        """
        index = self.indexAt(pos)

        # Label
        actionLabelLetter = QAction('Letter', self)
        actionLabelLetter.setStatusTip('Change label to a capital letter')
        actionLabelLetter.setToolTip('Change label to a capital letter')
        actionLabelLetter.triggered.connect( lambda: self.onActionLabelVerticalTriggered(index.row(), Preferences.HeaderLabel.Letter) )

        actionLabelNumber = QAction('Number', self)
        actionLabelNumber.setStatusTip('Change label to a decimal number')
        actionLabelNumber.setToolTip('Change label to a decimal number')
        actionLabelNumber.triggered.connect( lambda: self.onActionLabelVerticalTriggered(index.row(), Preferences.HeaderLabel.Decimal) )

        actionLabelCustom = QAction('Custom???', self)
        actionLabelCustom.setStatusTip('Change label to a user-defined text')
        actionLabelCustom.setToolTip('Change label to a user-defined text')
        actionLabelCustom.triggered.connect( lambda: self.onActionLabelVerticalTriggered(index.row(), Preferences.HeaderLabel.Custom) )

        actionLabelLetters = QAction('Letters', self)
        actionLabelLetters.setStatusTip('Change all labels to capital letters')
        actionLabelLetters.setToolTip('Change all labels to capital letters')
        actionLabelLetters.triggered.connect( lambda: self.onActionLabelAllVerticalTriggered(Preferences.HeaderLabel.Letter) )

        actionLabelNumbers = QAction('Numbers', self)
        actionLabelNumbers.setStatusTip('Change all labels to decimal numbers')
        actionLabelNumbers.setToolTip('Change all labels to decimal numbers')
        actionLabelNumbers.triggered.connect( lambda: self.onActionLabelAllVerticalTriggered(Preferences.HeaderLabel.Decimal) )

        actionLabelCustoms = QAction('Custom???', self)
        actionLabelCustoms.setStatusTip('Change all labels to user-defined texts')
        actionLabelCustoms.setToolTip('Change all labels to user-defined texts')
        actionLabelCustoms.triggered.connect( lambda: self.onActionLabelAllVerticalTriggered(Preferences.HeaderLabel.Custom) )

        # Context menu
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
        menuLabel.addAction(actionLabelCustoms)

        contextMenu = QMenu(self)
        contextMenu.addMenu(menuLabel)
        contextMenu.exec_(self.mapToGlobal(pos))


    def onActionLabelVerticalTriggered(self, row, type):
        """
        Updates a specific vertical header item.
        """
        parameter = self.headerItemDefaultParameter(type)

        if type == Preferences.HeaderLabel.Custom:

            documentTableHeaderDialog = DocumentTableHeaderDialog('vertical', row, self)
            documentTableHeaderDialog.setWindowTitle(f'Vertical Header Item')

            if documentTableHeaderDialog.exec_() == QDialog.Accepted:
                type = documentTableHeaderDialog.headerLabelType()
                parameter = documentTableHeaderDialog.headerLabelParameter()
            else:
                return

        self.updateVerticalHeaderItem(row, type, parameter)


    def onActionLabelAllVerticalTriggered(self, type):
        """
        Updates all vertical header items.
        """
        parameter = self.headerItemDefaultParameter(type)

        if type == Preferences.HeaderLabel.Custom:

            documentTableHeaderDialog = DocumentTableHeaderDialog('vertical', -1, self)
            documentTableHeaderDialog.setWindowTitle(f'Vertical Header Items')

            if documentTableHeaderDialog.exec_() == QDialog.Accepted:
                type = documentTableHeaderDialog.headerLabelType()
                parameter = documentTableHeaderDialog.headerLabelParameter()
            else:
                return

        for row in range(0, self.rowCount()):
            self.updateVerticalHeaderItem(row, type, parameter)


    def updateVerticalHeaderItem(self, row, type, parameter):
        """
        Updates a vertical header item.
        """
        number = row

        item = self.verticalHeaderItem(row)
        item.setText(self.headerItemText(number, type, parameter))
