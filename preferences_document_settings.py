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
from PySide2.QtWidgets import (QButtonGroup, QFormLayout, QGroupBox, QHBoxLayout, QLabel,
                               QRadioButton, QSpinBox, QTabWidget, QVBoxLayout, QWidget)

from settings import Settings


class PreferencesDocumentWidget(QWidget):

    settingChanged = Signal()


    def __init__(self, parent=None):
        """
        Initializes the PreferencesDocumentWidget class.
        """
        super(PreferencesDocumentWidget, self).__init__(parent)

        label = QLabel('<strong style="font-size:large;">Document</strong>')

        # Tab box
        tabBox = QTabWidget()
        tabBox.addTab(self.tabDefaultSettings(), 'Default')

        # Main layout
        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(tabBox)

        self.setLayout(layout)


    def tabDefaultSettings(self):
        """
        Creates the default settings tab page.
        """

        # Default: Headers
        rdbDefaultHeaderLabelHorizontalLetters = QRadioButton('Letters')
        rdbDefaultHeaderLabelHorizontalLetters.setToolTip('Capital letters as default horizontal header labels')

        rdbDefaultHeaderLabelHorizontalNumbers = QRadioButton('Numbers')
        rdbDefaultHeaderLabelHorizontalNumbers.setToolTip('Decimal numbers as default horizontal header labels')

        self.grpDefaultHeaderLabelHorizontal = QButtonGroup(self)
        self.grpDefaultHeaderLabelHorizontal.addButton(rdbDefaultHeaderLabelHorizontalLetters, Settings.HeaderLabel.Letter.value)
        self.grpDefaultHeaderLabelHorizontal.addButton(rdbDefaultHeaderLabelHorizontalNumbers, Settings.HeaderLabel.Decimal.value)
        self.grpDefaultHeaderLabelHorizontal.buttonClicked.connect(self.onSettingChanged)

        defaultHeaderLabelHorizontalBox = QHBoxLayout()
        defaultHeaderLabelHorizontalBox.addWidget(rdbDefaultHeaderLabelHorizontalLetters)
        defaultHeaderLabelHorizontalBox.addWidget(rdbDefaultHeaderLabelHorizontalNumbers)

        rdbDefaultHeaderLabelVerticalLetters = QRadioButton('Letters')
        rdbDefaultHeaderLabelVerticalLetters.setToolTip('Capital letters as default vertical header labels')

        rdbDefaultHeaderLabelVerticalNumbers = QRadioButton('Numbers')
        rdbDefaultHeaderLabelVerticalNumbers.setToolTip('Decimal numbers as default vertical header labels')

        self.grpDefaultHeaderLabelVertical = QButtonGroup(self)
        self.grpDefaultHeaderLabelVertical.addButton(rdbDefaultHeaderLabelVerticalLetters, Settings.HeaderLabel.Letter.value)
        self.grpDefaultHeaderLabelVertical.addButton(rdbDefaultHeaderLabelVerticalNumbers, Settings.HeaderLabel.Decimal.value)
        self.grpDefaultHeaderLabelVertical.buttonClicked.connect(self.onSettingChanged)

        defaultHeaderLabelVerticalBox = QHBoxLayout()
        defaultHeaderLabelVerticalBox.addWidget(rdbDefaultHeaderLabelVerticalLetters)
        defaultHeaderLabelVerticalBox.addWidget(rdbDefaultHeaderLabelVerticalNumbers)

        defaultHeadersLayout = QFormLayout()
        defaultHeadersLayout.addRow('Labels of horizontal header', defaultHeaderLabelHorizontalBox)
        defaultHeadersLayout.addRow('Labels of vertical header', defaultHeaderLabelVerticalBox)

        defaultHeadersGroup = QGroupBox('Headers')
        defaultHeadersGroup.setLayout(defaultHeadersLayout)

        # Default: Cells
        self.spbDefaultCellColumns = QSpinBox(self)
        self.spbDefaultCellColumns.setRange(1, 1000)
        self.spbDefaultCellColumns.setToolTip('Default number of columns of new documents')
        self.spbDefaultCellColumns.valueChanged.connect(self.onSettingChanged)

        self.spbDefaultCellRows = QSpinBox(self)
        self.spbDefaultCellRows.setRange(1, 1000)
        self.spbDefaultCellRows.setToolTip('Default number of rows of new documents')
        self.spbDefaultCellRows.valueChanged.connect(self.onSettingChanged)

        defaultCellsLayout = QFormLayout()
        defaultCellsLayout.addRow('Number of columns', self.spbDefaultCellColumns)
        defaultCellsLayout.addRow('Number of rows', self.spbDefaultCellRows)

        defaultCellsGroup = QGroupBox('Cells')
        defaultCellsGroup.setLayout(defaultCellsLayout)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(defaultHeadersGroup)
        layout.addWidget(defaultCellsGroup)
        layout.addStretch()

        widget = QWidget()
        widget.setLayout(layout)

        return widget


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


    def defaultHeaderLabelHorizontal(self):
        """
        Returns the default type of the horizontal header labels of documents.
        """
        return Settings.HeaderLabel(self.grpDefaultHeaderLabelHorizontal.checkedId())


    def setDefaultHeaderLabelHorizontal(self, type):
        """
        Sets the default type of the horizontal header labels of documents.
        """
        if type.value != self.grpDefaultHeaderLabelHorizontal.checkedId():
            self.onSettingChanged()

        for button in self.grpDefaultHeaderLabelHorizontal.buttons():
            if self.grpDefaultHeaderLabelHorizontal.id(button) == type.value:
                button.setChecked(True)


    def defaultHeaderLabelVertical(self):
        """
        Returns the default type of the vertical header labels of documents.
        """
        return Settings.HeaderLabel(self.grpDefaultHeaderLabelVertical.checkedId())


    def setDefaultHeaderLabelVertical(self, type):
        """
        Sets the default type of the vertical header labels of documents.
        """
        if type.value != self.grpDefaultHeaderLabelVertical.checkedId():
            self.onSettingChanged()

        for button in self.grpDefaultHeaderLabelVertical.buttons():
            if self.grpDefaultHeaderLabelVertical.id(button) == type.value:
                button.setChecked(True)


    def defaultCellColumns(self):
        """
        Returns the default number of columns of new documents.
        """
        return self.spbDefaultCellColumns.value()


    def setDefaultCellColumns(self, number):
        """
        Sets the default number of columns of new documents.
        """
        self.spbDefaultCellColumns.setValue(number)


    def defaultCellRows(self):
        """
        Returns the default number of rows of new documents.
        """
        return self.spbDefaultCellRows.value()


    def setDefaultCellRows(self, number):
        """
        Sets the default number of rows of new documents.
        """
        self.spbDefaultCellRows.setValue(number)
