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
from PySide2.QtWidgets import QButtonGroup, QFormLayout, QGroupBox, QHBoxLayout, QLabel, QRadioButton, QVBoxLayout, QWidget


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

        # Main layout
        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(headerLabelsGroup)
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
