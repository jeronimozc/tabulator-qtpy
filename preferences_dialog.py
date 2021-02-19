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

from preferences import Preferences
from preferences_document_presets_page import PreferencesDocumentPresetsPage
from preferences_documents_page import PreferencesDocumentsPage
from preferences_general_page import PreferencesGeneralPage


class PreferencesDialog(QDialog):

    _preferences = Preferences()


    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle(self.tr('Preferences'))

        # Preferences box
        self.generalPage = PreferencesGeneralPage(self)
        self.generalPage.setZeroMargins()
        self.generalPage.preferencesChanged.connect(self.onPreferencesChanged)

        self.documentsPage = PreferencesDocumentsPage(self)
        self.documentsPage.setZeroMargins()
        self.documentsPage.preferencesChanged.connect(self.onPreferencesChanged)

        self.documentPresetsPage = PreferencesDocumentPresetsPage(self)
        self.documentPresetsPage.setZeroMargins()
        self.documentPresetsPage.preferencesChanged.connect(self.onPreferencesChanged)

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

        preferencesBox = QHBoxLayout()
        preferencesBox.addWidget(listBox, 1)
        preferencesBox.addWidget(stackedBox, 3)

        # Button box
        buttonBox = QDialogButtonBox(QDialogButtonBox.RestoreDefaults | QDialogButtonBox.Ok | QDialogButtonBox.Apply | QDialogButtonBox.Cancel)
        self.buttonApply = buttonBox.button(QDialogButtonBox.Apply)
        buttonBox.button(QDialogButtonBox.RestoreDefaults).clicked.connect(self.onButtonDefaultsClicked)
        buttonBox.accepted.connect(self.onButtonOkClicked)
        buttonBox.button(QDialogButtonBox.Apply).clicked.connect(self.onButtonApplyClicked)
        buttonBox.rejected.connect(self.close)

        # Main layout
        layout = QVBoxLayout(self)
        layout.addLayout(preferencesBox)
        layout.addWidget(buttonBox)

        self.updatePreferences()
        self.buttonApply.setEnabled(False)


    def setDialogGeometry(self, geometry=QByteArray()):

        if not geometry.isEmpty():
            self.restoreGeometry(geometry)
        else:
            self.resize(800, 600)


    def dialogGeometry(self):

        return self.saveGeometry()


    def setPreferences(self, preferences):

        self._preferences = preferences

        self.updatePreferences()
        self.buttonApply.setEnabled(False)


    def preferences(self):

        return self._preferences


    def onPreferencesChanged(self):

        self.buttonApply.setEnabled(True)


    def onButtonDefaultsClicked(self):

        self.updatePreferences(True)


    def onButtonOkClicked(self):

        self.savePreferences()
        self.close()


    def onButtonApplyClicked(self):

        self.savePreferences()
        self.buttonApply.setEnabled(False)


    def updatePreferences(self, isDefault=False):

        # General: State & Geometries
        self.generalPage.setRestoreApplicationState(self._preferences.restoreApplicationState(isDefault))
        self.generalPage.setRestoreApplicationGeometry(self._preferences.restoreApplicationGeometry(isDefault))
        self.generalPage.setRestoreDialogGeometry(self._preferences.restoreDialogGeometry(isDefault))

        # Documents: Recently Opened Documents
        self.documentsPage.setMaximumRecentDocuments(self._preferences.maximumRecentDocuments(isDefault))

        # Document Presets: Header Labels
        self.documentPresetsPage.setDefaultHeaderLabelHorizontal(self._preferences.defaultHeaderLabelHorizontal(isDefault))
        self.documentPresetsPage.setDefaultHeaderLabelVertical(self._preferences.defaultHeaderLabelVertical(isDefault))

        # Document Presets: Cell Counts
        self.documentPresetsPage.setDefaultCellCountColumn(self._preferences.defaultCellCountColumn(isDefault))
        self.documentPresetsPage.setDefaultCellCountRow(self._preferences.defaultCellCountRow(isDefault))


    def savePreferences(self):

        # General: State & Geometries
        self._preferences.setRestoreApplicationState(self.generalPage.restoreApplicationState())
        self._preferences.setRestoreApplicationGeometry(self.generalPage.restoreApplicationGeometry())
        self._preferences.setRestoreDialogGeometry(self.generalPage.restoreDialogGeometry())

        # Documents: Recently Opened Documents
        self._preferences.setMaximumRecentDocuments(self.documentsPage.maximumRecentDocuments())

        # Document Presets: Header Labels
        self._preferences.setDefaultHeaderLabelHorizontal(self.documentPresetsPage.defaultHeaderLabelHorizontal())
        self._preferences.setDefaultHeaderLabelVertical(self.documentPresetsPage.defaultHeaderLabelVertical())

        # Document Presets: Cell Counts
        self._preferences.setDefaultCellCountColumn(self.documentPresetsPage.defaultCellCountColumn())
        self._preferences.setDefaultCellCountRow(self.documentPresetsPage.defaultCellCountRow())
