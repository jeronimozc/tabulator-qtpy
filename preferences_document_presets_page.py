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
from PySide2.QtWidgets import (QButtonGroup, QFormLayout, QGroupBox, QHBoxLayout, QLabel,
                               QRadioButton, QSpinBox, QVBoxLayout, QWidget)

from settings import Settings


class PreferencesDocumentPresetsPage(QWidget):

    settingsChanged = Signal()


    def __init__(self, parent=None):
        super().__init__(parent)

        # Title
        title = QLabel(self.tr('<strong style="font-size:large;">Document Presets</strong>'))

        # Header Labels
        rdbDefaultHeaderLabelHorizontalLetters = QRadioButton(self.tr('Letters'))
        rdbDefaultHeaderLabelHorizontalLetters.setToolTip(self.tr('Capital letters as default horizontal header labels of new documents'))

        rdbDefaultHeaderLabelHorizontalNumbers = QRadioButton(self.tr('Numbers'))
        rdbDefaultHeaderLabelHorizontalNumbers.setToolTip(self.tr('Decimal numbers as default horizontal header labels of new documents'))

        self.grpDefaultHeaderLabelHorizontal = QButtonGroup(self)
        self.grpDefaultHeaderLabelHorizontal.addButton(rdbDefaultHeaderLabelHorizontalLetters, Settings.HeaderLabel.Letter.value)
        self.grpDefaultHeaderLabelHorizontal.addButton(rdbDefaultHeaderLabelHorizontalNumbers, Settings.HeaderLabel.Decimal.value)
        self.grpDefaultHeaderLabelHorizontal.buttonClicked.connect(self.onSettingsChanged)

        defaultHeaderLabelHorizontalBox = QHBoxLayout()
        defaultHeaderLabelHorizontalBox.addWidget(rdbDefaultHeaderLabelHorizontalLetters)
        defaultHeaderLabelHorizontalBox.addWidget(rdbDefaultHeaderLabelHorizontalNumbers)

        rdbDefaultHeaderLabelVerticalLetters = QRadioButton(self.tr('Letters'))
        rdbDefaultHeaderLabelVerticalLetters.setToolTip(self.tr('Capital letters as default vertical header labels of new documents'))

        rdbDefaultHeaderLabelVerticalNumbers = QRadioButton(self.tr('Numbers'))
        rdbDefaultHeaderLabelVerticalNumbers.setToolTip(self.tr('Decimal numbers as default vertical header labels of new documents'))

        self.grpDefaultHeaderLabelVertical = QButtonGroup(self)
        self.grpDefaultHeaderLabelVertical.addButton(rdbDefaultHeaderLabelVerticalLetters, Settings.HeaderLabel.Letter.value)
        self.grpDefaultHeaderLabelVertical.addButton(rdbDefaultHeaderLabelVerticalNumbers, Settings.HeaderLabel.Decimal.value)
        self.grpDefaultHeaderLabelVertical.buttonClicked.connect(self.onSettingsChanged)

        defaultHeaderLabelVerticalBox = QHBoxLayout()
        defaultHeaderLabelVerticalBox.addWidget(rdbDefaultHeaderLabelVerticalLetters)
        defaultHeaderLabelVerticalBox.addWidget(rdbDefaultHeaderLabelVerticalNumbers)

        defaultHeaderLabelLayout = QFormLayout()
        defaultHeaderLabelLayout.addRow(self.tr('Labels of the horizontal header'), defaultHeaderLabelHorizontalBox)
        defaultHeaderLabelLayout.addRow(self.tr('Labels of the vertical header'), defaultHeaderLabelVerticalBox)

        defaultHeaderLabelGroup = QGroupBox(self.tr('Header Labels'))
        defaultHeaderLabelGroup.setLayout(defaultHeaderLabelLayout)

        # Cell Counts
        self.spbDefaultCellCountColumn = QSpinBox(self)
        self.spbDefaultCellCountColumn.setRange(1, 1000)
        self.spbDefaultCellCountColumn.setToolTip(self.tr('Default number of columns of new documents'))
        self.spbDefaultCellCountColumn.valueChanged.connect(self.onSettingsChanged)

        self.spbDefaultCellCountRow = QSpinBox(self)
        self.spbDefaultCellCountRow.setRange(1, 1000)
        self.spbDefaultCellCountRow.setToolTip(self.tr('Default number of rows of new documents'))
        self.spbDefaultCellCountRow.valueChanged.connect(self.onSettingsChanged)

        defaultCellCountLayout = QFormLayout()
        defaultCellCountLayout.addRow(self.tr('Number of columns'), self.spbDefaultCellCountColumn)
        defaultCellCountLayout.addRow(self.tr('Number of rows'), self.spbDefaultCellCountRow)

        defaultCellCountGroup = QGroupBox(self.tr('Cell Counts'))
        defaultCellCountGroup.setLayout(defaultCellCountLayout)

        # Main layout
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(title)
        self.layout.addWidget(defaultHeaderLabelGroup)
        self.layout.addWidget(defaultCellCountGroup)
        self.layout.addStretch()


    def title(self):

        return self.tr('Document Presets')


    def setZeroMargins(self):

        self.layout.setContentsMargins(0, 0, 0, 0)


    def onSettingsChanged(self):

        self.settingsChanged.emit()


    def setDefaultHeaderLabelHorizontal(self, type):

        if type.value != self.grpDefaultHeaderLabelHorizontal.checkedId():
            self.onSettingsChanged()

        for button in self.grpDefaultHeaderLabelHorizontal.buttons():
            if self.grpDefaultHeaderLabelHorizontal.id(button) == type.value:
                button.setChecked(True)


    def defaultHeaderLabelHorizontal(self):

        return Settings.HeaderLabel(self.grpDefaultHeaderLabelHorizontal.checkedId())


    def setDefaultHeaderLabelVertical(self, type):

        if type.value != self.grpDefaultHeaderLabelVertical.checkedId():
            self.onSettingsChanged()

        for button in self.grpDefaultHeaderLabelVertical.buttons():
            if self.grpDefaultHeaderLabelVertical.id(button) == type.value:
                button.setChecked(True)


    def defaultHeaderLabelVertical(self):

        return Settings.HeaderLabel(self.grpDefaultHeaderLabelVertical.checkedId())


    def setDefaultCellCountColumn(self, val):

        self.spbDefaultCellCountColumn.setValue(val)


    def defaultCellCountColumn(self):

        return self.spbDefaultCellCountColumn.value()


    def setDefaultCellCountRow(self, val):

        self.spbDefaultCellCountRow.setValue(val)


    def defaultCellCountRow(self):

        return self.spbDefaultCellCountRow.value()
