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

from PySide2.QtCore import QByteArray, QRect
from PySide2.QtWidgets import QApplication, QDialog, QDialogButtonBox, QTabWidget, QVBoxLayout

from colophon_about_page import ColophonAboutPage
from colophon_authors_widget import ColophonAuthorsWidget
from colophon_credits_widget import ColophonCreditsWidget
from colophon_environment_page import ColophonEnvironmentPage
from colophon_license_widget import ColophonLicenseWidget
from dialog_title_box import DialogTitleBox


class ColophonDialog(QDialog):

    def __init__(self, parent=None):
        """
        Initializes the ColophonDialog class.
        """
        super(ColophonDialog, self).__init__(parent)

        # Tab box
        about = ColophonAboutPage()
        authors = ColophonAuthorsWidget()
        credits = ColophonCreditsWidget()
        environment = ColophonEnvironmentPage()
        license = ColophonLicenseWidget()

        tabBox = QTabWidget()
        tabBox.addTab(about, about.title())
        tabBox.addTab(environment, environment.title())
        tabBox.addTab(license, license.title())
        tabBox.addTab(authors, authors.title())
        tabBox.addTab(credits, credits.title())

        # Button box
        buttonBox = QDialogButtonBox(QDialogButtonBox.Close)
        buttonBox.rejected.connect(self.close)

        # Main layout
        layout = QVBoxLayout()
        layout.addWidget(DialogTitleBox())
        layout.addWidget(tabBox, 1)
        layout.addWidget(buttonBox)

        self.setLayout(layout)


    def windowGeometry(self):
        """
        Returns the geometry of the widget.
        """
        return self.saveGeometry()


    def setWindowGeometry(self, geometry):
        """
        Sets the geometry of the widget.
        """
        if geometry:
            self.restoreGeometry(geometry)
        else:
            availableGeometry = QRect(QApplication.desktop().availableGeometry(self))
            self.resize(availableGeometry.width() / 3, availableGeometry.height() / 3)
            self.move((availableGeometry.width() - self.width()) / 2, (availableGeometry.height() - self.height()) / 2)
