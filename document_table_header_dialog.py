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
from PySide2.QtWidgets import (QButtonGroup, QCheckBox, QDialog, QDialogButtonBox, QGridLayout,
                               QGroupBox, QLabel, QLineEdit, QRadioButton, QVBoxLayout)

from settings import Settings


class DocumentTableHeaderDialog(QDialog):

    def __init__(self, type, index, parent=None):
        super(DocumentTableHeaderDialog, self).__init__(parent)

        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        # Group box
        text = 'Binary Number' if index >= 0 else 'Binary Numbers'
        toolTip = 'Change label to a binary number' if index >= 0 else 'Change all labels to binary numbers'
        rdbBinary = QRadioButton(text)
        rdbBinary.setToolTip(toolTip)

        text = 'With prefix 0b'
        toolTip = 'Change label to a binary number with prefix 0b otherwise without prefix' if index >= 0 else 'Change all labels to binary numbers with prefix 0b otherwise without prefix'
        self.chkBinary = QCheckBox(text)
        self.chkBinary.setChecked(True)
        self.chkBinary.setEnabled(False)
        self.chkBinary.setToolTip(toolTip)
        rdbBinary.toggled.connect(lambda checked: self.chkBinary.setEnabled(checked))

        text = 'Octal Number' if index >= 0 else 'Octal Numbers'
        toolTip = 'Change label to a octal number' if index >= 0 else 'Change all labels to octal numbers'
        rdbOctal = QRadioButton(text)
        rdbOctal.setToolTip(toolTip)

        text = 'With prefix 0o'
        toolTip = 'Change label to a octal number with prefix 0o otherwise without prefix' if index >= 0 else 'Change all labels to octal numbers with prefix 0o otherwise without prefix'
        self.chkOctal = QCheckBox(text)
        self.chkOctal.setChecked(True)
        self.chkOctal.setEnabled(False)
        self.chkOctal.setToolTip(toolTip)
        rdbOctal.toggled.connect(lambda checked: self.chkOctal.setEnabled(checked))

        text = 'Decimal Number' if index >= 0 else 'Decimal Numbers'
        toolTip = 'Change label to a decimal number' if index >= 0 else 'Change all labels to decimal numbers'
        rdbDecimal = QRadioButton(text)
        rdbDecimal.setToolTip(toolTip)

        text = 'Enumeration starting with 1'
        toolTip = 'Change label to a decimal number with the enumeration starting with 1 otherwise with 0' if index >= 0 else 'Change all labels to decimal numbers with the enumeration starting with 1 otherwise with 0'
        self.chkDecimal = QCheckBox(text)
        self.chkDecimal.setChecked(True)
        self.chkDecimal.setEnabled(False)
        self.chkDecimal.setToolTip(toolTip)
        rdbDecimal.toggled.connect(lambda checked: self.chkDecimal.setEnabled(checked))

        text = 'Hexadecimal Number' if index >= 0 else 'Hexadecimal Numbers'
        toolTip = 'Change label to a hexadecimal number' if index >= 0 else 'Change all labels to hexadecimal numbers'
        rdbHexadecimal = QRadioButton(text)
        rdbHexadecimal.setToolTip(toolTip)

        text = 'With prefix 0x'
        toolTip = 'Change label to a hexadecimal number with prefix 0x otherwise without prefix' if index >= 0 else 'Change all labels to hexadecimal numbers with prefix 0x otherwise without prefix'
        self.chkHexadecimal = QCheckBox(text)
        self.chkHexadecimal.setChecked(True)
        self.chkHexadecimal.setEnabled(False)
        self.chkHexadecimal.setToolTip(toolTip)
        rdbHexadecimal.toggled.connect(lambda checked: self.chkHexadecimal.setEnabled(checked))

        text = 'Capital Letter' if index >= 0 else 'Capital Letters'
        toolTip = 'Change label to a capital letter' if index >= 0 else 'Change all labels to capital letters'
        rdbLetter = QRadioButton(text)
        rdbLetter.setToolTip(toolTip)

        text = 'Letter as uppercase letter' if index >= 0 else 'Letters as uppercase letters'
        toolTip = 'Change label to a letter as uppercase letter otherwise lowercase letter' if index >= 0 else 'Change all labels to letters as uppercase letters otherwise lowercase letters'
        self.chkLetter = QCheckBox(text)
        self.chkLetter.setChecked(True)
        self.chkLetter.setEnabled(False)
        self.chkLetter.setToolTip(toolTip)
        rdbLetter.toggled.connect(lambda checked: self.chkLetter.setEnabled(checked))

        text = 'User-defined Text' if index >= 0 else 'User-defined Texts'
        toolTip = 'Change label to a user-defined text' if index >= 0 else 'Change all labels to user-defined texts'
        rdbCustom = QRadioButton(text)
        rdbCustom.setToolTip(toolTip)

        toolTip = 'Change label to a user-defined text' if index >= 0 else 'Change all labels to user-defined texts'
        self.ledCustom = QLineEdit()
        self.ledCustom.setEnabled(False)
        self.ledCustom.setToolTip(toolTip)
        rdbCustom.toggled.connect(lambda checked: self.ledCustom.setEnabled(checked))

        text = '# will be replaced with column index' if type == 'horizontal' else '# will be replaced with row index'
        lblCustom = QLabel(text)
        lblCustom.setEnabled(False)
        rdbCustom.toggled.connect(lambda checked: lblCustom.setEnabled(checked))

        self.grpHeaderLabel = QButtonGroup(self)
        self.grpHeaderLabel.addButton(rdbBinary, Settings.HeaderLabel.Binary.value)
        self.grpHeaderLabel.addButton(rdbOctal, Settings.HeaderLabel.Octal.value)
        self.grpHeaderLabel.addButton(rdbDecimal, Settings.HeaderLabel.Decimal.value)
        self.grpHeaderLabel.addButton(rdbHexadecimal, Settings.HeaderLabel.Hexadecimal.value)
        self.grpHeaderLabel.addButton(rdbLetter, Settings.HeaderLabel.Letter.value)
        self.grpHeaderLabel.addButton(rdbCustom, Settings.HeaderLabel.Custom.value)
        self.grpHeaderLabel.buttonClicked.connect(self.onSettingChanged)

        groupLayout = QGridLayout()
        groupLayout.addWidget(rdbBinary, 0, 0)
        groupLayout.addWidget(self.chkBinary, 0, 1)
        groupLayout.addWidget(rdbOctal, 1, 0)
        groupLayout.addWidget(self.chkOctal, 1, 1)
        groupLayout.addWidget(rdbDecimal, 2, 0)
        groupLayout.addWidget(self.chkDecimal, 2, 1)
        groupLayout.addWidget(rdbHexadecimal, 3, 0)
        groupLayout.addWidget(self.chkHexadecimal, 3, 1)
        groupLayout.addWidget(rdbLetter, 4, 0)
        groupLayout.addWidget(self.chkLetter, 4, 1)
        groupLayout.addWidget(rdbCustom, 5, 0)
        groupLayout.addWidget(self.ledCustom, 5, 1)
        groupLayout.addWidget(lblCustom, 6, 1)
        groupLayout.setRowStretch(7, 1)

        text = 'Change label to a …' if index >= 0 else 'Change all labels to …'
        groupBox = QGroupBox(text)
        groupBox.setLayout(groupLayout)

        # Button box
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonOk = buttonBox.button(QDialogButtonBox.Ok)
        self.buttonOk.setEnabled(False)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        # Main layout
        layout = QVBoxLayout()
        layout.addWidget(groupBox)
        layout.addWidget(buttonBox)

        self.setLayout(layout)


    def onSettingChanged(self):
        """
        Enables the ok button if a setting has been changed.
        """
        self.buttonOk.setEnabled(True)


    def headerLabelType(self):
        """
        Returns the type of the header label.
        """
        return Settings.HeaderLabel(self.grpHeaderLabel.checkedId())


    def headerLabelParameter(self):
        """
        Returns the parameter of the header label.
        """
        type = self.headerLabelType()

        if type == Settings.HeaderLabel.Binary:
            return '0b' if self.chkBinary.isChecked() else ''
        elif type == Settings.HeaderLabel.Octal:
            return '0o' if self.chkOctal.isChecked() else ''
        elif type == Settings.HeaderLabel.Decimal:
            return '1' if self.chkDecimal.isChecked() else '0'
        elif type == Settings.HeaderLabel.Hexadecimal:
            return '0x' if self.chkHexadecimal.isChecked() else ''
        elif type == Settings.HeaderLabel.Letter:
            return 'upper' if self.chkLetter.isChecked() else 'lower'
        elif type == Settings.HeaderLabel.Custom:
            return self.ledCustom.text()
        else:
            return ''
