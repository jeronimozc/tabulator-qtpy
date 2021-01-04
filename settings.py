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

    # Document: Defaults
    defaultHeaderLabelHorizontal = HeaderLabel.Letter
    defaultHeaderLabelVertical = HeaderLabel.Decimal
    defaultCellColumns = 25
    defaultCellRows = 50

    recentDocumentList = []

    def __init__(self):

        # General: State & Geometries
        self._restoreApplicationState = True
        self._restoreApplicationGeometry = True
        self._restoreDialogGeometry = True


    def load(self, settings):

        settings.beginGroup('Settings')

        # General: State & Geometries
        self.setRestoreApplicationState(self.valueToBool(settings.value('restoreApplicationState', True)))
        self.setRestoreApplicationGeometry(self.valueToBool(settings.value('restoreApplicationGeometry', True)))
        self.setRestoreDialogGeometry(self.valueToBool(settings.value('restoreDialogGeometry', True)))

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
