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

from enum import Enum


class Preferences:

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

        settings.beginGroup('Preferences')

        # General: State & Geometries
        self.setRestoreApplicationState(self.valueToBool(settings.value('RestoreApplicationState', True)))
        self.setRestoreApplicationGeometry(self.valueToBool(settings.value('RestoreApplicationGeometry', True)))
        self.setRestoreDialogGeometry(self.valueToBool(settings.value('RestoreDialogGeometry', True)))

        # Documents: Recently Opened Documents
        self.setMaximumRecentDocuments(int(settings.value('MaximumRecentDocuments', 10)))

        # Document Presets: Header Labels
        self.setDefaultHeaderLabelHorizontal(Preferences.HeaderLabel(int(settings.value('DefaultHeaderLabelHorizontal', self.HeaderLabel.Letter.value))))
        self.setDefaultHeaderLabelVertical(Preferences.HeaderLabel(int(settings.value('DefaultHeaderLabelVertical', self.HeaderLabel.Decimal.value))))

        # Document Presets: Cell Counts
        self.setDefaultCellCountColumn(int(settings.value('DefaultCellCountColumn', 25)))
        self.setDefaultCellCountRow(int(settings.value('DefaultCellCountRow', 50)))

        settings.endGroup()


    def save(self, settings):

        settings.beginGroup('Preferences')
        settings.remove('')

        # General: State & Geometries
        settings.setValue('RestoreApplicationState', self._restoreApplicationState)
        settings.setValue('RestoreApplicationGeometry', self._restoreApplicationGeometry)
        settings.setValue('RestoreDialogGeometry', self._restoreDialogGeometry)

        # Documents: Recently Opened Documents
        settings.setValue('MaximumRecentDocuments', self._maximumRecentDocuments)

        # Document Presets: Header Labels
        settings.setValue('DefaultHeaderLabelHorizontal', self._defaultHeaderLabelHorizontal.value)
        settings.setValue('DefaultHeaderLabelVertical', self._defaultHeaderLabelVertical.value)

        # Document Presets: Cell Counts
        settings.setValue('DefaultCellCountColumn', self._defaultCellCountColumn)
        settings.setValue('DefaultCellCountRow', self._defaultCellCountRow)

        settings.endGroup()


    @staticmethod
    def valueToBool(value):

        return value.lower() == 'true' if isinstance(value, str) else bool(value)


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

        self._maximumRecentDocuments = value if value >= 0 and value <= 25 else 10


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

        self._defaultCellCountColumn = value if value >= 1 and value <= 1000 else 25


    def defaultCellCountColumn(self, isDefault=False):

        return self._defaultCellCountColumn if not isDefault else 25


    def setDefaultCellCountRow(self, value):

        self._defaultCellCountRow = value if value >= 1 and value <= 1000 else 50


    def defaultCellCountRow(self, isDefault=False):

        return self._defaultCellCountRow if not isDefault else 50
