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

from enum import Enum


class Settings():

    class HeaderLabel(Enum):
        Custom = 0
        Binary = 2
        Octal = 8
        Decimal = 10
        Hexadecimal = 16
        Letter = 26


    def __init__(self):

        # General: State & Geometries
        self._restoreApplicationState = True
        self._restoreApplicationGeometry = True
        self._restoreDialogGeometry = True

        # Documents: Recently Opened Documents
        self._maximumRecentDocuments = 10

        # Document Presets: Header Labels
        self._defaultHeaderLabelHorizontal = self.HeaderLabel.Letter
        self._defaultHeaderLabelVertical = self.HeaderLabel.Decimal

        # Document Presets: Cell Counts
        self._defaultCellCountColumn = 25
        self._defaultCellCountRow = 50


    def load(self, settings):

        settings.beginGroup('Settings')

        # General: State & Geometries
        self.setRestoreApplicationState(self.valueToBool(settings.value('restoreApplicationState', True)))
        self.setRestoreApplicationGeometry(self.valueToBool(settings.value('restoreApplicationGeometry', True)))
        self.setRestoreDialogGeometry(self.valueToBool(settings.value('restoreDialogGeometry', True)))

        # Documents: Recently Opened Documents
        self.setMaximumRecentDocuments(int(settings.value('maximumRecentDocuments', 10)))

        # Document Presets: Header Labels
        self.setDefaultHeaderLabelHorizontal(Settings.HeaderLabel(int(settings.value('defaultHeaderLabelHorizontal', self.HeaderLabel.Letter.value))))
        self.setDefaultHeaderLabelVertical(Settings.HeaderLabel(int(settings.value('defaultHeaderLabelVertical', self.HeaderLabel.Decimal.value))))

        # Document Presets: Cell Counts
        self.setDefaultCellCountColumn(int(settings.value('defaultCellCountColumn', 25)))
        self.setDefaultCellCountRow(int(settings.value('defaultCellCountRow', 50)))

        settings.endGroup()


    @staticmethod
    def valueToBool(value):

        return value.lower() == 'true' if isinstance(value, str) else bool(value)


    def save(self, settings):

        settings.remove('Settings')

        settings.beginGroup('Settings')

        # General: State & Geometries
        settings.setValue('restoreApplicationState', self._restoreApplicationState)
        settings.setValue('restoreApplicationGeometry', self._restoreApplicationGeometry)
        settings.setValue('restoreDialogGeometry', self._restoreDialogGeometry)

        # Documents: Recently Opened Documents
        settings.setValue('maximumRecentDocuments', self._maximumRecentDocuments)

        # Document Presets: Header Labels
        settings.setValue('defaultHeaderLabelHorizontal', self._defaultHeaderLabelHorizontal.value)
        settings.setValue('defaultHeaderLabelVertical', self._defaultHeaderLabelVertical.value)

        # Document Presets: Cell Counts
        settings.setValue('defaultCellCountColumn', self._defaultCellCountColumn)
        settings.setValue('defaultCellCountRow', self._defaultCellCountRow)

        settings.endGroup()


    def setRestoreApplicationState(self, value):

        self._restoreApplicationState = value


    def restoreApplicationState(self, isDefault=False):

        return self._restoreApplicationState if not isDefault else True


    def setRestoreApplicationGeometry(self, value):

        self._restoreApplicationGeometry = value


    def restoreApplicationGeometry(self, isDefault=False):

        return self._restoreApplicationGeometry if not isDefault else True


    def setRestoreDialogGeometry(self, value):

        self._restoreDialogGeometry = value


    def restoreDialogGeometry(self, isDefault=False):

        return self._restoreDialogGeometry if not isDefault else True


    def setMaximumRecentDocuments(self, value):

        if value >= 0 and value <= 25:
            self._maximumRecentDocuments = value
        else:
            self._maximumRecentDocuments = 10


    def maximumRecentDocuments(self, isDefault=False):

        return self._maximumRecentDocuments if not isDefault else 10


    def setDefaultHeaderLabelHorizontal(self, value):

        self._defaultHeaderLabelHorizontal = value


    def defaultHeaderLabelHorizontal(self, isDefault=False):

        return self._defaultHeaderLabelHorizontal if not isDefault else self.HeaderLabel.Letter


    def setDefaultHeaderLabelVertical(self, value):

        self._defaultHeaderLabelVertical = value


    def defaultHeaderLabelVertical(self, isDefault=False):

        return self._defaultHeaderLabelVertical if not isDefault else self.HeaderLabel.Decimal


    def setDefaultCellCountColumn(self, value):

        if value >= 1 and value <= 1000:
            self._defaultCellCountColumn = value
        else:
            self._defaultCellCountColumn = 25


    def defaultCellCountColumn(self, isDefault=False):

        return self._defaultCellCountColumn if not isDefault else 25


    def setDefaultCellCountRow(self, value):

        if value >= 1 and value <= 1000:
            self._defaultCellCountRow = value
        else:
            self._defaultCellCountRow = 50


    def defaultCellCountRow(self, isDefault=False):

        return self._defaultCellCountRow if not isDefault else 50
