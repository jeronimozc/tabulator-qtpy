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

import sys

from PySide2.QtCore import QCommandLineParser, QCoreApplication
from PySide2.QtWidgets import QApplication

from main_window import MainWindow


if __name__ == "__main__":

    app = QApplication(sys.argv)
    app.setOrganizationName("NotNypical")
    app.setOrganizationDomain("https://notnypical.github.io")
    app.setApplicationName("Tabulator-QtPy")
    app.setApplicationDisplayName("Tabulator-QtPy")
    app.setApplicationVersion("0.1.0")

    parser = QCommandLineParser()
    parser.setApplicationDescription(QCoreApplication.translate("main", "{0} - An editor tool for documents with character-separated values").format(app.applicationName()))
    parser.addHelpOption()
    parser.addVersionOption()
    parser.addPositionalArgument("files", "Documents to open.", "[files...]")
    parser.process(app)

    window = MainWindow()
    fileNames = parser.positionalArguments()
    for fileName in fileNames:
        window.openDocument(fileName)
    window.show()

    sys.exit(app.exec_())
