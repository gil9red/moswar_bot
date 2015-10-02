#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import sys
from PySide.QtGui import QApplication
from mainwindow import MainWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)

    mw = MainWindow()
    mw.resize(1300, 800)
    mw.show()

    # Загрузка страницы мосвара и авторизация
    mw.auth()

    sys.exit(app.exec_())

    # from PySide.QtWebKit import *
    # view = QWebView()
    # view.setHtml(open('Проигранный бой ВсехПорву [9] vs. Draconzver [10] .htm', encoding='utf-8').read())
    # # view.setHtml("""        <div class="fighter2">
    # #       <span class="user ">
    # #            <i class="npc" title="Горожанин"></i>
    # #            <a onclick="return AngryAjax.goToUrl(this, event);" href="http://www.moswar.ru/player/38325/"> savteam</a>
    # #            <span class="level">[7]</span>
    # #        </span>
    # #      </div>""")
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
    #
    # import re
    # pattern = re.compile(r'Победитель: (.+) \[[\d]+\]')
    # pattern2 = re.compile(r'(.+) \[[\d]+\]')
    #
    # css_path = '#personal .name'
    # name = doc.findFirst(css_path)
    # match = pattern2.search(name.toPlainText())
    # print('"{}"'.format(match.group(1)))
    #
    # # print('"{}"'.format(doc.findFirst('.fighter2 a').toPlainText()))
    # # result = doc.findFirst('.result')
    # # if result.isNone():
    # #     raise Exception('Не найден result')
    # # result_text = result.toPlainText()
    # # match = pattern.search(result_text)
    # # if match is None:
    # #     raise Exception('Не удалось найти победителя драки')
    # # print('Победитель: "{}"'.format(match.group(1)))
    # #
    # # view.show()
    # # app.exec_()
