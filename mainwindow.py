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

from PySide2.QtCore import QByteArray, QRect, QSettings
from PySide2.QtGui import QIcon, QKeySequence
from PySide2.QtWidgets import QAction, QApplication, QMainWindow

import resources


class MainWindow(QMainWindow):

    def __init__(self):
        """
        Initializes the MainWindow class.
        """
        QMainWindow.__init__(self)

        self.setWindowIcon(QIcon(':/logos/tabulator'))

        self.setupUI()

        self.readSettings()


    def setupUI(self):
        """
        Setup user interface.
        """

        self.createActions()
        self.createMenus()
        self.createStatusBars()


    def createActions(self):
        """
        Creates user interface actions.
        """

        # Actions: Application
        self.actionQuit = QAction('Quit', self)
        self.actionQuit.setIcon(QIcon.fromTheme('application-exit', QIcon(':/icons/application-exit')))
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
        menuApplication.addAction(self.actionQuit)


    def createStatusBars(self):
        """
        Creates the status bar.
        """

        self.statusBar().showMessage('Ready', 3000)


    def readSettings(self):
        """
        Restores user preferences and other application settings.
        """
        settings = QSettings()

        geometry = settings.value('MainWindow/geometry', QByteArray())
        if geometry:
            # Restore window geometry
            self.restoreGeometry(geometry)
        else:
            # Center window
            availableGeometry = QRect(QApplication.desktop().availableGeometry(self))
            self.resize(availableGeometry.width() / 2, availableGeometry.height() / 2);
            self.move((availableGeometry.width() - self.width()) / 2, (availableGeometry.height() - self.height()) / 2);


    def writeSettings(self):
        """
        Saves user preferences and other application settings.
        """
        settings = QSettings()

        settings.setValue('MainWindow/geometry', self.saveGeometry())


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


    def onActionQuitTriggered(self):
        """
        Fires the Close event to terminate the application.
        """

        self.close()
