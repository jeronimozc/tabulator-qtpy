# This Python file uses the following encoding: utf-8
#
# Copyright 2020-2021 NotNypical, <https://notnypical.github.io>.
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

from PySide2.QtCore import QByteArray, QRect
from PySide2.QtWidgets import QApplication, QDialog, QDialogButtonBox, QVBoxLayout

from keyboard_shortcuts_widget import KeyboardShortcutsWidget


class KeyboardShortcutsDialog(QDialog):

    def __init__(self, parent=None):
        """
        Initializes the KeyboardShortcutsDialog class.
        """
        super(KeyboardShortcutsDialog, self).__init__(parent)

        # Button box
        buttonBox = QDialogButtonBox(QDialogButtonBox.Close)
        buttonBox.rejected.connect(self.close)

        # Main layout
        layout = QVBoxLayout()
        layout.addWidget(KeyboardShortcutsWidget(self.parentWidget()), 1)
        layout.addWidget(buttonBox)

        self.setLayout(layout)


    def windowGeometry(self):
        """
        Returns the geometry of the widget.
        """
        return self.saveGeometry()


    def setWindowGeometry(self, geometry):
        """
        Sets the geometry of the widget.
        """
        if geometry:
            self.restoreGeometry(geometry)
        else:
            availableGeometry = QRect(QApplication.desktop().availableGeometry(self))
            self.resize(availableGeometry.width() / 3, availableGeometry.height() / 3)
            self.move((availableGeometry.width() - self.width()) / 2, (availableGeometry.height() - self.height()) / 2)
