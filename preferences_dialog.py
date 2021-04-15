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

from PySide2.QtWidgets import QDialog, QDialogButtonBox, QHBoxLayout, QListWidget, QStackedWidget, QVBoxLayout

from preferences import Preferences
from preferences_document_presets_page import PreferencesDocumentPresetsPage
from preferences_documents_page import PreferencesDocumentsPage
from preferences_general_page import PreferencesGeneralPage


class PreferencesDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setMinimumSize(800, 600)
        self.setWindowTitle(self.tr("Preferences"))

        self._preferences = Preferences()

        #
        # Content

        self._generalPage = PreferencesGeneralPage()
        self._generalPage.setZeroMargins()
        self._generalPage.preferencesChanged.connect(self._onPreferencesChanged)

        self._documentsPage = PreferencesDocumentsPage()
        self._documentsPage.setZeroMargins()
        self._documentsPage.preferencesChanged.connect(self._onPreferencesChanged)

        self._documentPresetsPage = PreferencesDocumentPresetsPage()
        self._documentPresetsPage.setZeroMargins()
        self._documentPresetsPage.preferencesChanged.connect(self._onPreferencesChanged)

        stackedBox = QStackedWidget()
        stackedBox.addWidget(self._generalPage)
        stackedBox.addWidget(self._documentsPage)
        stackedBox.addWidget(self._documentPresetsPage)
        stackedBox.setCurrentIndex(0)

        listBox = QListWidget()
        listBox.addItem(self._generalPage.title())
        listBox.addItem(self._documentsPage.title())
        listBox.addItem(self._documentPresetsPage.title())
        listBox.setCurrentRow(stackedBox.currentIndex())
        listBox.currentRowChanged.connect(stackedBox.setCurrentIndex)

        preferencesBox = QHBoxLayout()
        preferencesBox.addWidget(listBox, 1)
        preferencesBox.addWidget(stackedBox, 3)

        # Button box
        buttonBox = QDialogButtonBox(QDialogButtonBox.RestoreDefaults | QDialogButtonBox.Ok | QDialogButtonBox.Apply | QDialogButtonBox.Cancel)
        self._buttonApply = buttonBox.button(QDialogButtonBox.Apply)
        buttonBox.button(QDialogButtonBox.RestoreDefaults).clicked.connect(self._onButtonDefaultsClicked)
        buttonBox.accepted.connect(self._onButtonOkClicked)
        buttonBox.button(QDialogButtonBox.Apply).clicked.connect(self._onButtonApplyClicked)
        buttonBox.rejected.connect(self.close)

        # Main layout
        layout = QVBoxLayout(self)
        layout.addLayout(preferencesBox)
        layout.addWidget(buttonBox)

        self._updatePreferences()
        self._buttonApply.setEnabled(False)


    def setPreferences(self, preferences):

        self._preferences = preferences

        self._updatePreferences()
        self._buttonApply.setEnabled(False)


    def preferences(self):

        return self._preferences


    def _onPreferencesChanged(self):

        self._buttonApply.setEnabled(True)


    def _onButtonDefaultsClicked(self):

        self._updatePreferences(True)


    def _onButtonOkClicked(self):

        self._savePreferences()
        self.close()


    def _onButtonApplyClicked(self):

        self._savePreferences()
        self._buttonApply.setEnabled(False)


    def _updatePreferences(self, isDefault=False):

        # General: Geometry & State
        self._generalPage.setRestoreApplicationGeometry(self._preferences.restoreApplicationGeometry(isDefault))
        self._generalPage.setRestoreApplicationState(self._preferences.restoreApplicationState(isDefault))

        # General: Recently Opened Documents
        self._generalPage.setMaximumRecentDocuments(self._preferences.maximumRecentDocuments(isDefault))
        self._generalPage.setRestoreRecentDocuments(self._preferences.restoreRecentDocuments(isDefault))

        # Document Presets: Header Labels
        self._documentPresetsPage.setDefaultHeaderLabelHorizontal(self._preferences.defaultHeaderLabelHorizontal(isDefault))
        self._documentPresetsPage.setDefaultHeaderLabelVertical(self._preferences.defaultHeaderLabelVertical(isDefault))

        # Document Presets: Cell Counts
        self._documentPresetsPage.setDefaultCellCountColumn(self._preferences.defaultCellCountColumn(isDefault))
        self._documentPresetsPage.setDefaultCellCountRow(self._preferences.defaultCellCountRow(isDefault))


    def _savePreferences(self):

        # General: Geometry & State
        self._preferences.setRestoreApplicationGeometry(self._generalPage.restoreApplicationGeometry())
        self._preferences.setRestoreApplicationState(self._generalPage.restoreApplicationState())

        # General: Recently Opened Documents
        self._preferences.setMaximumRecentDocuments(self._generalPage.maximumRecentDocuments())
        self._preferences.setRestoreRecentDocuments(self._generalPage.restoreRecentDocuments())

        # Document Presets: Header Labels
        self._preferences.setDefaultHeaderLabelHorizontal(self._documentPresetsPage.defaultHeaderLabelHorizontal())
        self._preferences.setDefaultHeaderLabelVertical(self._documentPresetsPage.defaultHeaderLabelVertical())

        # Document Presets: Cell Counts
        self._preferences.setDefaultCellCountColumn(self._documentPresetsPage.defaultCellCountColumn())
        self._preferences.setDefaultCellCountRow(self._documentPresetsPage.defaultCellCountRow())
