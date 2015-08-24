#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'

from PySide.QtGui import *
from PySide.QtCore import *

from mainwindow_ui import Ui_MainWindow


class MoswarBotError(Exception):
    pass


class MoswarButtonIsMissError(MoswarBotError):
    def __init__(self, title_button):
        super().__init__('Не найдена кнопка "{}".'.format(title_button))


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
        self.ui.view.linkClicked.connect(lambda x: self.ui.url_le.setText(x.toString()))

        # При клике на кнопку, мы получаем значение data текущего элемента и вызываем функцию, хранящуюся там
        self.ui.run_pb.clicked.connect(lambda: self.ui.commands_cb.itemData(self.ui.commands_cb.currentIndex())())

        # Список действий бота
        self.name_action_dict = {
            'Авторизация': self.auth,
            'Закоулки': self.alley,
            'Площадь': self.square,
            'Задания': self.jobs,
            'Персонаж': self.pers,
            'Рейтинг': self.rating,
            'Хата': self.home,
            'Клан': self.clan,
            'Заначка': self.stash,
            'Тверская': self.tverskaya,
            'Арбат': self.arbat,
            'Бутово': self.butovo,
        }

        # Добавляем команды
        for command in sorted(self.name_action_dict):
            self.ui.commands_cb.addItem(command, self.name_action_dict[command])

    def auth(self):
        """Функция заполняет поля логина и пароля и нажимает на кнопку Войти."""

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
            raise MoswarButtonIsMissError('Войти')

        submit.evaluateJavaScript("this.click()")

    def alley(self):
        """Функция нажимает на кнопку Закоулки."""

        doc = self.ui.view.page().mainFrame().documentElement()

        a = doc.findFirst("a[class=alley]")
        if a.isNull():
            raise MoswarButtonIsMissError('Закоулки')

        a.evaluateJavaScript("window.location.href = this.href;")

    def square(self):
        """Функция нажимает на кнопку Площадь."""

        doc = self.ui.view.page().mainFrame().documentElement()

        a = doc.findFirst("a[class=square]")
        if a.isNull():
            raise MoswarButtonIsMissError('Площадь')

        a.evaluateJavaScript("window.location.href = this.href;")

    def jobs(self):
        """Функция нажимает на кнопку Задания."""

        doc = self.ui.view.page().mainFrame().documentElement()

        a = doc.findFirst("a[class=jobs]")
        if a.isNull():
            raise MoswarButtonIsMissError('Задания')

        a.evaluateJavaScript("window.location.href = this.href;")

    def pers(self):
        """Функция нажимает на кнопку Персонаж."""

        doc = self.ui.view.page().mainFrame().documentElement()

        a = doc.findFirst("a[class=pers]")
        if a.isNull():
            raise MoswarButtonIsMissError('Персонаж')

        a.evaluateJavaScript("window.location.href = this.href;")

    def rating(self):
        """Функция нажимает на кнопку Рейтинг."""

        doc = self.ui.view.page().mainFrame().documentElement()

        a = doc.findFirst("a[class=rating]")
        if a.isNull():
            raise MoswarButtonIsMissError('Рейтинг')

        a.evaluateJavaScript("window.location.href = this.href;")

    def home(self):
        """Функция нажимает на кнопку Хата."""

        doc = self.ui.view.page().mainFrame().documentElement()

        a = doc.findFirst("a[class=home]")
        if a.isNull():
            raise MoswarButtonIsMissError('Хата')

        a.evaluateJavaScript("window.location.href = this.href;")

    def clan(self):
        """Функция нажимает на кнопку Клан."""

        doc = self.ui.view.page().mainFrame().documentElement()

        a = doc.findFirst("a[class=clan]")
        if a.isNull():
            raise MoswarButtonIsMissError('Клан')

        a.evaluateJavaScript("window.location.href = this.href;")

    def stash(self):
        """Функция нажимает на кнопку Заначка."""

        doc = self.ui.view.page().mainFrame().documentElement()

        a = doc.findFirst("a[class=stash]")
        if a.isNull():
            raise MoswarButtonIsMissError('Заначка')

        a.evaluateJavaScript("window.location.href = this.href;")

    def tverskaya(self):
        """Функция нажимает на кнопку Тверская."""

        doc = self.ui.view.page().mainFrame().documentElement()

        a = doc.findFirst("a[class=square-leftstreet]")
        if a.isNull():
            raise MoswarButtonIsMissError('Тверская')

        a.evaluateJavaScript("window.location.href = this.href;")

    def arbat(self):
        """Функция нажимает на кнопку Арбат."""

        doc = self.ui.view.page().mainFrame().documentElement()

        a = doc.findFirst("a[class=square-rightstreet]")
        if a.isNull():
            raise MoswarButtonIsMissError('Арбат')

        a.evaluateJavaScript("window.location.href = this.href;")

    def butovo(self):
        """Функция нажимает на кнопку Бутово."""

        doc = self.ui.view.page().mainFrame().documentElement()

        a = doc.findFirst("a[class=square-middlestreet]")
        if a.isNull():
            raise MoswarButtonIsMissError('Бутово')

        a.evaluateJavaScript("window.location.href = this.href;")
