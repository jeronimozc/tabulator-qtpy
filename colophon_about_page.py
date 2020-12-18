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

from PySide2.QtWidgets import QApplication, QFrame, QTextBrowser, QVBoxLayout, QWidget


class ColophonAboutWidget(QWidget):

    def __init__(self, parent=None):
        """
        Initializes the ColophonAboutWidget class.
        """
        super(ColophonAboutWidget, self).__init__(parent)

        textBox = QTextBrowser()
        textBox.setFrameStyle(QFrame.NoFrame)
        textBox.setStyleSheet('background-color:transparent;')
        textBox.setOpenExternalLinks(True)
        textBox.setHtml(f'''<html><body>
            <p>{QApplication.applicationName()} is an open source tool written in Qt for Python and intended for easy creation and editing of documents with character-separated values.</p>
            <p>Copyright &copy; 2020 <a href="{QApplication.organizationDomain()}">{QApplication.organizationName()}</a>.</p>
            <p>This application is licensed under the terms of the <a href="https://www.gnu.org/licenses/gpl-3.0.en.html">GNU General Public License, version 3</a>.</p>
            </body></html>''')

        # Main layout
        layout = QVBoxLayout()
        layout.addWidget(textBox, 1)

        self.setLayout(layout)


    def title(self):
        """
        Returns title of the widget.
        """
        return 'About'
