#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import logging
import sys

from PySide.QtGui import *
from PySide.QtCore import *
from PySide.QtWebKit import *

from mainwindow import MainWindow


# URL = 'http://www.moswar.ru/player/'
URL = 'http://www.moswar.ru/'
LOGIN = 'ilya.petrash@inbox.ru'
PASSWORD = '0JHQu9GPRnVjazop'
TITLE = "Бот moswar'а"


app = QApplication(sys.argv)

mw = MainWindow()
mw.setWindowTitle(TITLE)
mw.resize(1000, 800)
mw.show()

sys.exit(app.exec_())
