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

from PySide2.QtSvg import QSvgWidget
from PySide2.QtWidgets import QApplication, QHBoxLayout, QLabel, QVBoxLayout, QWidget

import icons


class DialogTitleBox(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        logo = QSvgWidget()
        logo.load(':/icons/apps/22/tabulator.svg')

        name = QLabel(self.tr(f'<strong style="font-size:large;">{QApplication.applicationName()}</strong> v{QApplication.applicationVersion()}'))
        description = QLabel(self.tr('An editor tool for documents with character-separated values'))

        labels = QVBoxLayout()
        labels.addWidget(name)
        labels.addWidget(description)

        # Main layout
        self.layout = QHBoxLayout(self)
        self.layout.addWidget(logo)
        self.layout.addLayout(labels)

        # Set logo size
        height = name.sizeHint().height() + labels.layout().spacing() + description.sizeHint().height()
        logo.setFixedSize(height, height)


    def setZeroMargins(self):

        self.layout.setContentsMargins(0, 0, 0, 0)
