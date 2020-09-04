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


class LicensePage(QWidget):

    def __init__(self, parent=None):
        """
        Initializes the LicensePage class.
        """
        super(LicensePage, self).__init__(parent)

        textBox = QTextBrowser()
        textBox.setFrameStyle(QFrame.NoFrame)
        textBox.setStyleSheet('background-color:transparent;')
        textBox.setOpenExternalLinks(True)
        textBox.setHtml(f'''<html><body>
            <p>{QApplication.applicationName()} is free software: you can redistribute it and/or modify it under the terms of the
                GNU General Public License as published by the Free Software Foundation, either version 3 of the License,
                or (at your option) any later version.</p>
            <p>{QApplication.applicationName()} is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
                without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
                See the GNU General Public License for more details.</p>
            <p>You should have received a copy of the GNU General Public License along with {QApplication.applicationName()}.
                If not, see <a href="https://www.gnu.org/licenses/">https://www.gnu.org/licenses/</a>.</p>
            </body></html>''')

        # Main layout
        layout = QVBoxLayout()
        layout.addWidget(textBox)
        layout.addStretch(1)

        self.setLayout(layout)
