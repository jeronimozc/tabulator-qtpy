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

from PySide2.QtCore import QCommandLineParser
from PySide2.QtWidgets import QApplication

from main_window import MainWindow


ORGANIZATION_NAME             = 'NotNypical'
ORGANIZATION_DOMAIN           = 'https://notnypical.github.io'
APPLICATION_NAME              = 'pyTabulator'
APPLICATION_BRIEF_DESCRIPTION = 'A CSV editor written in Qt for Python.'
APPLICATION_VERSION           = '0.1.0'


if __name__ == "__main__":

    app = QApplication(sys.argv)
    app.setOrganizationName(ORGANIZATION_NAME)
    app.setOrganizationDomain(ORGANIZATION_DOMAIN)
    app.setApplicationName(APPLICATION_NAME)
    app.setApplicationVersion(APPLICATION_VERSION)

    parser = QCommandLineParser()
    parser.setApplicationDescription(f'{APPLICATION_NAME} - {APPLICATION_BRIEF_DESCRIPTION}')
    parser.addHelpOption()
    parser.addVersionOption()
    parser.process(app)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
