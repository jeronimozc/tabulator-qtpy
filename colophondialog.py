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

import sys
import PySide2.QtCore

from PySide2.QtCore import QByteArray, QRect, QSettings, QSysInfo
from PySide2.QtSvg import QSvgWidget
from PySide2.QtWidgets import QApplication, QDialog, QDialogButtonBox, QFrame, QHBoxLayout, QLabel, QTabWidget, QTextBrowser, QVBoxLayout, QWidget


class ColophonDialog(QDialog):

    def __init__(self, parent=None):
        """
        Initializes the ColophonDialog class.
        """
        super(ColophonDialog, self).__init__(parent)

        self.organizationName = QApplication.organizationName()
        self.organizationDomain = QApplication.organizationDomain()
        self.applicationName = QApplication.applicationName()
        self.applicationDescription = 'A CSV editor written in Qt for Python.'
        self.applicationVersion = QApplication.applicationVersion()

        self.pythonVersion = sys.version
        self.pysideVersion = PySide2.__version__
        self.qtVersion = PySide2.QtCore.qVersion() # Qt version used to run Qt for Python
        self.qtBuildVersion = PySide2.QtCore.__version__ # Qt version used to compile PySide2
        self.osName = QSysInfo.prettyProductName()
        self.osKernelVersion = QSysInfo.kernelVersion()
        self.osCpuArchitecture = QSysInfo.currentCpuArchitecture()

        self.setWindowTitle(f'Colophon') 

        self.setupUI()

        self.readSettings()


    def setupUI(self):
        """
        Setup user interface.
        """

        # Title box
        name = QLabel(f'<strong style="font-size:large">{self.applicationName}</strong> v{self.applicationVersion}')
        description = QLabel(self.applicationDescription)

        widgetTmp = QWidget()
        vboxlayoutTmp = QVBoxLayout(widgetTmp)
        vboxlayoutHeight = name.sizeHint().height() + vboxlayoutTmp.layout().spacing() + description.sizeHint().height()

        logo = QSvgWidget()
        logo.load(':/logos/tabulator')
        logo.setFixedSize(vboxlayoutHeight, vboxlayoutHeight)

        labels = QVBoxLayout()
        labels.addWidget(name)
        labels.addWidget(description)

        titleBox = QHBoxLayout()
        titleBox.addWidget(logo)
        titleBox.addLayout(labels)

        # Tab box
        tabBox = QTabWidget()
        tabBox.addTab(self.tabAbout(), 'About')
        tabBox.addTab(self.tabEnvironment(), 'Environment')
        tabBox.addTab(self.tabLicense(), 'License')
        tabBox.addTab(self.tabAuthors(), 'Authors')
        tabBox.addTab(self.tabCredits(), 'Credits')

        # Button box
        buttonBox = QDialogButtonBox(QDialogButtonBox.Close)
        buttonBox.rejected.connect(self.onButtonCloseClicked)

        # Layout
        layout = QVBoxLayout()
        layout.addLayout(titleBox)
        layout.addWidget(tabBox)
        layout.addWidget(buttonBox)

        self.setLayout(layout)


    def tabAbout(self):
        """
        Displays the About tab.
        """

        textBox = QTextBrowser()
        textBox.setFrameStyle(QFrame.NoFrame)
        textBox.setStyleSheet('background-color:transparent;')
        textBox.setOpenExternalLinks(True)
        textBox.setHtml(f'''<html><body>
            <p>{self.applicationName} is an open source tool written in Qt for Python and intended for easy creation and editing of documents with character-separated values.</p>
            <p>Copyright &copy; 2020 <a href="{self.organizationDomain}">{self.organizationName}</a>.</p>
            <p>This application is licensed under the terms of the <a href="https://www.gnu.org/licenses/gpl-3.0.en.html">GNU General Public License, version 3</a>.</p>
            </body></html>''')

        return textBox


    def tabEnvironment(self):
        """
        Displays the Environment tab.
        """

        textBox = QTextBrowser()
        textBox.setFrameStyle(QFrame.NoFrame)
        textBox.setStyleSheet('background-color:transparent;')
        textBox.setOpenExternalLinks(True)
        textBox.setHtml(f'''<html><body><dl>
            <dt><strong>Application version</strong></dt>
                <dd>{self.applicationVersion}</dd>
            <dt><strong>Qt for Python version</strong></dt>
                <dd>{self.pysideVersion} runs on Qt {self.qtVersion} (Built against {self.qtBuildVersion})</dd>
            <dt><strong>Python version</strong></dt>
                <dd>{self.pythonVersion}</dd>
            <dt><strong>Operation System</strong></dt>
                <dd>{self.osName} (Kernel {self.osKernelVersion} on {self.osCpuArchitecture})</dd>
            </dl></body></html>''')

        return textBox


    def tabLicense(self):
        """
        Displays the License tab.
        """

        textBox = QTextBrowser()
        textBox.setFrameStyle(QFrame.NoFrame)
        textBox.setStyleSheet('background-color:transparent;')
        textBox.setOpenExternalLinks(True)
        textBox.setHtml(f'''<html><body>
            <p>{self.applicationName} is free software: you can redistribute it and/or modify it under the terms of the
                GNU General Public License as published by the Free Software Foundation, either version 3 of the License,
                or (at your option) any later version.</p>
            <p>{self.applicationName} is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
                without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
                See the GNU General Public License for more details.</p>
            <p>You should have received a copy of the GNU General Public License along with {self.applicationName}.
                If not, see <a href="https://www.gnu.org/licenses/">https://www.gnu.org/licenses/</a>.</p>
            </body></html>''')

        return textBox


    def tabAuthors(self):
        """
        Displays the Authors tab.
        """

        textBox = QTextBrowser()
        textBox.setFrameStyle(QFrame.NoFrame)
        textBox.setStyleSheet('background-color:transparent;')
        textBox.setOpenExternalLinks(True)
        textBox.setHtml('''<html><body><dl>
            <dt><strong>NotNypical</strong></dt>
                <dd>Created and developed by <a href="https://notnypical.github.io" title="Visit author's homepage">NotNypical</a>.</dd>
            </dl></body></html>''')

        return textBox


    def tabCredits(self):
        """
        Displays the Credits tab.
        """

        textBox = QTextBrowser()
        textBox.setFrameStyle(QFrame.NoFrame)
        textBox.setStyleSheet('background-color:transparent;')
        textBox.setOpenExternalLinks(True)
        textBox.setHtml('''<html><body><dl>
            <dt><strong>BreezeIcons project</strong></dt>
            <dd>Application logo and icons made by <a href="https://api.kde.org/frameworks/breeze-icons/html/" title="Visit project's homepage">BreezeIcons project</a>
                from <a href="https://kde.org" title="Visit organization's homepage">KDE</a>
                are licensed under <a href="https://www.gnu.org/licenses/lgpl-3.0.en.html" title="GNU Lesser General Public License Version 3">LGPLv3</a>.</dd>
            </dl></body></html>''')

        return textBox


    def readSettings(self):
        """
        Restores user preferences and other application settings.
        """
        settings = QSettings()

        geometry = settings.value('ColophonDialog/geometry', QByteArray())
        if geometry:
            # Restore dialog geometry
            self.restoreGeometry(geometry)
        else:
            # Center dialog
            availableGeometry = QRect(QApplication.desktop().availableGeometry(self))
            self.resize(availableGeometry.width() / 3, availableGeometry.height() / 3);
            self.move((availableGeometry.width() - self.width()) / 2, (availableGeometry.height() - self.height()) / 2);


    def writeSettings(self):
        """
        Saves user preferences and other application settings.
        """
        settings = QSettings()

        settings.setValue('ColophonDialog/geometry', self.saveGeometry())


    def closeEvent(self, event):
        """
        Processes the close event.

        Args:
            event (QCloseEvent): The close event.
        """

        self.writeSettings()
        event.accept()


    def onButtonCloseClicked(self):
        """
        Fires the Close event to terminate the dialog.
        """

        self.close()
