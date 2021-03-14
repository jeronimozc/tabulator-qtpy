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
from PySide2.QtWidgets import QAction, QApplication, QFileDialog, QMainWindow, QMdiArea, QMenu

from about_dialog import AboutDialog
from colophon_dialog import ColophonDialog
from document import Document
from keyboard_shortcuts_dialog import KeyboardShortcutsDialog
from preferences import Preferences
from preferences_dialog import PreferencesDialog

import icons


class MainWindow(QMainWindow):

    _preferences = Preferences()


    def __init__(self, parent=None):
        super().__init__(parent)

        self.recentDocuments = []
        self.actionRecentDocuments = []
        self.keyboardShortcutsDialog = None

        self.setWindowIcon(QIcon(':/icons/apps/16/tabulator.svg'))

        self.loadSettings()

        self.createActions()
        self.createMenus()
        self.createToolBars()

        # Application properties
        self.setApplicationState(self._applicationState)
        self.setApplicationGeometry(self._applicationGeometry)

        self.updateActionFullScreen()
        self.updateMenus()
        self.updateMenuOpenRecent()

        # Central widget
        self._documentArea = QMdiArea()
        self._documentArea.setViewMode(QMdiArea.TabbedView)
        self._documentArea.setTabsMovable(True)
        self._documentArea.setTabsClosable(True)
        self.setCentralWidget(self._documentArea)
        self._documentArea.subWindowActivated.connect(self.onDocumentWindowActivated)


    def setApplicationState(self, state=QByteArray()):

        if not state.isEmpty():
            self.restoreState(state)
        else:
            self.toolbarApplication.setVisible(True)
            self.toolbarDocument.setVisible(True)
            self.toolbarEdit.setVisible(True)
            self.toolbarTools.setVisible(True)
            self.toolbarView.setVisible(False)
            self.toolbarHelp.setVisible(False)


    def applicationState(self):

        return self.saveState()


    def setApplicationGeometry(self, geometry=QByteArray()):

        if not geometry.isEmpty():
            self.restoreGeometry(geometry)
        else:
            availableGeometry = self.screen().availableGeometry()
            self.resize(availableGeometry.width() * 2/3, availableGeometry.height() * 2/3)
            self.move((availableGeometry.width() - self.width()) / 2, (availableGeometry.height() - self.height()) / 2)


    def applicationGeometry(self):

        return self.saveGeometry()


    def closeEvent(self, event):

        if True:
            # Recent documents
            if not self._preferences.restoreRecentDocuments():
                 self.recentDocuments.clear()

            # Application properties
            self._applicationState = self.applicationState() if self._preferences.restoreApplicationState() else QByteArray()
            self._applicationGeometry = self.applicationGeometry() if self._preferences.restoreApplicationGeometry() else QByteArray()

            self.saveSettings()
            event.accept()
        else:
            event.ignore()


    def loadSettings(self):

        settings = QSettings()

        # Preferences
        self._preferences.load(settings)

        # Recent documents
        size = settings.beginReadArray('RecentDocuments')
        for idx in range(size-1, -1, -1):
            settings.setArrayIndex(idx)
            canonicalName = QFileInfo(settings.value('Document')).canonicalFilePath()
            self.updateRecentDocuments(canonicalName)
        settings.endArray()

        # Application and dialog properties
        self._applicationState = settings.value('Application/State', QByteArray()) if self._preferences.restoreApplicationState() else QByteArray()
        self._applicationGeometry = settings.value('Application/Geometry', QByteArray()) if self._preferences.restoreApplicationGeometry() else QByteArray()
        self._aboutDialogGeometry = settings.value('AboutDialog/Geometry', QByteArray())
        self._colophonDialogGeometry = settings.value('ColophonDialog/Geometry', QByteArray())
        self._keyboardShortcutsDialogGeometry = settings.value('KeyboardShortcutsDialog/Geometry', QByteArray())
        self._preferencesDialogGeometry = settings.value('PreferencesDialog/Geometry', QByteArray())


    def saveSettings(self):

        settings = QSettings()

        # Preferences
        self._preferences.save(settings)

        # Recent documents
        settings.remove('RecentDocuments')
        settings.beginWriteArray('RecentDocuments')
        for idx in range(len(self.recentDocuments)):
            settings.setArrayIndex(idx)
            settings.setValue('Document', self.recentDocuments[idx])
        settings.endArray()

        # Application and dialog properties
        settings.setValue('Application/State', self._applicationState)
        settings.setValue('Application/Geometry', self._applicationGeometry)
        settings.setValue('AboutDialog/Geometry', self._aboutDialogGeometry)
        settings.setValue('ColophonDialog/Geometry', self._colophonDialogGeometry)
        settings.setValue('KeyboardShortcutsDialog/Geometry', self._keyboardShortcutsDialogGeometry)
        settings.setValue('PreferencesDialog/Geometry', self._preferencesDialogGeometry)


    def createActions(self):

        # Actions: Application
        self.actionAbout = QAction(self.tr(f'About {QApplication.applicationName()}'), self)
        self.actionAbout.setObjectName('actionAbout')
        self.actionAbout.setIcon(QIcon(':/icons/apps/16/tabulator.svg'))
        self.actionAbout.setIconText(self.tr('About'))
        self.actionAbout.setToolTip(self.tr('Brief description of the application'))
        self.actionAbout.triggered.connect(self.onActionAboutTriggered)

        self.actionColophon = QAction(self.tr('Colophon'), self)
        self.actionColophon.setObjectName('actionColophon')
        self.actionColophon.setToolTip(self.tr('Lengthy description of the application'))
        self.actionColophon.triggered.connect(self.onActionColophonTriggered)

        self.actionPreferences = QAction(self.tr('Preferences…'), self)
        self.actionPreferences.setObjectName('actionPreferences')
        self.actionPreferences.setIcon(QIcon.fromTheme('configure', QIcon(':/icons/actions/16/application-configure.svg')))
        self.actionPreferences.setIconText(self.tr('Preferences'))
        self.actionPreferences.setToolTip(self.tr('Customize the appearance and behavior of the application'))
        self.actionPreferences.triggered.connect(self.onActionPreferencesTriggered)

        self.actionQuit = QAction(self.tr('Quit'), self)
        self.actionQuit.setObjectName('actionQuit')
        self.actionQuit.setIcon(QIcon.fromTheme('application-exit', QIcon(':/icons/actions/16/application-exit.svg')))
        self.actionQuit.setIconText(self.tr('Quit'))
        self.actionQuit.setShortcut(QKeySequence.Quit)
        self.actionQuit.setToolTip(self.tr(f'Quit the application [{self.actionQuit.shortcut().toString(QKeySequence.NativeText)}]'))
        self.actionQuit.setData(self.tr('Quit the application'))
        self.actionQuit.triggered.connect(self.close)

        # Actions: Document
        self.actionNew = QAction(self.tr('New'), self)
        self.actionNew.setObjectName('actionNew')
        self.actionNew.setIcon(QIcon.fromTheme('document-new', QIcon(':/icons/actions/16/document-new.svg')))
        self.actionNew.setIconText(self.tr('New'))
        self.actionNew.setShortcut(QKeySequence.New)
        self.actionNew.setToolTip(self.tr(f'Create new document [{self.actionNew.shortcut().toString(QKeySequence.NativeText)}]'))
        self.actionNew.setData(self.tr('Create new document'))
        self.actionNew.triggered.connect(self.onActionNewTriggered)

        self.actionOpen = QAction(self.tr('Open…'), self)
        self.actionOpen.setObjectName('actionOpen')
        self.actionOpen.setIcon(QIcon.fromTheme('document-open', QIcon(':/icons/actions/16/document-open.svg')))
        self.actionOpen.setIconText(self.tr('Open'))
        self.actionOpen.setShortcut(QKeySequence.Open)
        self.actionOpen.setToolTip(self.tr(f'Open an existing document [{self.actionOpen.shortcut().toString(QKeySequence.NativeText)}]'))
        self.actionOpen.setData(self.tr('Open an existing document'))
        self.actionOpen.triggered.connect(self.onActionOpenTriggered)

        self.actionOpenRecentClear = QAction(self.tr('Clear List'), self)
        self.actionOpenRecentClear.setObjectName('actionOpenRecentClear')
        self.actionOpenRecentClear.setToolTip(self.tr('Clear document list'))
        self.actionOpenRecentClear.triggered.connect(self.onActionOpenRecentClearTriggered)

        self.actionClose = QAction(self.tr('Close'), self)
        self.actionClose.setObjectName('actionClose')
        self.actionClose.setIcon(QIcon.fromTheme('document-close', QIcon(':/icons/actions/16/document-close.svg')))
        self.actionClose.setShortcut(QKeySequence.Close)
        self.actionClose.setToolTip(f'Close document [{self.actionClose.shortcut().toString(QKeySequence.NativeText)}]')
        self.actionClose.triggered.connect(self.onActionCloseTriggered)

        self.actionCloseOther = QAction(self.tr('Close Other'), self)
        self.actionCloseOther.setObjectName('actionCloseOther')
        self.actionCloseOther.setToolTip('Close all other documents')
        self.actionCloseOther.triggered.connect(self.onActionCloseOtherTriggered)

        self.actionCloseAll = QAction(self.tr('Close All'), self)
        self.actionCloseAll.setObjectName('actionCloseAll')
        self.actionCloseAll.setShortcut(QKeySequence(Qt.CTRL + Qt.SHIFT + Qt.Key_W))
        self.actionCloseAll.setToolTip(f'Close all documents [{self.actionCloseAll.shortcut().toString(QKeySequence.NativeText)}]')
        self.actionCloseAll.triggered.connect(self.onActionCloseAllTriggered)

        # Actions: View
        self.actionFullScreen = QAction(self)
        self.actionFullScreen.setObjectName('actionFullScreen')
        self.actionFullScreen.setCheckable(True)
        self.actionFullScreen.setIconText(self.tr('Full Screen'))
        self.actionFullScreen.setShortcuts([QKeySequence(Qt.Key_F11), QKeySequence.FullScreen])
        self.actionFullScreen.setData(self.tr('Display the window in full screen'))
        self.actionFullScreen.triggered.connect(self.onActionFullScreenTriggered)

        self.actionTitlebarFullPath = QAction(self.tr('Show Path in Titlebar'), self)
        self.actionTitlebarFullPath.setObjectName('actionTitlebarFullPath')
        self.actionTitlebarFullPath.setCheckable(True)
        self.actionTitlebarFullPath.setChecked(True)
        self.actionTitlebarFullPath.setToolTip(self.tr('Display the full path of the document in the titlebar'))
        self.actionTitlebarFullPath.triggered.connect(self.onActionTitlebarFullPathTriggered)

        self.actionToolbarApplication = QAction(self.tr('Show Application Toolbar'), self)
        self.actionToolbarApplication.setObjectName('actionToolbarApplication')
        self.actionToolbarApplication.setCheckable(True)
        self.actionToolbarApplication.setToolTip(self.tr('Display the Application toolbar'))
        self.actionToolbarApplication.toggled.connect(lambda checked: self.toolbarApplication.setVisible(checked))

        self.actionToolbarDocument = QAction(self.tr('Show Document Toolbar'), self)
        self.actionToolbarDocument.setObjectName('actionToolbarDocument')
        self.actionToolbarDocument.setCheckable(True)
        self.actionToolbarDocument.setToolTip(self.tr('Display the Document toolbar'))
        self.actionToolbarDocument.toggled.connect(lambda checked: self.toolbarDocument.setVisible(checked))

        self.actionToolbarEdit = QAction(self.tr('Show Edit Toolbar'), self)
        self.actionToolbarEdit.setObjectName('actionToolbarEdit')
        self.actionToolbarEdit.setCheckable(True)
        self.actionToolbarEdit.setToolTip(self.tr('Display the Edit toolbar'))
        self.actionToolbarEdit.toggled.connect(lambda checked: self.toolbarEdit.setVisible(checked))

        self.actionToolbarTools = QAction(self.tr('Show Tools Toolbar'), self)
        self.actionToolbarTools.setObjectName('actionToolbarTools')
        self.actionToolbarTools.setCheckable(True)
        self.actionToolbarTools.setToolTip(self.tr('Display the Tools toolbar'))
        self.actionToolbarTools.toggled.connect(lambda checked: self.toolbarTools.setVisible(checked))

        self.actionToolbarView = QAction(self.tr('Show View Toolbar'), self)
        self.actionToolbarView.setObjectName('actionToolbarView')
        self.actionToolbarView.setCheckable(True)
        self.actionToolbarView.setToolTip(self.tr('Display the View toolbar'))
        self.actionToolbarView.toggled.connect(lambda checked: self.toolbarView.setVisible(checked))

        self.actionToolbarHelp = QAction(self.tr('Show Help Toolbar'), self)
        self.actionToolbarHelp.setObjectName('actionToolbarHelp')
        self.actionToolbarHelp.setCheckable(True)
        self.actionToolbarHelp.setToolTip(self.tr('Display the Help toolbar'))
        self.actionToolbarHelp.toggled.connect(lambda checked: self.toolbarHelp.setVisible(checked))

        # Actions: Help
        self.actionKeyboardShortcuts = QAction(self.tr('Keyboard Shortcuts'), self)
        self.actionKeyboardShortcuts.setObjectName('actionKeyboardShortcuts')
        self.actionKeyboardShortcuts.setIcon(QIcon.fromTheme('help-keyboard-shortcuts', QIcon(':/icons/actions/16/help-keyboard-shortcuts.svg')))
        self.actionKeyboardShortcuts.setIconText(self.tr('Shortcuts'))
        self.actionKeyboardShortcuts.setToolTip(self.tr('List of all keyboard shortcuts'))
        self.actionKeyboardShortcuts.triggered.connect(self.onActionKeyboardShortcutsTriggered)


    def createMenus(self):

        # Menu: Application
        menuApplication = self.menuBar().addMenu(self.tr('Application'))
        menuApplication.setObjectName('menuApplication')
        menuApplication.addAction(self.actionAbout)
        menuApplication.addAction(self.actionColophon)
        menuApplication.addSeparator()
        menuApplication.addAction(self.actionPreferences)
        menuApplication.addSeparator()
        menuApplication.addAction(self.actionQuit)

        # Menu: Document
        self.menuOpenRecent = QMenu(self.tr('Open Recent'), self)
        self.menuOpenRecent.setObjectName('menuOpenRecent')
        self.menuOpenRecent.setIcon(QIcon.fromTheme('document-open-recent', QIcon(':/icons/actions/16/document-open-recent.svg')))
        self.menuOpenRecent.setToolTip('Open a document which was recently opened')

        menuDocument = self.menuBar().addMenu(self.tr('Document'))
        menuDocument.setObjectName('menuDocument')
        menuDocument.addAction(self.actionNew)
        menuDocument.addSeparator()
        menuDocument.addAction(self.actionOpen)
        menuDocument.addMenu(self.menuOpenRecent)
        menuDocument.addSeparator()
        menuDocument.addAction(self.actionClose)
        menuDocument.addAction(self.actionCloseOther)
        menuDocument.addAction(self.actionCloseAll)

        # Menu: Edit
        menuEdit = self.menuBar().addMenu(self.tr('Edit'))
        menuEdit.setObjectName('menuEdit')

        # Menu: Tools
        menuTools = self.menuBar().addMenu(self.tr('Tools'))
        menuTools.setObjectName('menuTools')

        # Menu: View
        menuView = self.menuBar().addMenu(self.tr('View'))
        menuView.setObjectName('menuView')
        menuView.addAction(self.actionFullScreen)
        menuView.addSeparator()
        menuView.addAction(self.actionTitlebarFullPath)
        menuView.addSeparator()
        menuView.addAction(self.actionToolbarApplication)
        menuView.addAction(self.actionToolbarDocument)
        menuView.addAction(self.actionToolbarEdit)
        menuView.addAction(self.actionToolbarTools)
        menuView.addAction(self.actionToolbarView)
        menuView.addAction(self.actionToolbarHelp)

        # Menu: Help
        menuHelp = self.menuBar().addMenu(self.tr('Help'))
        menuHelp.setObjectName('menuHelp')
        menuHelp.addAction(self.actionKeyboardShortcuts)


    def createToolBars(self):

        # Toolbar: Application
        self.toolbarApplication = self.addToolBar(self.tr('Application Toolbar'))
        self.toolbarApplication.setObjectName('toolbarApplication')
        self.toolbarApplication.addAction(self.actionAbout)
        self.toolbarApplication.addAction(self.actionPreferences)
        self.toolbarApplication.addSeparator()
        self.toolbarApplication.addAction(self.actionQuit)
        self.toolbarApplication.visibilityChanged.connect(lambda visible: self.actionToolbarApplication.setChecked(visible))

        # Toolbar: Document
        self.toolbarDocument = self.addToolBar(self.tr('Document Toolbar'))
        self.toolbarDocument.setObjectName('toolbarDocument')
        self.toolbarDocument.addAction(self.actionNew)
        self.toolbarDocument.addAction(self.actionOpen)
        self.toolbarDocument.addSeparator()
        self.toolbarDocument.addAction(self.actionClose)
        self.toolbarDocument.visibilityChanged.connect(lambda visible: self.actionToolbarDocument.setChecked(visible))

        # Toolbar: Edit
        self.toolbarEdit = self.addToolBar(self.tr('Edit Toolbar'))
        self.toolbarEdit.setObjectName('toolbarEdit')
        self.toolbarEdit.visibilityChanged.connect(lambda visible: self.actionToolbarEdit.setChecked(visible))

        # Toolbar: Tools
        self.toolbarTools = self.addToolBar(self.tr('Tools Toolbar'))
        self.toolbarTools.setObjectName('toolbarTools')
        self.toolbarTools.visibilityChanged.connect(lambda visible: self.actionToolbarTools.setChecked(visible))

        # Toolbar: View
        self.toolbarView = self.addToolBar(self.tr('View Toolbar'))
        self.toolbarView.setObjectName('toolbarView')
        self.toolbarView.addAction(self.actionFullScreen)
        self.toolbarView.visibilityChanged.connect(lambda visible: self.actionToolbarView.setChecked(visible))

        # Toolbar: Help
        self.toolbarHelp = self.addToolBar(self.tr('Help Toolbar'))
        self.toolbarHelp.setObjectName('toolbarHelp')
        self.toolbarHelp.addAction(self.actionKeyboardShortcuts)
        self.toolbarHelp.visibilityChanged.connect(lambda visible: self.actionToolbarHelp.setChecked(visible))


    def updateActionFullScreen(self):

        if not self.isFullScreen():
            self.actionFullScreen.setText(self.tr('Full Screen Mode'))
            self.actionFullScreen.setIcon(QIcon.fromTheme('view-fullscreen', QIcon(':/icons/actions/16/view-fullscreen.svg')))
            self.actionFullScreen.setChecked(False)
            self.actionFullScreen.setToolTip(self.tr(f'Display the window in full screen [{self.actionFullScreen.shortcut().toString(QKeySequence.NativeText)}]'))
        else:
            self.actionFullScreen.setText(self.tr('Exit Full Screen Mode'))
            self.actionFullScreen.setIcon(QIcon.fromTheme('view-restore', QIcon(':/icons/actions/16/view-restore.svg')))
            self.actionFullScreen.setChecked(True)
            self.actionFullScreen.setToolTip(self.tr(f'Exit the full screen mode [{self.actionFullScreen.shortcut().toString(QKeySequence.NativeText)}]'))


    def updateActionRecentDocuments(self):

        # Add items to the list, if necessary
        for idx in range(len(self.actionRecentDocuments)+1, self._preferences.maximumRecentDocuments()+1):

            actionRecentDocument = QAction(self)
            actionRecentDocument.setObjectName(f'actionRecentDocument_{idx}')
            actionRecentDocument.triggered.connect(lambda data=actionRecentDocument.data(): self.onActionOpenRecentDocumentTriggered(data))

            self.actionRecentDocuments.append(actionRecentDocument)

        # Remove items from the list, if necessary
        while len(self.actionRecentDocuments) > self._preferences.maximumRecentDocuments():
            self.actionRecentDocuments.pop()

        # Update items
        for idx in range(len(self.actionRecentDocuments)):
            text = None
            data = None
            show = False

            if idx < len(self.recentDocuments):
                text = self.tr(f'{QFileInfo(self.recentDocuments[idx]).fileName()} [{self.recentDocuments[idx]}]')
                data = self.recentDocuments[idx]
                show = True

            self.actionRecentDocuments[idx].setText(text)
            self.actionRecentDocuments[idx].setData(data)
            self.actionRecentDocuments[idx].setVisible(show)


    def updateMenus(self, cntWindows=0):

        hasDocument = cntWindows >= 1
        hasDocuments = cntWindows >= 2

        self.actionClose.setEnabled(hasDocument)
        self.actionCloseOther.setEnabled(hasDocuments)
        self.actionCloseAll.setEnabled(hasDocument)


    def updateMenuOpenRecent(self):

        self.menuOpenRecent.clear()

        if self._preferences.maximumRecentDocuments() > 0:
            # Document list wanted; show the menu
            self.menuOpenRecent.menuAction().setVisible(True)

            if len(self.recentDocuments) > 0:
                # Document list has items; enable the menu
                self.menuOpenRecent.setEnabled(True)

                self.menuOpenRecent.addActions(self.actionRecentDocuments)
                self.menuOpenRecent.addSeparator()
                self.menuOpenRecent.addAction(self.actionOpenRecentClear)
            else:
                # Document list is empty; disable the menu
                self.menuOpenRecent.setEnabled(False)
        else:
            # No document list wanted; hide the menu
            self.menuOpenRecent.menuAction().setVisible(False)


    def updateTitleBar(self):

        title = None

        document = self.activeDocument()
        if document:
            title = document.canonicalName() if self.actionTitlebarFullPath.isChecked() and document.canonicalName() else document.documentTitle()

        self.setWindowTitle(title)


    def onActionAboutTriggered(self):

        geometry = self._aboutDialogGeometry if self._preferences.restoreDialogGeometry() else QByteArray()

        dialog = AboutDialog(self)
        dialog.setDialogGeometry(geometry)
        dialog.exec_()

        self._aboutDialogGeometry = dialog.dialogGeometry() if self._preferences.restoreDialogGeometry() else QByteArray()


    def onActionColophonTriggered(self):

        geometry = self._colophonDialogGeometry if self._preferences.restoreDialogGeometry() else QByteArray()

        dialog = ColophonDialog(self)
        dialog.setDialogGeometry(geometry)
        dialog.exec_()

        self._colophonDialogGeometry = dialog.dialogGeometry() if self._preferences.restoreDialogGeometry() else QByteArray()


    def onActionPreferencesTriggered(self):

        geometry = self._preferencesDialogGeometry if self._preferences.restoreDialogGeometry() else QByteArray()

        dialog = PreferencesDialog(self)
        dialog.setDialogGeometry(geometry)
        dialog.setPreferences(self._preferences)
        dialog.exec_()

        self._preferences = dialog.preferences()
        self._preferencesDialogGeometry = dialog.dialogGeometry() if self._preferences.restoreDialogGeometry() else QByteArray()

        self.updateRecentDocuments(None)
        self.updateMenuOpenRecent()


    def onActionNewTriggered(self):

        self.loadDocument('')


    def onActionOpenTriggered(self):

        fileNames = QFileDialog.getOpenFileNames(self, self.tr('Open Document'),
                        QStandardPaths.writableLocation(QStandardPaths.HomeLocation),
                        self.tr('CSV Files (*.csv);;All Files (*.*)'))[0]

        for fileName in fileNames:
            self.openDocument(fileName)


    def onActionOpenRecentDocumentTriggered(self, canonicalName):
        pass

#        self.openDocument(canonicalName)


    def onActionOpenRecentClearTriggered(self):

        self.recentDocuments.clear()

        self.updateRecentDocuments(None)
        self.updateMenuOpenRecent()


    def onActionCloseTriggered(self):

        self._documentArea.closeActiveSubWindow()


    def onActionCloseOtherTriggered(self):

        for window in self._documentArea.subWindowList():
            if window != self._documentArea.activeSubWindow():
                window.close()


    def onActionCloseAllTriggered(self):

        self._documentArea.closeAllSubWindows()


    def onActionFullScreenTriggered(self):

        if not self.isFullScreen():
            self.setWindowState(self.windowState() | Qt.WindowFullScreen)
        else:
            self.setWindowState(self.windowState() & ~Qt.WindowFullScreen)

        self.updateActionFullScreen()


    def onActionTitlebarFullPathTriggered(self):

        self.updateTitleBar()


    def onActionKeyboardShortcutsTriggered(self):

        if not self.keyboardShortcutsDialog:
            geometry = self._keyboardShortcutsDialogGeometry if self._preferences.restoreDialogGeometry() else QByteArray()

            self.keyboardShortcutsDialog = KeyboardShortcutsDialog(self)
            self.keyboardShortcutsDialog.setDialogGeometry(geometry)
            self.keyboardShortcutsDialog.finished.connect(self.onDialogKeyboardShortcutsFinished)

        self.keyboardShortcutsDialog.show()
        self.keyboardShortcutsDialog.raise_()
        self.keyboardShortcutsDialog.activateWindow()


    def onDialogKeyboardShortcutsFinished(self):

        self._keyboardShortcutsDialogGeometry = self.keyboardShortcutsDialog.dialogGeometry() if self._preferences.restoreDialogGeometry() else QByteArray()
        self.keyboardShortcutsDialog = None


    def onDocumentWindowActivated(self, window):

        self.updateTitleBar()
        self.updateMenus(len(self._documentArea.subWindowList()))

        if not window:
            return


    def onDocumentAboutToClose(self, canonicalName):

        # Update menu items but first delete the emitter from the list
        self.updateMenus(len(self._documentArea.subWindowList())-1)


    def createDocument(self):

        document = Document(self)
        document.setPreferences(self._preferences)
        document.aboutToClose.connect(self.onDocumentAboutToClose)

        window = self._documentArea.addSubWindow(document)
        window.setWindowIcon(QIcon())
        window.showMaximized()

        return document


    def createDocumentIndex(self, canonicalName):

        fileName = QFileInfo(canonicalName).fileName()
        canonicalIndex = 0

        for window in self._documentArea.subWindowList():
            if QFileInfo(window.widget().canonicalName()).fileName() == fileName:
                if window.widget().canonicalIndex() > canonicalIndex:
                    canonicalIndex = window.widget().canonicalIndex()

        return canonicalIndex+1


    def findDocumentWindow(self, canonicalName):

        for window in self._documentArea.subWindowList():
            if window.widget().canonicalName() == canonicalName:
                return window

        return None


    def activeDocument(self):

        window = self._documentArea.activeSubWindow()

        return window.widget() if window else None


    def openDocument(self, fileName):

        canonicalName = QFileInfo(fileName).canonicalFilePath()

        window = self.findDocumentWindow(canonicalName)
        if window:
            # Given document is already open; activate the window
            self._documentArea.setActiveSubWindow(window)

            self.updateRecentDocuments(canonicalName)
            self.updateMenuOpenRecent()
            return True

        return self.loadDocument(canonicalName);


    def loadDocument(self, canonicalName):

        document = self.createDocument()

        succeeded = document.load(canonicalName)
        if succeeded:
            document.setCanonicalIndex(self.createDocumentIndex(canonicalName))
            document.updateDocumentTitle()
            document.show()

            # Update list of recent documents
            self.updateRecentDocuments(canonicalName)
            self.updateMenuOpenRecent()

            # Update application
            self.updateTitleBar()
            self.updateMenus(len(self._documentArea.subWindowList()))
        else:
            document.close()

        return succeeded


    def updateRecentDocuments(self, canonicalName):

        if canonicalName:
            while canonicalName in self.recentDocuments:
                self.recentDocuments.remove(canonicalName)
            self.recentDocuments.insert(0, canonicalName)

        # Remove items from the list, if necessary
        while len(self.recentDocuments) > self._preferences.maximumRecentDocuments():
            self.recentDocuments.pop()

        self.updateActionRecentDocuments()
