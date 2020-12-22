# This Python file uses the following encoding: utf-8
#
# Copyright 2020 NotNypical, <https://notnypical.github.io>.
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
                               QRadioButton, QSpinBox, QTabWidget, QVBoxLayout, QWidget)

from settings import Settings


class PreferencesDocumentSettings(QWidget):

    settingsChanged = Signal()


    def __init__(self, parent=None):
        super().__init__(parent)

        # Title
        title = QLabel(self.tr('<strong style="font-size:large;">Document Settings</strong>'))

        # Tab box
        tabBox = QTabWidget()
        tabBox.addTab(self.tabDefaultSettings(), self.tr('Default'))

        # Main layout
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(title)
        self.layout.addWidget(tabBox)


    def tabDefaultSettings(self):

        # Default: Headers
        rdbDefaultHeaderLabelHorizontalLetters = QRadioButton(self.tr('Letters'))
        rdbDefaultHeaderLabelHorizontalLetters.setToolTip(self.tr('Capital letters as default horizontal header labels'))

        rdbDefaultHeaderLabelHorizontalNumbers = QRadioButton(self.tr('Numbers'))
        rdbDefaultHeaderLabelHorizontalNumbers.setToolTip(self.tr('Decimal numbers as default horizontal header labels'))

        self.grpDefaultHeaderLabelHorizontal = QButtonGroup(self)
        self.grpDefaultHeaderLabelHorizontal.addButton(rdbDefaultHeaderLabelHorizontalLetters, Settings.HeaderLabel.Letter.value)
        self.grpDefaultHeaderLabelHorizontal.addButton(rdbDefaultHeaderLabelHorizontalNumbers, Settings.HeaderLabel.Decimal.value)
        self.grpDefaultHeaderLabelHorizontal.buttonClicked.connect(self.onSettingsChanged)

        defaultHeaderLabelHorizontalBox = QHBoxLayout()
        defaultHeaderLabelHorizontalBox.addWidget(rdbDefaultHeaderLabelHorizontalLetters)
        defaultHeaderLabelHorizontalBox.addWidget(rdbDefaultHeaderLabelHorizontalNumbers)

        rdbDefaultHeaderLabelVerticalLetters = QRadioButton(self.tr('Letters'))
        rdbDefaultHeaderLabelVerticalLetters.setToolTip(self.tr('Capital letters as default vertical header labels'))

        rdbDefaultHeaderLabelVerticalNumbers = QRadioButton(self.tr('Numbers'))
        rdbDefaultHeaderLabelVerticalNumbers.setToolTip(self.tr('Decimal numbers as default vertical header labels'))

        self.grpDefaultHeaderLabelVertical = QButtonGroup(self)
        self.grpDefaultHeaderLabelVertical.addButton(rdbDefaultHeaderLabelVerticalLetters, Settings.HeaderLabel.Letter.value)
        self.grpDefaultHeaderLabelVertical.addButton(rdbDefaultHeaderLabelVerticalNumbers, Settings.HeaderLabel.Decimal.value)
        self.grpDefaultHeaderLabelVertical.buttonClicked.connect(self.onSettingsChanged)

        defaultHeaderLabelVerticalBox = QHBoxLayout()
        defaultHeaderLabelVerticalBox.addWidget(rdbDefaultHeaderLabelVerticalLetters)
        defaultHeaderLabelVerticalBox.addWidget(rdbDefaultHeaderLabelVerticalNumbers)

        defaultHeadersLayout = QFormLayout()
        defaultHeadersLayout.addRow(self.tr('Labels of horizontal header'), defaultHeaderLabelHorizontalBox)
        defaultHeadersLayout.addRow(self.tr('Labels of vertical header'), defaultHeaderLabelVerticalBox)

        defaultHeadersGroup = QGroupBox(self.tr('Headers'))
        defaultHeadersGroup.setLayout(defaultHeadersLayout)

        # Default: Cells
        self.spbDefaultCellColumns = QSpinBox(self)
        self.spbDefaultCellColumns.setRange(1, 1000)
        self.spbDefaultCellColumns.setToolTip(self.tr('Default number of columns of new documents'))
        self.spbDefaultCellColumns.valueChanged.connect(self.onSettingsChanged)

        self.spbDefaultCellRows = QSpinBox(self)
        self.spbDefaultCellRows.setRange(1, 1000)
        self.spbDefaultCellRows.setToolTip(self.tr('Default number of rows of new documents'))
        self.spbDefaultCellRows.valueChanged.connect(self.onSettingsChanged)

        defaultCellsLayout = QFormLayout()
        defaultCellsLayout.addRow(self.tr('Number of columns'), self.spbDefaultCellColumns)
        defaultCellsLayout.addRow(self.tr('Number of rows'), self.spbDefaultCellRows)

        defaultCellsGroup = QGroupBox(self.tr('Cells'))
        defaultCellsGroup.setLayout(defaultCellsLayout)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(defaultHeadersGroup)
        layout.addWidget(defaultCellsGroup)
        layout.addStretch()

        widget = QWidget()
        widget.setLayout(layout)

        return widget


    def title(self):

        return self.tr('Document')


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


    def setDefaultCellColumns(self, number):

        self.spbDefaultCellColumns.setValue(number)


    def defaultCellColumns(self):

        return self.spbDefaultCellColumns.value()


    def setDefaultCellRows(self, number):

        self.spbDefaultCellRows.setValue(number)


    def defaultCellRows(self):

        return self.spbDefaultCellRows.value()
