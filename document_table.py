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
from PySide2.QtWidgets import QHeaderView, QMenu, QTableWidget

from settings import Settings


class DocumentTable(QTableWidget):

    m_settings = Settings()


    def __init__(self, parent=None):
        super(DocumentTable, self).__init__(parent)

        self.setAttribute(Qt.WA_DeleteOnClose)

        # Creates a default document
        self.setColumnCount(self.m_settings.newDocumentColumns)
        self.setRowCount(self.m_settings.newDocumentRows)

        # Enable context menus
        hHeaderView = self.horizontalHeader()
        hHeaderView.setContextMenuPolicy(Qt.CustomContextMenu)
        hHeaderView.customContextMenuRequested.connect(self.contextMenuHorizontalHeader)


    def setSettings(self, settings):
        """
        Sets the user preferences.
        """
        self.m_settings = settings


    def contextMenuHorizontalHeader(self, pos):
        """
        Creates a context menu for the horizonzal header.
        """
        contextMenu = QMenu(self)
        contextMenu.exec_(self.mapToGlobal(pos))
