#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import sys
from PySide.QtGui import QApplication
from mainwindow import MainWindow


# TODO: бесплатный спортлото: http://www.moswar.ru/casino/sportloto/


if __name__ == '__main__':
    app = QApplication(sys.argv)

    mw = MainWindow()
    mw.resize(1000, 800)
    mw.show()

    # Загрузка страницы мосвара и авторизация
    mw.auth()

    sys.exit(app.exec_())

    # from PySide.QtWebKit import *
    # view = QWebView()
    # view.setHtml(open('Ограбление корованов. Пустыня.htm', encoding='utf-8').read())
    # from PySide.QtCore import *
    # timer = QTimer()
    # timer.setSingleShot(True)
    # timer.start(3000)
    # loop = QEventLoop()
    # timer.timeout.connect(loop.quit)
    # loop.exec_()
    #
    # doc = view.page().mainFrame().documentElement()
    #
    # # view.show()
    # # app.exec_()
