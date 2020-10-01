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
from PySide2.QtWidgets import (QButtonGroup, QFormLayout, QGroupBox, QHBoxLayout,
                               QLabel, QRadioButton, QSpinBox, QVBoxLayout, QWidget)


class PreferencesDocumentWidget(QWidget):

    settingChanged = Signal()


    def __init__(self, parent=None):
        """
        Initializes the PreferencesDocumentWidget class.
        """
        super(PreferencesDocumentWidget, self).__init__(parent)

        label = QLabel('<strong style="font-size:large;">Document</strong>')

        # Header Labels
        rdbHorizontalHeaderLabelsLetters = QRadioButton('Letters')
        rdbHorizontalHeaderLabelsLetters.setToolTip('Horizontal header labels as capital letters')

        rdbHorizontalHeaderLabelsNumbers = QRadioButton('Numbers')
        rdbHorizontalHeaderLabelsNumbers.setToolTip('Horizontal header labels as numbers')

        self.horizontalHeaderLabelsGroup = QButtonGroup(self)
        self.horizontalHeaderLabelsGroup.addButton(rdbHorizontalHeaderLabelsLetters, 0)
        self.horizontalHeaderLabelsGroup.addButton(rdbHorizontalHeaderLabelsNumbers, 1)
        self.horizontalHeaderLabelsGroup.buttonClicked.connect(self.onSettingChanged)

        horizontalHeaderLabelsBox = QHBoxLayout()
        horizontalHeaderLabelsBox.addWidget(rdbHorizontalHeaderLabelsLetters)
        horizontalHeaderLabelsBox.addWidget(rdbHorizontalHeaderLabelsNumbers)

        rdbVerticalHeaderLabelsLetters = QRadioButton('Letters')
        rdbVerticalHeaderLabelsLetters.setToolTip('Vertical header labels as capital letters')

        rdbVerticalHeaderLabelsNumbers = QRadioButton('Numbers')
        rdbVerticalHeaderLabelsNumbers.setToolTip('Vertical header labels as numbers')

        self.verticalHeaderLabelsGroup = QButtonGroup(self)
        self.verticalHeaderLabelsGroup.addButton(rdbVerticalHeaderLabelsLetters, 0)
        self.verticalHeaderLabelsGroup.addButton(rdbVerticalHeaderLabelsNumbers, 1)
        self.verticalHeaderLabelsGroup.buttonClicked.connect(self.onSettingChanged)

        verticalHeaderLabelsBox = QHBoxLayout()
        verticalHeaderLabelsBox.addWidget(rdbVerticalHeaderLabelsLetters)
        verticalHeaderLabelsBox.addWidget(rdbVerticalHeaderLabelsNumbers)

        headerLabelsLayout = QFormLayout()
        headerLabelsLayout.addRow('Horizontal header', horizontalHeaderLabelsBox)
        headerLabelsLayout.addRow('Vertical header', verticalHeaderLabelsBox)

        headerLabelsGroup = QGroupBox('Header Labels')
        headerLabelsGroup.setLayout(headerLabelsLayout)

        # New Document
        self.spbNewDocumentColumns = QSpinBox(self)
        self.spbNewDocumentColumns.setRange(1, 100)
        self.spbNewDocumentColumns.setToolTip('Number of columns of new documents')
        self.spbNewDocumentColumns.valueChanged.connect(self.onSettingChanged)

        self.spbNewDocumentRows = QSpinBox(self)
        self.spbNewDocumentRows.setRange(1, 100)
        self.spbNewDocumentRows.setToolTip('Number of rows of new documents')
        self.spbNewDocumentRows.valueChanged.connect(self.onSettingChanged)

        newDocumentLayout = QFormLayout()
        newDocumentLayout.addRow('Number of columns', self.spbNewDocumentColumns)
        newDocumentLayout.addRow('Number of rows', self.spbNewDocumentRows)

        newDocumentGroup = QGroupBox('New Document')
        newDocumentGroup.setLayout(newDocumentLayout)

        # Main layout
        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(headerLabelsGroup)
        layout.addWidget(newDocumentGroup)
        layout.addStretch()

        self.setLayout(layout)


    def onSettingChanged(self):
        """
        Emits signal that a setting has been changed.
        """
        self.settingChanged.emit()


    def title(self):
        """
        Returns title of the widget.
        """
        return 'Document'


    def horizontalHeaderLabels(self):
        """
        Returns type of the horizontal header labels.
        """
        return self.horizontalHeaderLabelsGroup.checkedId()


    def setHorizontalHeaderLabels(self, id):
        """
        Sets type of the horizontal header labels.
        """
        if id != self.horizontalHeaderLabelsGroup.checkedId():
            self.onSettingChanged()

        for button in self.horizontalHeaderLabelsGroup.buttons():
            if self.horizontalHeaderLabelsGroup.id(button) == id:
                button.setChecked(True)


    def verticalHeaderLabels(self):
        """
        Returns type of the vertical header labels.
        """
        return self.verticalHeaderLabelsGroup.checkedId()


    def setVerticalHeaderLabels(self, id):
        """
        Sets type of the vertical header labels.
        """
        if id != self.verticalHeaderLabelsGroup.checkedId():
            self.onSettingChanged()

        for button in self.verticalHeaderLabelsGroup.buttons():
            if self.verticalHeaderLabelsGroup.id(button) == id:
                button.setChecked(True)


    def newDocumentColumns(self):
        """
        Returns number of columns of new document.
        """
        return self.spbNewDocumentColumns.value()


    def setNewDocumentColumns(self, number):
        """
        Sets number of columns of new document.
        """
        self.spbNewDocumentColumns.setValue(number)


    def newDocumentRows(self):
        """
        Returns number of rows of new document.
        """
        return self.spbNewDocumentRows.value()


    def setNewDocumentRows(self, number):
        """
        Sets number of rows of new document.
        """
        self.spbNewDocumentRows.setValue(number)