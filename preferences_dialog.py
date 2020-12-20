# This Python file uses the following encoding: utf-8
#
# Copyright 2020 NotNypical, <https://notnypical.github.io>.
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

from PySide2.QtCore import QByteArray
from PySide2.QtWidgets import QDialog, QDialogButtonBox, QHBoxLayout, QListWidget, QStackedWidget, QVBoxLayout

from preferences_document_settings import PreferencesDocumentSettings
from preferences_general_settings import PreferencesGeneralSettings
from settings import Settings


class PreferencesDialog(QDialog):

    _settings = Settings()


    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle(self.tr('Preferences'))

        self.setDialogGeometry()

        # Settings box
        self.generalSettings = PreferencesGeneralSettings(self)
        self.generalSettings.settingsChanged.connect(self.onSettingsChanged)

        self.documentSettings = PreferencesDocumentSettings(self)
        self.documentSettings.settingsChanged.connect(self.onSettingsChanged)

        stackedBox = QStackedWidget()
        stackedBox.addWidget(self.generalSettings)
        stackedBox.addWidget(self.documentSettings)
        stackedBox.setCurrentIndex(0)

        listBox = QListWidget()
        listBox.addItem(self.generalSettings.title())
        listBox.addItem(self.documentSettings.title())
        listBox.setCurrentRow(stackedBox.currentIndex())
        listBox.currentRowChanged.connect(stackedBox.setCurrentIndex)

        settingsBox = QHBoxLayout()
        settingsBox.addWidget(listBox, 1)
        settingsBox.addWidget(stackedBox, 3)

        # Button box
        buttonBox = QDialogButtonBox(QDialogButtonBox.RestoreDefaults | QDialogButtonBox.Ok | QDialogButtonBox.Apply | QDialogButtonBox.Cancel)
        self.buttonApply = buttonBox.button(QDialogButtonBox.Apply)
        buttonBox.button(QDialogButtonBox.RestoreDefaults).clicked.connect(self.onButtonDefaultsClicked)
        buttonBox.accepted.connect(self.onButtonOkClicked)
        buttonBox.button(QDialogButtonBox.Apply).clicked.connect(self.onButtonApplyClicked)
        buttonBox.rejected.connect(self.close)

        # Main layout
        layout = QVBoxLayout(self)
        layout.addLayout(settingsBox)
        layout.addWidget(buttonBox)

        self.updateSettings(self._settings)


    def setDialogGeometry(self, geometry=QByteArray()):

        if geometry:
            self.restoreGeometry(geometry)
        else:
            self.resize(800, 600)


    def dialogGeometry(self):

        return self.saveGeometry()


    def onSettingsChanged(self):

        self.buttonApply.setEnabled(True)


    def setSettings(self, settings):

        self.updateSettings(settings)
        self.saveSettings()


    def settings(self):

        return self._settings


    def onButtonDefaultsClicked(self):

        settings = Settings()
        self.updateSettings(settings)


    def onButtonOkClicked(self):

        self.saveSettings()
        self.close()


    def onButtonApplyClicked(self):

        self.saveSettings()


    def updateSettings(self, settings):

        # General
        self.generalSettings.setRestoreApplicationGeometry(settings.restoreWindowGeometry)
        self.generalSettings.setRestoreDialogGeometry(settings.restoreDialogGeometry)

        # Document: Defaults
        self.documentSettings.setDefaultHeaderLabelHorizontal(settings.defaultHeaderLabelHorizontal)
        self.documentSettings.setDefaultHeaderLabelVertical(settings.defaultHeaderLabelVertical)
        self.documentSettings.setDefaultCellColumns(settings.defaultCellColumns)
        self.documentSettings.setDefaultCellRows(settings.defaultCellRows)


    def saveSettings(self):

        # General
        self._settings.restoreWindowGeometry = self.generalSettings.restoreApplicationGeometry()
        self._settings.restoreDialogGeometry = self.generalSettings.restoreDialogGeometry()

        # Document: Defaults
        self._settings.defaultHeaderLabelHorizontal = self.documentSettings.defaultHeaderLabelHorizontal()
        self._settings.defaultHeaderLabelVertical = self.documentSettings.defaultHeaderLabelVertical()
        self._settings.defaultCellColumns = self.documentSettings.defaultCellColumns()
        self._settings.defaultCellRows = self.documentSettings.defaultCellRows()

        self.buttonApply.setEnabled(False)
