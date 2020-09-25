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
from PySide2.QtWidgets import QLabel, QVBoxLayout, QWidget


class PreferencesDocumentWidget(QWidget):

    settingChanged = Signal()


    def __init__(self, parent=None):
        """
        Initializes the PreferencesDocumentWidget class.
        """
        super(PreferencesDocumentWidget, self).__init__(parent)

        label = QLabel('<strong style="font-size:large;">Document</strong>')

        # Main layout
        layout = QVBoxLayout()
        layout.addWidget(label)
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
