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

from PySide2.QtCore import QByteArray
from PySide2.QtWidgets import QDialog, QDialogButtonBox, QHBoxLayout, QListWidget, QStackedWidget, QVBoxLayout

from preferences_document_presets_page import PreferencesDocumentPresetsPage
from preferences_documents_page import PreferencesDocumentsPage
from preferences_general_page import PreferencesGeneralPage
from settings import Settings


class PreferencesDialog(QDialog):

    _settings = Settings()


    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle(self.tr('Preferences'))

        self.setDialogGeometry()

        # Settings box
        self.generalPage = PreferencesGeneralPage(self)
        self.generalPage.setZeroMargins()
        self.generalPage.settingsChanged.connect(self.onSettingsChanged)

        self.documentsPage = PreferencesDocumentsPage(self)
        self.documentsPage.setZeroMargins()
        self.documentsPage.settingsChanged.connect(self.onSettingsChanged)

        self.documentPresetsPage = PreferencesDocumentPresetsPage(self)
        self.documentPresetsPage.setZeroMargins()
        self.documentPresetsPage.settingsChanged.connect(self.onSettingsChanged)

        stackedBox = QStackedWidget()
        stackedBox.addWidget(self.generalPage)
        stackedBox.addWidget(self.documentsPage)
        stackedBox.addWidget(self.documentPresetsPage)
        stackedBox.setCurrentIndex(0)

        listBox = QListWidget()
        listBox.addItem(self.generalPage.title())
        listBox.addItem(self.documentsPage.title())
        listBox.addItem(self.documentPresetsPage.title())
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

        self.updateSettings()
        self.buttonApply.setEnabled(False)


    def setDialogGeometry(self, geometry=QByteArray()):

        if geometry:
            self.restoreGeometry(geometry)
        else:
            self.resize(800, 600)


    def dialogGeometry(self):

        return self.saveGeometry()


    def setSettings(self, settings):

        self._settings = settings

        self.updateSettings()
        self.buttonApply.setEnabled(False)


    def settings(self):

        return self._settings


    def onSettingsChanged(self):

        self.buttonApply.setEnabled(True)


    def onButtonDefaultsClicked(self):

        self.updateSettings(True)


    def onButtonOkClicked(self):

        self.saveSettings()
        self.close()


    def onButtonApplyClicked(self):

        self.saveSettings()
        self.buttonApply.setEnabled(False)


    def updateSettings(self, isDefault=False):

        # General: State & Geometries
        self.generalPage.setRestoreApplicationState(self._settings.restoreApplicationState(isDefault))
        self.generalPage.setRestoreApplicationGeometry(self._settings.restoreApplicationGeometry(isDefault))
        self.generalPage.setRestoreDialogGeometry(self._settings.restoreDialogGeometry(isDefault))

        # Documents: Recently Opened Documents
        self.documentsPage.setMaximumRecentDocuments(self._settings.maximumRecentDocuments(isDefault))

        # Document Presets: Header Labels
        self.documentPresetsPage.setDefaultHeaderLabelHorizontal(self._settings.defaultHeaderLabelHorizontal(isDefault))
        self.documentPresetsPage.setDefaultHeaderLabelVertical(self._settings.defaultHeaderLabelVertical(isDefault))

        # Document Presets: Cell Counts
        self.documentPresetsPage.setDefaultCellCountColumn(self._settings.defaultCellCountColumn(isDefault))

        # Document: Defaults
        self.documentPresetsPage.setDefaultCellRows(self._settings.defaultCellRows)


    def saveSettings(self):

        # General: State & Geometries
        self._settings.setRestoreApplicationState(self.generalPage.restoreApplicationState())
        self._settings.setRestoreApplicationGeometry(self.generalPage.restoreApplicationGeometry())
        self._settings.setRestoreDialogGeometry(self.generalPage.restoreDialogGeometry())

        # Documents: Recently Opened Documents
        self._settings.setMaximumRecentDocuments(self.documentsPage.maximumRecentDocuments())

        # Document Presets: Header Labels
        self._settings.setDefaultHeaderLabelHorizontal(self.documentPresetsPage.defaultHeaderLabelHorizontal())
        self._settings.setDefaultHeaderLabelVertical(self.documentPresetsPage.defaultHeaderLabelVertical())

        # Document Presets: Cell Counts
        self._settings.setDefaultCellCountColumn(self.documentPresetsPage.defaultCellCountColumn())

        # Document: Defaults
        self._settings.defaultCellRows = self.documentPresetsPage.defaultCellRows()
