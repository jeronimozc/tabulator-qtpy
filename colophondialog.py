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
from PySide2.QtSvg import QSvgWidget
from PySide2.QtWidgets import QApplication, QDialog, QDialogButtonBox, QHBoxLayout, QLabel, QVBoxLayout, QWidget


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

        # Button box
        buttonBox = QDialogButtonBox(QDialogButtonBox.Close)
        buttonBox.rejected.connect(self.onButtonCloseClicked)

        # Layout
        layout = QVBoxLayout()
        layout.addLayout(titleBox)
        layout.addWidget(buttonBox)

        self.setLayout(layout)


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
