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
from PySide2.QtWidgets import QDialog, QDialogButtonBox, QGroupBox, QVBoxLayout


class DocumentTableHeaderDialog(QDialog):

    def __init__(self, number, parent=None):
        super(DocumentTableHeaderDialog, self).__init__(parent)

        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        # Group box
        groupLayout = QVBoxLayout()
        groupLayout.addStretch(1)

        text = 'Change label to a …' if isinstance(number, int) else 'Change all labels to …'
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
