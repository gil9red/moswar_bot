#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'

from PySide.QtGui import *
from PySide.QtCore import *

from mainwindow_ui import Ui_MainWindow


class MoswarBotError(Exception):
    pass


class MoswarAuthError(MoswarBotError):
    pass


URL = 'http://www.moswar.ru/'
LOGIN = 'ilya.petrash@inbox.ru'
PASSWORD = '0JHQu9GPRnVjazop'
TITLE = "Бот moswar'а"


class MainWindow(QMainWindow, QObject):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # view.loadFinished.connect(auth)
        self.ui.view.load(URL)

        self.ui.view.urlChanged.connect(lambda x: self.ui.url_le.setText(x.toString()))

        self.ui.commands_cb.addItem('Авторизация', self.auth)

        # При клике на кнопку, мы получаем значение data текущего элемента и вызываем функцию, хранящуюся там
        self.ui.run_pb.clicked.connect(lambda: self.ui.commands_cb.itemData(self.ui.commands_cb.currentIndex())())

    def auth(self):
        current_url = self.ui.view.url().toString()
        if current_url != URL:
            print('Авторизация используется для страницы "{}", Текущая страница: "{}"'.format(URL, current_url))
            return

        doc = self.ui.view.page().mainFrame().documentElement()
        login = doc.findFirst('input[id=login-email]')
        password = doc.findFirst('input[id=login-password]')

        if login.isNull() or password.isNull():
            raise MoswarAuthError('Не найдены поля логина и пароля.')

        login.setAttribute("value", LOGIN)
        password.setAttribute("value", PASSWORD)

        submit = doc.findFirst("input[type=submit]")
        if submit.isNull():
            raise MoswarAuthError('Не найдена кнопка "Войти".')

        submit.evaluateJavaScript("this.click()")


    # def auth(self, is_finished):
    #     print(is_finished, self.ui.view.url())
    #
    #     current_url = self.ui.view.url().toString()
    #     if current_url != URL:
    #         print('Авторизация используется для страницы "{}", Текущая страница: "{}"'.format(URL, current_url))
    #         return
    #
    #     if not is_finished:
    #         return
    #
    #     doc = self.ui.view.page().mainFrame().documentElement()
    #     login = doc.findFirst('input[id=login-email]')
    #     password = doc.findFirst('input[id=login-password]')
    #
    #     if login.isNull() or password.isNull():
    #         raise MoswarAuthError('Не найдены поля логина и пароля.')
    #
    #     login.setAttribute("value", LOGIN)
    #     password.setAttribute("value", PASSWORD)
    #
    #     submit = doc.findFirst("input[type=submit]")
    #     if submit.isNull():
    #         raise MoswarAuthError('Не найдена кнопка "Войти".')
    #
    #     submit.evaluateJavaScript("this.click()")
