#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import sys
from PySide.QtGui import QApplication
from mainwindow import MainWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)

    mw = MainWindow()
    mw.resize(1000, 800)
    mw.show()

    # Загрузка страницы мосвара и авторизация
    mw.auth()

    sys.exit(app.exec_())

#     from PySide.QtWebKit import *
#     view = QWebView()
#     # view.setHtml(open('Ограбление корованов. Пустыня.htm', encoding='utf-8').read())
#     view.setHtml("""<div class="kubovich">
#                     <div class="controls">
#                     <button id="push" class="button disabled" type="button"/>
#                     <button id="push-ellow" class="button" tooltip="1" type="button"/>
#                     </div>
#                     </div>""")
#     # from PySide.QtCore import *
#     # timer = QTimer()
#     # timer.setSingleShot(True)
#     # timer.start(3000)
#     # loop = QEventLoop()
#     # timer.timeout.connect(loop.quit)
#     # loop.exec_()
#
#     doc = view.page().mainFrame().documentElement()
#
#     controls = doc.findFirst('.kubovich .controls')
#     if controls.isNull():
#         raise MoswarElementIsMissError('Не найдена панель управления для игры с Кубовичем.')
#
#     game_button = controls.findFirst('#push')
#     super_game_button = controls.findFirst('#push-ellow')
#
#     if game_button.isNull() or super_game_button.isNull():
#         raise MoswarElementIsMissError('Не найдены кнопки для игры с Кубовичем.')
#
#     disabled_game = 'disabled' in game_button.attribute('class')
#     disabled_super_game = 'disabled' in super_game_button.attribute('class')
#
#     print(disabled_game)
#     print(disabled_super_game)
#
#     if not disabled_game:
#         # TODO: определять, была ли уже игра или еще сегодня не наступила
#         print('Кубович еще не готов играть')
#         return
#
#
#     # Крутить барабан: controls.findFirst('#push')
# # Супер игра: controls.findFirst('.#push-ellow')
#
#     # view.show()
#     # app.exec_()
