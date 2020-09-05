# This Python file uses the following encoding: utf-8
#
# Copyright 2020 NotNypical, <https://notnypical.github.io>.
#
# This file is part of pyTabulator.
#
# pyTabulator is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyTabulator is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyTabulator.  If not, see <https://www.gnu.org/licenses/>.
#

from PySide2.QtCore import QByteArray, QRect, QSettings, Qt
from PySide2.QtGui import QIcon, QKeySequence
from PySide2.QtWidgets import QAction, QApplication, QMainWindow

from about_dialog import AboutDialog
from colophon_dialog import ColophonDialog
from preferences_dialog import PreferencesDialog

import resources


class MainWindow(QMainWindow):

    def __init__(self):
        """
        Initializes the MainWindow class.
        """
        QMainWindow.__init__(self)

        self.setupUI()

        self.readSettings()


    def setupUI(self):
        """
        Sets up the user interface.
        """
        self.setWindowIcon(QIcon(':/icons/apps/22/tabulator.svg'))

        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()


    def createActions(self):
        """
        Creates user interface actions.
        """

        # Actions: Application
        self.actionAbout = QAction(f'About {QApplication.applicationName()}', self)
        self.actionAbout.setIcon(QIcon(':/icons/apps/16/tabulator.svg'))
        self.actionAbout.setStatusTip('Brief description of the application')
        self.actionAbout.setToolTip('Brief description of the application')
        self.actionAbout.triggered.connect(self.onActionAboutTriggered)

        self.actionColophon = QAction('Colophon', self)
        self.actionColophon.setStatusTip('Lengthy description of the application')
        self.actionColophon.setToolTip('Lengthy description of the application')
        self.actionColophon.triggered.connect(self.onActionColophonTriggered)

        self.actionPreferences = QAction('Preferences…', self)
        self.actionPreferences.setIcon(QIcon.fromTheme('configure', QIcon(':/icons/actions/16/configure.svg')))
        self.actionPreferences.setStatusTip('Customize the appearance and behavior of the application')
        self.actionPreferences.setToolTip('Customize the appearance and behavior of the application')
        self.actionPreferences.triggered.connect(self.onActionPreferencesTriggered)

        self.actionQuit = QAction('Quit', self)
        self.actionQuit.setIcon(QIcon.fromTheme('application-exit', QIcon(':/icons/actions/16/application-exit.svg')))
        self.actionQuit.setShortcut(QKeySequence.Quit)
        self.actionQuit.setStatusTip('Quit the application')
        self.actionQuit.setToolTip('Quit the application')
        self.actionQuit.triggered.connect(self.onActionQuitTriggered)


    def createMenus(self):
        """
        Creates groups of menu items.
        """

        # Menu: Application
        menuApplication = self.menuBar().addMenu('Application')
        menuApplication.addAction(self.actionAbout)
        menuApplication.addAction(self.actionColophon)
        menuApplication.addSeparator()
        menuApplication.addAction(self.actionPreferences)
        menuApplication.addSeparator()
        menuApplication.addAction(self.actionQuit)

        # Menu: Document
        menuDocument = self.menuBar().addMenu('Document')

        # Menu: Edit
        menuEdit = self.menuBar().addMenu('Edit')

        # Menu: Tools
        menuTools = self.menuBar().addMenu('Tools')


    def createToolBars(self):
        """
        Creates groups of toolbar buttons.
        """

        # Toolbar: Document
        toolbarDocument = self.addToolBar('Document')
        toolbarDocument.setObjectName('toolbarDocument')

        # Toolbar: Edit
        toolbarEdit = self.addToolBar('Edit')
        toolbarEdit.setObjectName('toolbarEdit')

        # Toolbar: Tools
        toolbarTools = self.addToolBar('Tools')
        toolbarTools.setObjectName('toolbarTools')


    def createStatusBar(self):
        """
        Creates the status bar.
        """
        self.statusBar().showMessage(f'Welcome to {QApplication.applicationName()}', 3000)


    def readSettings(self):
        """
        Restores user preferences and other application properties.
        """
        settings = QSettings()

        # Read user preferences
        geometryWindowRestore = self.valueToBool(settings.value('Settings/geometryWindowRestore', True))

        # Set window properties
        geometry = settings.value('MainWindow/geometry', QByteArray())
        if geometryWindowRestore and geometry:
            self.restoreGeometry(geometry)
        else:
            availableGeometry = QRect(QApplication.desktop().availableGeometry(self))
            self.resize(availableGeometry.width() / 2, availableGeometry.height() / 2);
            self.move((availableGeometry.width() - self.width()) / 2, (availableGeometry.height() - self.height()) / 2);
        self.restoreState(settings.value('MainWindow/state', QByteArray()))


    def writeSettings(self):
        """
        Saves user preferences and other application properties.
        """
        settings = QSettings()

        # Read user preferences
        geometryWindowRestore = self.valueToBool(settings.value('Settings/geometryWindowRestore', True))

        # Store window properties
        if geometryWindowRestore:
            settings.setValue('MainWindow/geometry', self.saveGeometry())
        settings.setValue('MainWindow/state', self.saveState())


    @staticmethod
    def valueToBool(value):
        """
        Converts a specified value to an equivalent Boolean value.

        Args:
            value (bool): The specified value.

        Returns:
            bool: The equivalent Boolean value.
        """
        return value.lower() == 'true' if isinstance(value, str) else bool(value)


    def closeEvent(self, event):
        """
        Processes the Close event.

        Args:
            event (QCloseEvent): The Close event.
        """

        if True:
            self.writeSettings()
            event.accept()
        else:
            event.ignore()


    def onActionAboutTriggered(self):
        """
        Displays the About dialog.
        """
        aboutDialog = AboutDialog(self)
        aboutDialog.setWindowTitle(f'About {QApplication.applicationName()}')
        aboutDialog.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        aboutDialog.exec_()


    def onActionColophonTriggered(self):
        """
        Displays the Colophon dialog.
        """
        colophonDialog = ColophonDialog(self)
        colophonDialog.setWindowTitle('Colophon')
        colophonDialog.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        colophonDialog.exec_()


    def onActionPreferencesTriggered(self):
        """
        Displays the Preferences dialog.
        """
        preferencesDialog = PreferencesDialog(self)
        preferencesDialog.setWindowTitle('Preferences')
        preferencesDialog.exec_()


    def onActionQuitTriggered(self):
        """
        Fires the Close event to terminate the application.
        """
        self.close()
