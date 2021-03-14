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

from PySide2.QtCore import QFileInfo, Qt, Signal
from PySide2.QtWidgets import QWidget

from preferences import Preferences


class Document(QWidget):

    _preferences = Preferences()

    aboutToClose = Signal(str)


    def __init__(self, parent=None):
        super().__init__(parent)

        self._canonicalName = None
        self._canonicalIndex = 0

        self.setAttribute(Qt.WA_DeleteOnClose)


    def setPreferences(self, preferences):

        self._preferences = preferences


    def setCanonicalName(self, canonicalName):

        self._canonicalName = canonicalName


    def canonicalName(self):

        return self._canonicalName


    def setCanonicalIndex(self, canonicalIndex):

        self._canonicalIndex = canonicalIndex


    def canonicalIndex(self):

        return self._canonicalIndex


    def documentTitle(self):

        return self.windowTitle()


    def setDocumentTitle(self):

        fileName = QFileInfo(self._canonicalName).fileName() if self._canonicalName else self.tr('Untitled')

        if self._canonicalIndex > 1:
            self.setWindowTitle(self.tr(f'{fileName} ({self._canonicalIndex})'))
        else:
            self.setWindowTitle(fileName)


    def closeEvent(self, event):

        if True:
            # Document will be closed
            self.aboutToClose.emit(self._canonicalName)

            event.accept()
        else:
            event.ignore()


    def load(self, canonicalName):

        self.setCanonicalName(canonicalName)


        return True
