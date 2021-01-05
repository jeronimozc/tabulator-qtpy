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

from PySide2.QtCore import QByteArray, QFileInfo, QRect, QSettings, QStandardPaths, Qt
from PySide2.QtGui import QIcon, QKeySequence
from PySide2.QtWidgets import QAction, QApplication, QFileDialog, QMainWindow, QMdiArea, QMenu

from about_dialog import AboutDialog
from colophon_dialog import ColophonDialog
from document_table import DocumentTable
from keyboard_shortcuts_dialog import KeyboardShortcutsDialog
from preferences_dialog import PreferencesDialog
from settings import Settings

import resources


class MainWindow(QMainWindow):

    _settings = Settings()


    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowIcon(QIcon(':/icons/apps/16/tabulator.svg'))

        self.createActions()
        self.createMenus()
        self.createToolbars()

        self.readSettings()

        self.updateActionFullScreen()
        self.updateMenuOpenRecent()

        # Central widget
        self.documentArea = QMdiArea()
        self.documentArea.setViewMode(QMdiArea.TabbedView)
        self.documentArea.setTabsMovable(True)
        self.documentArea.setTabsClosable(True)
        self.setCentralWidget(self.documentArea)


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
        self.actionColophon.setIconText(self.tr('Colophon'))
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

        # Actions: View
        self.actionFullScreen = QAction(self)
        self.actionFullScreen.setObjectName('actionFullScreen')
        self.actionFullScreen.setCheckable(True)
        self.actionFullScreen.setIconText(self.tr('Full Screen'))
        self.actionFullScreen.setShortcuts([QKeySequence(Qt.Key_F11), QKeySequence.FullScreen])
        self.actionFullScreen.setData(self.tr('Display the window in full screen'))
        self.actionFullScreen.triggered.connect(self.onActionFullScreenTriggered)

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


    def updateMenuOpenRecent(self):

        if len(self._settings.recentDocumentList) > 0:
            pass

        else:
            # Document list is empty; disable the menu item.
            self.menuOpenRecent.setDisabled(True)


    def createToolbars(self):

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


    def readSettings(self):

        settings = QSettings()

        self._settings.load(settings)

        # Document: Defaults
        self._settings.defaultCellRows = int(settings.value('Settings/defaultCellRows', self._settings.defaultCellRows))

        # Recent documents
        size = settings.beginReadArray('recentDocumentList')
        for i in range(size):
            settings.setArrayIndex(i)
            self._settings.recentDocumentList.append(settings.value('document'))
        settings.endArray()

        # Application and dialog properties
        applicationState = settings.value('Application/state', QByteArray())
        applicationGeometry = settings.value('Application/geometry', QByteArray())
        self.aboutDialogGeometry = settings.value('AboutDialog/geometry', QByteArray())
        self.colophonDialogGeometry = settings.value('ColophonDialog/geometry', QByteArray())
        self.keyboardShortcutsDialogGeometry = settings.value('KeyboardShortcutsDialog/geometry', QByteArray())
        self.preferencesDialogGeometry = settings.value('PreferencesDialog/geometry', QByteArray())

        # Set application properties
        state = applicationState if self._settings.restoreApplicationState() else QByteArray()
        self.setApplicationState(state)
        geometry = applicationGeometry if self._settings.restoreApplicationGeometry() else QByteArray()
        self.setApplicationGeometry(geometry)


    def writeSettings(self):

        settings = QSettings()

        self._settings.save(settings)

        # Document: Defaults
        settings.setValue('Settings/defaultCellRows', self._settings.defaultCellRows)

        # Recent documents
        settings.beginWriteArray('recentDocumentList')
        for i in range(len(self._settings.recentDocumentList)):
            settings.setArrayIndex(i)
            settings.setValue('document', self._settings.recentDocumentList[i])
        settings.endArray()

        # Application and dialog properties
        state = self.applicationState() if self._settings.restoreApplicationState() else QByteArray()
        settings.setValue('Application/state', state)
        geometry = self.applicationGeometry() if self._settings.restoreApplicationGeometry() else QByteArray()
        settings.setValue('Application/geometry', geometry)
        settings.setValue('AboutDialog/geometry', self.aboutDialogGeometry)
        settings.setValue('ColophonDialog/geometry', self.colophonDialogGeometry)
        settings.setValue('KeyboardShortcutsDialog/geometry', self.keyboardShortcutsDialogGeometry)
        settings.setValue('PreferencesDialog/geometry', self.preferencesDialogGeometry)


    def setApplicationState(self, state=QByteArray()):

        if state:
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

        if geometry:
            self.restoreGeometry(geometry)
        else:
            availableGeometry = QRect(QApplication.desktop().availableGeometry(self))
            self.resize(availableGeometry.width() * 2/3, availableGeometry.height() * 2/3)
            self.move((availableGeometry.width() - self.width()) / 2, (availableGeometry.height() - self.height()) / 2)


    def applicationGeometry(self):

        return self.saveGeometry()


    def closeEvent(self, event):

        if True:
            self.writeSettings()
            event.accept()
        else:
            event.ignore()


    def createDocumentChild(self):

        document = DocumentTable(self)
        document.setSettings(self._settings)
        self.documentArea.addSubWindow(document)

        return document


    def findDocumentChild(self, url):

        canonicalFilePath = QFileInfo(url).canonicalFilePath()

        for window in self.documentArea.subWindowList():
            if window.widget().documentPath() == canonicalFilePath:
                return window

        return None


    def activeDocumentChild(self):

        window = self.documentArea.activeSubWindow()

        return window if window else None


    def openDocument(self, url):

        # Checks whether the given document is already open.
        existing = self.findDocumentChild(url)
        if existing:
            self.documentArea.setActiveSubWindow(existing)
            return True

        succeeded = self.loadDocument(url)
        if succeeded:
            self.statusBar().showMessage('Document loaded', 3000)

        return succeeded


    def loadDocument(self, url):

        document = self.createDocumentChild()

        succeeded = document.loadDocument(url)
        if succeeded:
            document.show()
        else:
            document.close()

        return succeeded


    def onActionAboutTriggered(self):

        geometry = self.aboutDialogGeometry if self._settings.restoreDialogGeometry() else QByteArray()

        dialog = AboutDialog(self)
        dialog.setDialogGeometry(geometry)
        dialog.exec_()

        self.aboutDialogGeometry = dialog.dialogGeometry() if self._settings.restoreDialogGeometry() else QByteArray()


    def onActionColophonTriggered(self):

        geometry = self.colophonDialogGeometry if self._settings.restoreDialogGeometry() else QByteArray()

        dialog = ColophonDialog(self)
        dialog.setDialogGeometry(geometry)
        dialog.exec_()

        self.colophonDialogGeometry = dialog.dialogGeometry() if self._settings.restoreDialogGeometry() else QByteArray()


    def onActionPreferencesTriggered(self):

        geometry = self.preferencesDialogGeometry if self._settings.restoreDialogGeometry() else QByteArray()

        dialog = PreferencesDialog(self)
        dialog.setDialogGeometry(geometry)
        dialog.setSettings(self._settings)
        dialog.exec_()

        self._settings = dialog.settings()
        self.preferencesDialogGeometry = dialog.dialogGeometry() if self._settings.restoreDialogGeometry() else QByteArray()


    def onActionNewTriggered(self):

        document = self.createDocumentChild()
        document.newDocument()
        document.show()


    def onActionOpenTriggered(self):

        urls = QFileDialog.getOpenFileNames(self,
                   'Open Document',
                   QStandardPaths.writableLocation(QStandardPaths.HomeLocation),
                   'CSV Files (*.csv);; All Files (*.*)')[0]

        for url in urls:
            self.openDocument(url)


    def onActionFullScreenTriggered(self):

        if not self.isFullScreen():
            self.setWindowState(self.windowState() | Qt.WindowFullScreen)
        else:
            self.setWindowState(self.windowState() & ~Qt.WindowFullScreen)

        self.updateActionFullScreen()


    def onActionKeyboardShortcutsTriggered(self):

        geometry = self.keyboardShortcutsDialogGeometry if self._settings.restoreDialogGeometry() else QByteArray()

        self.keyboardShortcutsDialog = KeyboardShortcutsDialog(self)
        self.keyboardShortcutsDialog.setWindowTitle('Keyboard Shortcuts')
        self.keyboardShortcutsDialog.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.keyboardShortcutsDialog.setWindowGeometry(geometry)
        self.keyboardShortcutsDialog.finished.connect(self.onDialogKeyboardShortcutsFinished)
        self.keyboardShortcutsDialog.show()


    def onDialogKeyboardShortcutsFinished(self):

        self.keyboardShortcutsDialogGeometry = self.keyboardShortcutsDialog.windowGeometry() if self._settings.restoreDialogGeometry() else QByteArray()
