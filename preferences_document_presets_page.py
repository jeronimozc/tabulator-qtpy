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

from PySide2.QtCore import Signal
from PySide2.QtWidgets import (QButtonGroup, QFormLayout, QGroupBox, QHBoxLayout, QLabel,
                               QRadioButton, QSpinBox, QVBoxLayout, QWidget)

from preferences import Preferences


class PreferencesDocumentPresetsPage(QWidget):

    preferencesChanged = Signal()


    def __init__(self, parent=None):
        super().__init__(parent)

        # Title
        title = QLabel(self.tr('<strong style="font-size:large;">Document Presets</strong>'))

        # Content: Header Labels

        rdbDefaultHeaderLabelHorizontalLetters = QRadioButton(self.tr('Letters'))
        rdbDefaultHeaderLabelHorizontalLetters.setToolTip(self.tr('Capital letters as default horizontal header labels of new documents'))

        rdbDefaultHeaderLabelHorizontalNumbers = QRadioButton(self.tr('Numbers'))
        rdbDefaultHeaderLabelHorizontalNumbers.setToolTip(self.tr('Decimal numbers as default horizontal header labels of new documents'))

        self._grpDefaultHeaderLabelHorizontal = QButtonGroup(self)
        self._grpDefaultHeaderLabelHorizontal.addButton(rdbDefaultHeaderLabelHorizontalLetters, Preferences.HeaderLabel.Letter.value)
        self._grpDefaultHeaderLabelHorizontal.addButton(rdbDefaultHeaderLabelHorizontalNumbers, Preferences.HeaderLabel.Decimal.value)
        self._grpDefaultHeaderLabelHorizontal.buttonClicked.connect(self._onPreferencesChanged)

        defaultHeaderLabelHorizontalBox = QHBoxLayout()
        defaultHeaderLabelHorizontalBox.addWidget(rdbDefaultHeaderLabelHorizontalLetters)
        defaultHeaderLabelHorizontalBox.addWidget(rdbDefaultHeaderLabelHorizontalNumbers)

        rdbDefaultHeaderLabelVerticalLetters = QRadioButton(self.tr('Letters'))
        rdbDefaultHeaderLabelVerticalLetters.setToolTip(self.tr('Capital letters as default vertical header labels of new documents'))

        rdbDefaultHeaderLabelVerticalNumbers = QRadioButton(self.tr('Numbers'))
        rdbDefaultHeaderLabelVerticalNumbers.setToolTip(self.tr('Decimal numbers as default vertical header labels of new documents'))

        self._grpDefaultHeaderLabelVertical = QButtonGroup()
        self._grpDefaultHeaderLabelVertical.addButton(rdbDefaultHeaderLabelVerticalLetters, Preferences.HeaderLabel.Letter.value)
        self._grpDefaultHeaderLabelVertical.addButton(rdbDefaultHeaderLabelVerticalNumbers, Preferences.HeaderLabel.Decimal.value)
        self._grpDefaultHeaderLabelVertical.buttonClicked.connect(self._onPreferencesChanged)

        defaultHeaderLabelVerticalBox = QHBoxLayout()
        defaultHeaderLabelVerticalBox.addWidget(rdbDefaultHeaderLabelVerticalLetters)
        defaultHeaderLabelVerticalBox.addWidget(rdbDefaultHeaderLabelVerticalNumbers)

        defaultHeaderLabelLayout = QFormLayout()
        defaultHeaderLabelLayout.addRow(self.tr('Labels of the horizontal header'), defaultHeaderLabelHorizontalBox)
        defaultHeaderLabelLayout.addRow(self.tr('Labels of the vertical header'), defaultHeaderLabelVerticalBox)

        defaultHeaderLabelGroup = QGroupBox(self.tr('Header Labels'))
        defaultHeaderLabelGroup.setLayout(defaultHeaderLabelLayout)

        # Content: Cell Counts

        self._spbDefaultCellCountColumn = QSpinBox()
        self._spbDefaultCellCountColumn.setRange(1, 1000)
        self._spbDefaultCellCountColumn.setToolTip(self.tr('Default number of columns of new documents'))
        self._spbDefaultCellCountColumn.valueChanged.connect(self._onPreferencesChanged)

        self._spbDefaultCellCountRow = QSpinBox()
        self._spbDefaultCellCountRow.setRange(1, 1000)
        self._spbDefaultCellCountRow.setToolTip(self.tr('Default number of rows of new documents'))
        self._spbDefaultCellCountRow.valueChanged.connect(self._onPreferencesChanged)

        defaultCellCountLayout = QFormLayout()
        defaultCellCountLayout.addRow(self.tr('Number of columns'), self._spbDefaultCellCountColumn)
        defaultCellCountLayout.addRow(self.tr('Number of rows'), self._spbDefaultCellCountRow)

        defaultCellCountGroup = QGroupBox(self.tr('Cell Counts'))
        defaultCellCountGroup.setLayout(defaultCellCountLayout)

        # Main layout
        self._layout = QVBoxLayout(self)
        self._layout.addWidget(title)
        self._layout.addWidget(defaultHeaderLabelGroup)
        self._layout.addWidget(defaultCellCountGroup)
        self._layout.addStretch(1)


    def setZeroMargins(self):

        self._layout.setContentsMargins(0, 0, 0, 0)


    def title(self):

        return self.tr('Document Presets')


    def _onPreferencesChanged(self):

        self.preferencesChanged.emit()


    def setDefaultHeaderLabelHorizontal(self, type):

        if type.value != self._grpDefaultHeaderLabelHorizontal.checkedId():
            self._onPreferencesChanged()

        for button in self._grpDefaultHeaderLabelHorizontal.buttons():
            if self._grpDefaultHeaderLabelHorizontal.id(button) == type.value:
                button.setChecked(True)


    def defaultHeaderLabelHorizontal(self):

        return Preferences.HeaderLabel(self._grpDefaultHeaderLabelHorizontal.checkedId())


    def setDefaultHeaderLabelVertical(self, type):

        if type.value != self._grpDefaultHeaderLabelVertical.checkedId():
            self._onPreferencesChanged()

        for button in self._grpDefaultHeaderLabelVertical.buttons():
            if self._grpDefaultHeaderLabelVertical.id(button) == type.value:
                button.setChecked(True)


    def defaultHeaderLabelVertical(self):

        return Preferences.HeaderLabel(self._grpDefaultHeaderLabelVertical.checkedId())


    def setDefaultCellCountColumn(self, val):

        self._spbDefaultCellCountColumn.setValue(val)


    def defaultCellCountColumn(self):

        return self._spbDefaultCellCountColumn.value()


    def setDefaultCellCountRow(self, val):

        self._spbDefaultCellCountRow.setValue(val)


    def defaultCellCountRow(self):

        return self._spbDefaultCellCountRow.value()
