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

from PySide2.QtCore import QByteArray, QFileInfo, QSettings, QStandardPaths, Qt
from PySide2.QtGui import QIcon, QKeySequence
from PySide2.QtWidgets import QAction, QActionGroup, QApplication, QFileDialog, QMainWindow, QMdiArea, QMenu

from about_dialog import AboutDialog
from colophon_dialog import ColophonDialog
from document import Document
from keyboard_shortcuts_dialog import KeyboardShortcutsDialog
from preferences import Preferences
from preferences_dialog import PreferencesDialog

import icons


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowIcon(QIcon(':/icons/apps/16/tabulator.svg'))

        self._recentDocuments = []
        self._actionRecentDocuments = []
        self._keyboardShortcutsDialog = None

        self._preferences = Preferences()
        self._preferences.loadSettings()

        self._createActions()
        self._createMenus()
        self._createToolBars()

        self._loadSettings()

        self._updateActions()
        self._updateActionFullScreen()
        self._updateMenuOpenRecent()

        # Central widget
        self._documentArea = QMdiArea()
        self._documentArea.setViewMode(QMdiArea.TabbedView)
        self._documentArea.setTabsMovable(True)
        self._documentArea.setTabsClosable(True)
        self.setCentralWidget(self._documentArea)
        self._documentArea.subWindowActivated.connect(self._onDocumentWindowActivated)


    def closeEvent(self, event):

        if True:
            # Store application properties and preferences
            self._saveSettings()
            self._preferences.saveSettings()

            event.accept()
        else:
            event.ignore()


    def _loadSettings(self):

        settings = QSettings()

        # Recent documents
        size = settings.beginReadArray('RecentDocuments')
        for idx in range(size-1, -1, -1):
            settings.setArrayIndex(idx)
            canonicalName = QFileInfo(settings.value('Document')).canonicalFilePath()
            self._updateRecentDocuments(canonicalName)
        settings.endArray()

        # Application properties: Geometry
        geometry = settings.value('Application/Geometry', QByteArray()) if self._preferences.restoreApplicationGeometry() else QByteArray()
        if not geometry.isEmpty():
            self.restoreGeometry(geometry)
        else:
            availableGeometry = self.screen().availableGeometry()
            self.resize(availableGeometry.width() * 2/3, availableGeometry.height() * 2/3)
            self.move((availableGeometry.width() - self.width()) / 2, (availableGeometry.height() - self.height()) / 2)

        # Application properties: State
        state = settings.value('Application/State', QByteArray()) if self._preferences.restoreApplicationState() else QByteArray()
        if not state.isEmpty():
            self.restoreState(state)
        else:
            self._toolbarApplication.setVisible(True)
            self._toolbarDocument.setVisible(True)
            self._toolbarEdit.setVisible(True)
            self._toolbarTools.setVisible(True)
            self._toolbarView.setVisible(False)
            self._toolbarHelp.setVisible(False)


    def _saveSettings(self):

        settings = QSettings()

        # Recent documents
        if not self._preferences.restoreRecentDocuments():
            self._recentDocuments.clear()
        settings.remove('RecentDocuments')
        settings.beginWriteArray('RecentDocuments')
        for idx in range(len(self._recentDocuments)):
            settings.setArrayIndex(idx)
            settings.setValue('Document', self._recentDocuments[idx])
        settings.endArray()

        # Application properties: Geometry
        geometry = self.saveGeometry() if self._preferences.restoreApplicationGeometry() else QByteArray()
        settings.setValue('Application/Geometry', geometry)

        # Application properties: State
        state = self.saveState() if self._preferences.restoreApplicationState() else QByteArray()
        settings.setValue('Application/State', state)


    def _createActions(self):

        # Actions: Application

        self._actionAbout = QAction(self.tr(f'About {QApplication.applicationName()}'), self)
        self._actionAbout.setObjectName('actionAbout')
        self._actionAbout.setIcon(QIcon(':/icons/apps/16/tabulator.svg'))
        self._actionAbout.setIconText(self.tr('About'))
        self._actionAbout.setToolTip(self.tr('Brief description of the application'))
        self._actionAbout.triggered.connect(self._onActionAboutTriggered)

        self._actionColophon = QAction(self.tr('Colophon'), self)
        self._actionColophon.setObjectName('actionColophon')
        self._actionColophon.setToolTip(self.tr('Lengthy description of the application'))
        self._actionColophon.triggered.connect(self._onActionColophonTriggered)

        self._actionPreferences = QAction(self.tr('Preferences…'), self)
        self._actionPreferences.setObjectName('actionPreferences')
        self._actionPreferences.setIcon(QIcon.fromTheme('configure', QIcon(':/icons/actions/16/application-configure.svg')))
        self._actionPreferences.setToolTip(self.tr('Customize the appearance and behavior of the application'))
        self._actionPreferences.triggered.connect(self._onActionPreferencesTriggered)

        self._actionQuit = QAction(self.tr('Quit'), self)
        self._actionQuit.setObjectName('actionQuit')
        self._actionQuit.setIcon(QIcon.fromTheme('application-exit', QIcon(':/icons/actions/16/application-exit.svg')))
        self._actionQuit.setShortcut(QKeySequence.Quit)
        self._actionQuit.setToolTip(self.tr('Quit the application'))
        self._actionQuit.triggered.connect(self.close)

        # Actions: Document

        self._actionNew = QAction(self.tr('New'), self)
        self._actionNew.setObjectName('actionNew')
        self._actionNew.setIcon(QIcon.fromTheme('document-new', QIcon(':/icons/actions/16/document-new.svg')))
        self._actionNew.setShortcut(QKeySequence.New)
        self._actionNew.setToolTip(self.tr('Create new document'))
        self._actionNew.triggered.connect(self._onActionNewTriggered)

        self._actionOpen = QAction(self.tr('Open…'), self)
        self._actionOpen.setObjectName('actionOpen')
        self._actionOpen.setIcon(QIcon.fromTheme('document-open', QIcon(':/icons/actions/16/document-open.svg')))
        self._actionOpen.setShortcut(QKeySequence.Open)
        self._actionOpen.setToolTip(self.tr('Open an existing document'))
        self._actionOpen.triggered.connect(self._onActionOpenTriggered)

        self._actionOpenRecentClear = QAction(self.tr('Clear List'), self)
        self._actionOpenRecentClear.setObjectName('actionOpenRecentClear')
        self._actionOpenRecentClear.setToolTip(self.tr('Clear document list'))
        self._actionOpenRecentClear.triggered.connect(self._onActionOpenRecentClearTriggered)

        self._actionSave = QAction(self.tr('Save'), self)
        self._actionSave.setObjectName('actionSave')
        self._actionSave.setIcon(QIcon.fromTheme('document-save', QIcon(':/icons/actions/16/document-save.svg')))
        self._actionSave.setShortcut(QKeySequence.Save)
        self._actionSave.setToolTip(self.tr('Save document'))
        self._actionSave.triggered.connect(self._onActionSaveTriggered)

        self._actionSaveAs = QAction(self.tr('Save As…'), self)
        self._actionSaveAs.setObjectName('actionSaveAs')
        self._actionSaveAs.setIcon(QIcon.fromTheme('document-save-as', QIcon(':/icons/actions/16/document-save-as.svg')))
        self._actionSaveAs.setShortcut(QKeySequence.SaveAs)
        self._actionSaveAs.setToolTip(self.tr('Save document under a new name'))
        self._actionSaveAs.triggered.connect(self._onActionSaveAsTriggered)

        self._actionSaveAsDelimiterColon = QAction(self.tr('Colon'), self)
        self._actionSaveAsDelimiterColon.setObjectName('actionSaveAsDelimiterColon')
        self._actionSaveAsDelimiterColon.setCheckable(True)
        self._actionSaveAsDelimiterColon.setToolTip(self.tr('Save document with colon as delimiter under a new name'))
        self._actionSaveAsDelimiterColon.setData('colon')
        self._actionSaveAsDelimiterColon.triggered.connect(lambda: self._onActionSaveAsDelimiterTriggered('colon') )

        self._actionSaveAsDelimiterComma = QAction(self.tr('Comma'), self)
        self._actionSaveAsDelimiterComma.setObjectName('actionSaveAsDelimiterComma')
        self._actionSaveAsDelimiterComma.setCheckable(True)
        self._actionSaveAsDelimiterComma.setToolTip(self.tr('Save document with comma as delimiter under a new name'))
        self._actionSaveAsDelimiterComma.setData('comma')
        self._actionSaveAsDelimiterComma.triggered.connect(lambda: self._onActionSaveAsDelimiterTriggered('comma') )

        self._actionSaveAsDelimiterSemicolon = QAction(self.tr('Semicolon'), self)
        self._actionSaveAsDelimiterSemicolon.setObjectName('actionSaveAsDelimiterSemicolon')
        self._actionSaveAsDelimiterSemicolon.setCheckable(True)
        self._actionSaveAsDelimiterSemicolon.setToolTip(self.tr('Save document with semicolon as delimiter under a new name'))
        self._actionSaveAsDelimiterSemicolon.setData('semicolon')
        self._actionSaveAsDelimiterSemicolon.triggered.connect(lambda: self._onActionSaveAsDelimiterTriggered('semicolon') )

        self._actionSaveAsDelimiterTab = QAction(self.tr('Tab'), self)
        self._actionSaveAsDelimiterTab.setObjectName('actionSaveAsDelimiterTab')
        self._actionSaveAsDelimiterTab.setCheckable(True)
        self._actionSaveAsDelimiterTab.setToolTip(self.tr('Save document with tab as delimiter under a new name'))
        self._actionSaveAsDelimiterTab.setData('tab')
        self._actionSaveAsDelimiterTab.triggered.connect(lambda: self._onActionSaveAsDelimiterTriggered('tab') )

        self._actionSaveAsDelimiter = QActionGroup(self)
        self._actionSaveAsDelimiter.setObjectName('actionSaveAsDelimiter')
        self._actionSaveAsDelimiter.addAction(self._actionSaveAsDelimiterColon)
        self._actionSaveAsDelimiter.addAction(self._actionSaveAsDelimiterComma)
        self._actionSaveAsDelimiter.addAction(self._actionSaveAsDelimiterSemicolon)
        self._actionSaveAsDelimiter.addAction(self._actionSaveAsDelimiterTab)

        self._actionSaveCopyAs = QAction(self.tr('Save Copy As…'), self)
        self._actionSaveCopyAs.setObjectName('actionSaveCopyAs')
        self._actionSaveCopyAs.setIcon(QIcon.fromTheme('document-save-as', QIcon(':/icons/actions/16/document-save-as.svg')))
        self._actionSaveCopyAs.setToolTip(self.tr('Save copy of document under a new name'))
        self._actionSaveCopyAs.triggered.connect(self._onActionSaveCopyAsTriggered)

        self._actionSaveAll = QAction(self.tr('Save All'), self)
        self._actionSaveAll.setObjectName('actionSaveAll')
        self._actionSaveAll.setIcon(QIcon.fromTheme('document-save-all', QIcon(':/icons/actions/16/document-save-all.svg')))
        self._actionSaveAll.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_L))
        self._actionSaveAll.setToolTip(self.tr('Save all documents'))
        self._actionSaveAll.triggered.connect(self._onActionSaveAllTriggered)

        self._actionClose = QAction(self.tr('Close'), self)
        self._actionClose.setObjectName('actionClose')
        self._actionClose.setIcon(QIcon.fromTheme('document-close', QIcon(':/icons/actions/16/document-close.svg')))
        self._actionClose.setShortcut(QKeySequence.Close)
        self._actionClose.setToolTip('Close document')
        self._actionClose.triggered.connect(self._onActionCloseTriggered)

        self._actionCloseOther = QAction(self.tr('Close Other'), self)
        self._actionCloseOther.setObjectName('actionCloseOther')
        self._actionCloseOther.setToolTip('Close all other documents')
        self._actionCloseOther.triggered.connect(self._onActionCloseOtherTriggered)

        self._actionCloseAll = QAction(self.tr('Close All'), self)
        self._actionCloseAll.setObjectName('actionCloseAll')
        self._actionCloseAll.setShortcut(QKeySequence(Qt.CTRL + Qt.SHIFT + Qt.Key_W))
        self._actionCloseAll.setToolTip('Close all documents')
        self._actionCloseAll.triggered.connect(self._onActionCloseAllTriggered)

        # Actions: View

        self._actionFullScreen = QAction(self)
        self._actionFullScreen.setObjectName('actionFullScreen')
        self._actionFullScreen.setIconText(self.tr('Full Screen'))
        self._actionFullScreen.setCheckable(True)
        self._actionFullScreen.setShortcuts([QKeySequence(Qt.Key_F11), QKeySequence.FullScreen])
        self._actionFullScreen.triggered.connect(self._onActionFullScreenTriggered)

        self._actionTitlebarFullPath = QAction(self.tr('Show Path in Titlebar'), self)
        self._actionTitlebarFullPath.setObjectName('actionTitlebarFullPath')
        self._actionTitlebarFullPath.setCheckable(True)
        self._actionTitlebarFullPath.setChecked(True)
        self._actionTitlebarFullPath.setToolTip(self.tr('Display the full path of the document in the titlebar'))
        self._actionTitlebarFullPath.triggered.connect(self._onActionTitlebarFullPathTriggered)

        self._actionToolbarApplication = QAction(self.tr('Show Application Toolbar'), self)
        self._actionToolbarApplication.setObjectName('actionToolbarApplication')
        self._actionToolbarApplication.setCheckable(True)
        self._actionToolbarApplication.setToolTip(self.tr('Display the Application toolbar'))
        self._actionToolbarApplication.toggled.connect(lambda checked: self._toolbarApplication.setVisible(checked))

        self._actionToolbarDocument = QAction(self.tr('Show Document Toolbar'), self)
        self._actionToolbarDocument.setObjectName('actionToolbarDocument')
        self._actionToolbarDocument.setCheckable(True)
        self._actionToolbarDocument.setToolTip(self.tr('Display the Document toolbar'))
        self._actionToolbarDocument.toggled.connect(lambda checked: self._toolbarDocument.setVisible(checked))

        self._actionToolbarEdit = QAction(self.tr('Show Edit Toolbar'), self)
        self._actionToolbarEdit.setObjectName('actionToolbarEdit')
        self._actionToolbarEdit.setCheckable(True)
        self._actionToolbarEdit.setToolTip(self.tr('Display the Edit toolbar'))
        self._actionToolbarEdit.toggled.connect(lambda checked: self._toolbarEdit.setVisible(checked))

        self._actionToolbarTools = QAction(self.tr('Show Tools Toolbar'), self)
        self._actionToolbarTools.setObjectName('actionToolbarTools')
        self._actionToolbarTools.setCheckable(True)
        self._actionToolbarTools.setToolTip(self.tr('Display the Tools toolbar'))
        self._actionToolbarTools.toggled.connect(lambda checked: self._toolbarTools.setVisible(checked))

        self._actionToolbarView = QAction(self.tr('Show View Toolbar'), self)
        self._actionToolbarView.setObjectName('actionToolbarView')
        self._actionToolbarView.setCheckable(True)
        self._actionToolbarView.setToolTip(self.tr('Display the View toolbar'))
        self._actionToolbarView.toggled.connect(lambda checked: self._toolbarView.setVisible(checked))

        self._actionToolbarHelp = QAction(self.tr('Show Help Toolbar'), self)
        self._actionToolbarHelp.setObjectName('actionToolbarHelp')
        self._actionToolbarHelp.setCheckable(True)
        self._actionToolbarHelp.setToolTip(self.tr('Display the Help toolbar'))
        self._actionToolbarHelp.toggled.connect(lambda checked: self._toolbarHelp.setVisible(checked))

        # Actions: Help

        self._actionKeyboardShortcuts = QAction(self.tr('Keyboard Shortcuts'), self)
        self._actionKeyboardShortcuts.setObjectName('actionKeyboardShortcuts')
        self._actionKeyboardShortcuts.setIcon(QIcon.fromTheme('help-keyboard-shortcuts', QIcon(':/icons/actions/16/help-keyboard-shortcuts.svg')))
        self._actionKeyboardShortcuts.setIconText(self.tr('Shortcuts'))
        self._actionKeyboardShortcuts.setToolTip(self.tr('List of all keyboard shortcuts'))
        self._actionKeyboardShortcuts.triggered.connect(self._onActionKeyboardShortcutsTriggered)


    def _createMenus(self):

        # Menu: Application
        menuApplication = self.menuBar().addMenu(self.tr('Application'))
        menuApplication.setObjectName('menuApplication')
        menuApplication.addAction(self._actionAbout)
        menuApplication.addAction(self._actionColophon)
        menuApplication.addSeparator()
        menuApplication.addAction(self._actionPreferences)
        menuApplication.addSeparator()
        menuApplication.addAction(self._actionQuit)

        # Menu: Document
        self._menuOpenRecent = QMenu(self.tr('Open Recent'), self)
        self._menuOpenRecent.setObjectName('menuOpenRecent')
        self._menuOpenRecent.setIcon(QIcon.fromTheme('document-open-recent', QIcon(':/icons/actions/16/document-open-recent.svg')))
        self._menuOpenRecent.setToolTip('Open a document which was recently opened')

        self._menuSaveAsDelimiter = QMenu(self.tr('Save As with Delimiter…'), self)
        self._menuSaveAsDelimiter.setObjectName('menuSaveAsDelimiter')
        self._menuSaveAsDelimiter.setIcon(QIcon.fromTheme('document-save-as', QIcon(':/icons/actions/16/document-save-as.svg')))
        self._menuSaveAsDelimiter.setToolTip(self.tr('Save document with specific delimiter under a new name'))
        self._menuSaveAsDelimiter.addActions(self._actionSaveAsDelimiter.actions())

        menuDocument = self.menuBar().addMenu(self.tr('Document'))
        menuDocument.setObjectName('menuDocument')
        menuDocument.addAction(self._actionNew)
        menuDocument.addSeparator()
        menuDocument.addAction(self._actionOpen)
        menuDocument.addMenu(self._menuOpenRecent)
        menuDocument.addSeparator()
        menuDocument.addAction(self._actionSave)
        menuDocument.addAction(self._actionSaveAs)
        menuDocument.addMenu(self._menuSaveAsDelimiter)
        menuDocument.addAction(self._actionSaveCopyAs)
        menuDocument.addAction(self._actionSaveAll)
        menuDocument.addSeparator()
        menuDocument.addAction(self._actionClose)
        menuDocument.addAction(self._actionCloseOther)
        menuDocument.addAction(self._actionCloseAll)

        # Menu: Edit
        menuEdit = self.menuBar().addMenu(self.tr('Edit'))
        menuEdit.setObjectName('menuEdit')

        # Menu: Tools
        menuTools = self.menuBar().addMenu(self.tr('Tools'))
        menuTools.setObjectName('menuTools')

        # Menu: View
        menuView = self.menuBar().addMenu(self.tr('View'))
        menuView.setObjectName('menuView')
        menuView.addAction(self._actionFullScreen)
        menuView.addSeparator()
        menuView.addAction(self._actionTitlebarFullPath)
        menuView.addSeparator()
        menuView.addAction(self._actionToolbarApplication)
        menuView.addAction(self._actionToolbarDocument)
        menuView.addAction(self._actionToolbarEdit)
        menuView.addAction(self._actionToolbarTools)
        menuView.addAction(self._actionToolbarView)
        menuView.addAction(self._actionToolbarHelp)

        # Menu: Help
        menuHelp = self.menuBar().addMenu(self.tr('Help'))
        menuHelp.setObjectName('menuHelp')
        menuHelp.addAction(self._actionKeyboardShortcuts)


    def _createToolBars(self):

        # Toolbar: Application
        self._toolbarApplication = self.addToolBar(self.tr('Application Toolbar'))
        self._toolbarApplication.setObjectName('toolbarApplication')
        self._toolbarApplication.addAction(self._actionAbout)
        self._toolbarApplication.addAction(self._actionPreferences)
        self._toolbarApplication.addSeparator()
        self._toolbarApplication.addAction(self._actionQuit)
        self._toolbarApplication.visibilityChanged.connect(lambda visible: self._actionToolbarApplication.setChecked(visible))

        # Toolbar: Document
        self._toolbarDocument = self.addToolBar(self.tr('Document Toolbar'))
        self._toolbarDocument.setObjectName('toolbarDocument')
        self._toolbarDocument.addAction(self._actionNew)
        self._toolbarDocument.addAction(self._actionOpen)
        self._toolbarDocument.addSeparator()
        self._toolbarDocument.addAction(self._actionSave)
        self._toolbarDocument.addAction(self._actionSaveAs)
        self._toolbarDocument.addSeparator()
        self._toolbarDocument.addAction(self._actionClose)
        self._toolbarDocument.visibilityChanged.connect(lambda visible: self._actionToolbarDocument.setChecked(visible))

        # Toolbar: Edit
        self._toolbarEdit = self.addToolBar(self.tr('Edit Toolbar'))
        self._toolbarEdit.setObjectName('toolbarEdit')
        self._toolbarEdit.visibilityChanged.connect(lambda visible: self._actionToolbarEdit.setChecked(visible))

        # Toolbar: Tools
        self._toolbarTools = self.addToolBar(self.tr('Tools Toolbar'))
        self._toolbarTools.setObjectName('toolbarTools')
        self._toolbarTools.visibilityChanged.connect(lambda visible: self._actionToolbarTools.setChecked(visible))

        # Toolbar: View
        self._toolbarView = self.addToolBar(self.tr('View Toolbar'))
        self._toolbarView.setObjectName('toolbarView')
        self._toolbarView.addAction(self._actionFullScreen)
        self._toolbarView.visibilityChanged.connect(lambda visible: self._actionToolbarView.setChecked(visible))

        # Toolbar: Help
        self._toolbarHelp = self.addToolBar(self.tr('Help Toolbar'))
        self._toolbarHelp.setObjectName('toolbarHelp')
        self._toolbarHelp.addAction(self._actionKeyboardShortcuts)
        self._toolbarHelp.visibilityChanged.connect(lambda visible: self._actionToolbarHelp.setChecked(visible))


    def _updateActions(self, subWindowCount=0):

        hasDocument = subWindowCount >= 1
        hasDocuments = subWindowCount >= 2

        # Actions: Document
        self._actionSave.setEnabled(hasDocument)
        self._actionSaveAs.setEnabled(hasDocument)
        self._menuSaveAsDelimiter.setEnabled(hasDocument)
        self._actionSaveCopyAs.setEnabled(hasDocument)
        self._actionSaveAll.setEnabled(hasDocument)
        self._actionClose.setEnabled(hasDocument)
        self._actionCloseOther.setEnabled(hasDocuments)
        self._actionCloseAll.setEnabled(hasDocument)


    def _updateActionFullScreen(self):

        if not self.isFullScreen():
            self._actionFullScreen.setText(self.tr('Full Screen Mode'))
            self._actionFullScreen.setIcon(QIcon.fromTheme('view-fullscreen', QIcon(':/icons/actions/16/view-fullscreen.svg')))
            self._actionFullScreen.setChecked(False)
            self._actionFullScreen.setToolTip(self.tr('Display the window in full screen'))
        else:
            self._actionFullScreen.setText(self.tr('Exit Full Screen Mode'))
            self._actionFullScreen.setIcon(QIcon.fromTheme('view-restore', QIcon(':/icons/actions/16/view-restore.svg')))
            self._actionFullScreen.setChecked(True)
            self._actionFullScreen.setToolTip(self.tr('Exit the full screen mode'))


    def _updateActionRecentDocuments(self):

        # Add items to the list, if necessary
        for idx in range(len(self._actionRecentDocuments)+1, self._preferences.maximumRecentDocuments()+1):

            actionRecentDocument = QAction(self)
            actionRecentDocument.setObjectName(f'actionRecentDocument_{idx}')
            actionRecentDocument.triggered.connect(lambda data=actionRecentDocument.data(): self._onActionOpenRecentDocumentTriggered(data))

            self._actionRecentDocuments.append(actionRecentDocument)

        # Remove items from the list, if necessary
        while len(self._actionRecentDocuments) > self._preferences.maximumRecentDocuments():
            self._actionRecentDocuments.pop()

        # Update items
        for idx in range(len(self._actionRecentDocuments)):
            text = None
            data = None
            show = False

            if idx < len(self._recentDocuments):
                text = self.tr(f'{QFileInfo(self._recentDocuments[idx]).fileName()} [{self._recentDocuments[idx]}]')
                data = self._recentDocuments[idx]
                show = True

            self._actionRecentDocuments[idx].setText(text)
            self._actionRecentDocuments[idx].setData(data)
            self._actionRecentDocuments[idx].setVisible(show)


    def _updateMenuOpenRecent(self):

        self._menuOpenRecent.clear()

        if self._preferences.maximumRecentDocuments() > 0:
            # Document list wanted; show the menu
            self._menuOpenRecent.menuAction().setVisible(True)

            if len(self._recentDocuments) > 0:
                # Document list has items; enable the menu
                self._menuOpenRecent.setEnabled(True)

                self._menuOpenRecent.addActions(self._actionRecentDocuments)
                self._menuOpenRecent.addSeparator()
                self._menuOpenRecent.addAction(self._actionOpenRecentClear)
            else:
                # Document list is empty; disable the menu
                self._menuOpenRecent.setEnabled(False)
        else:
            # No document list wanted; hide the menu
            self._menuOpenRecent.menuAction().setVisible(False)


    def _updateTitleBar(self):

        title = None

        document = self._activeDocument()
        if document:
            title = document.canonicalName() if self._actionTitlebarFullPath.isChecked() and document.canonicalName() else document.documentTitle()

        self.setWindowTitle(title)


    def _onActionAboutTriggered(self):

        dialog = AboutDialog(self)
        dialog.exec_()


    def _onActionColophonTriggered(self):

        dialog = ColophonDialog(self)
        dialog.exec_()


    def _onActionPreferencesTriggered(self):

        dialog = PreferencesDialog(self)
        dialog.setPreferences(self._preferences)
        dialog.exec_()

        self._preferences = dialog.preferences()

        self._updateRecentDocuments(None)
        self._updateMenuOpenRecent()


    def _onActionNewTriggered(self):

        self._loadDocument('')


    def _onActionOpenTriggered(self):

        fileNames = QFileDialog.getOpenFileNames(self, self.tr('Open Document'),
                        QStandardPaths.writableLocation(QStandardPaths.HomeLocation),
                        self.tr('CSV Files (*.csv);;All Files (*.*)'))[0]

        for fileName in fileNames:
            self._openDocument(fileName)


    def _onActionOpenRecentDocumentTriggered(self, canonicalName):
        pass

#        self.openDocument(canonicalName)


    def _onActionOpenRecentClearTriggered(self):

        self._recentDocuments.clear()

        self._updateRecentDocuments(None)
        self._updateMenuOpenRecent()


    def _onActionSaveTriggered(self):
        pass


    def _onActionSaveAsTriggered(self):
        pass


    def _onActionSaveAsDelimiterTriggered(self, delimiter):
        pass


    def _onActionSaveCopyAsTriggered(self):
        pass


    def _onActionSaveAllTriggered(self):
        pass


    def _onActionCloseTriggered(self):

        self._documentArea.closeActiveSubWindow()


    def _onActionCloseOtherTriggered(self):

        for subWindow in self._documentArea.subWindowList():
            if subWindow != self._documentArea.activeSubWindow():
                subWindow.close()


    def _onActionCloseAllTriggered(self):

        self._documentArea.closeAllSubWindows()


    def _onActionFullScreenTriggered(self):

        if not self.isFullScreen():
            self.setWindowState(self.windowState() | Qt.WindowFullScreen)
        else:
            self.setWindowState(self.windowState() & ~Qt.WindowFullScreen)

        self._updateActionFullScreen()


    def _onActionTitlebarFullPathTriggered(self):

        self._updateTitleBar()


    def _onActionKeyboardShortcutsTriggered(self):

        if not self._keyboardShortcutsDialog:
            self._keyboardShortcutsDialog = KeyboardShortcutsDialog(self)

        self._keyboardShortcutsDialog.show()
        self._keyboardShortcutsDialog.raise_()
        self._keyboardShortcutsDialog.activateWindow()


    def _onDocumentWindowActivated(self, subWindow):

        # Update the application window
        self._updateActions(len(self._documentArea.subWindowList()))
        self._updateTitleBar()

        if not subWindow:
            return


    def _onDocumentAboutToClose(self, canonicalName):

        # Workaround to show subwindows always maximized
        for subWindow in self._documentArea.subWindowList():
            if not subWindow.isMaximized():
                subWindow.showMaximized()

        # Update menu items without the emitter
        self._updateActions(len(self._documentArea.subWindowList()) - 1)


    def _createDocument(self):

        document = Document()
        document.setPreferences(self._preferences)
        document.aboutToClose.connect(self._onDocumentAboutToClose)

        subWindow = self._documentArea.addSubWindow(document)
        subWindow.setWindowIcon(QIcon())
        subWindow.showMaximized()

        return document


    def _createDocumentIndex(self, canonicalName):

        fileName = QFileInfo(canonicalName).fileName()
        canonicalIndex = 0

        for subWindow in self._documentArea.subWindowList():
            if QFileInfo(subWindow.widget().canonicalName()).fileName() == fileName:
                if subWindow.widget().canonicalIndex() > canonicalIndex:
                    canonicalIndex = subWindow.widget().canonicalIndex()

        return canonicalIndex + 1


    def _findDocumentWindow(self, canonicalName):

        for subWindow in self._documentArea.subWindowList():
            if subWindow.widget().canonicalName() == canonicalName:
                return subWindow

        return None


    def _activeDocument(self):

        subWindow = self._documentArea.activeSubWindow()

        return subWindow.widget() if subWindow else None


    def _openDocument(self, fileName):

        canonicalName = QFileInfo(fileName).canonicalFilePath()

        subWindow = self._findDocumentWindow(canonicalName)
        if subWindow:
            # Given document is already loaded; activate the subwindow
            self._documentArea.setActiveSubWindow(subWindow)

            # Update list of recent documents
            self._updateRecentDocuments(canonicalName)
            self._updateMenuOpenRecent()
            return True

        return self._loadDocument(canonicalName);


    def _loadDocument(self, canonicalName):

        document = self._createDocument()

        succeeded = document.load(canonicalName)
        if succeeded:
            document.setCanonicalIndex(self._createDocumentIndex(canonicalName))
            document.updateDocumentTitle()
            document.show()

            # Update list of recent documents
            self._updateRecentDocuments(canonicalName)
            self._updateMenuOpenRecent()

            # Update the application window
            self._updateActions(len(self._documentArea.subWindowList()))
            self._updateTitleBar()
        else:
            document.close()

        return succeeded


    def _updateRecentDocuments(self, canonicalName):

        if canonicalName:
            while canonicalName in self._recentDocuments:
                self._recentDocuments.remove(canonicalName)
            self._recentDocuments.insert(0, canonicalName)

        # Remove items from the list, if necessary
        while len(self._recentDocuments) > self._preferences.maximumRecentDocuments():
            self._recentDocuments.pop()

        self._updateActionRecentDocuments()
