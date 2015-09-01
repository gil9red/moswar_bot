#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'

from urllib.parse import urljoin

from PySide.QtGui import *
from PySide.QtCore import *
from PySide.QtWebKit import *

from mainwindow_ui import Ui_MainWindow

from thimblerig import Thimblerig
from utils import get_logger


class MoswarBotError(Exception):
    pass


class MoswarButtonIsMissError(MoswarBotError):
    def __init__(self, title_button):
        super().__init__('Не найдена кнопка "{}".'.format(title_button))


class MoswarAuthError(MoswarBotError):
    pass


class MoswarMoneyNotFoundError(MoswarBotError):
    pass


LOGIN = 'ilya.petrash@inbox.ru'
PASSWORD = '0JHQu9GPRnVjazop'



# TODO: level up:
# <div id="content" class="levelup">
# После левел апа нужно кликнуть на: <button class="button" type="submit">


# TODO: ограбление корованов: http://www.moswar.ru/desert/


# TODO: кубович на любой странице:
# <div id="leftblock">
# <div id="personal" class="small">
# <div id="tutorial-pers">
# <div class="side-invite">
# <a style="text-decoration:none;" href="/casino/kubovich/" onclick="return AngryAjax.goToUrl(this, event);">
# <div class="side-fractionwar" style="color:#89deff; background:url(/@/images/link/kubovich.jpg) #2a66a1 no-repeat;"> Приз в студию! </div>


# TODO: крутить барабан:
# <div class="reel-place">
# <div class="icon reel">
# <div id="kubovich-smile"></div>
# <div class="controls">
# <table align="center">
# <tbody>
# <tr>
# <td style="width: 35%;">
# <div>
# <button id="push" class="button" type="button">



# TODO: удалить всех из http://www.moswar.ru/phone/contacts/victims/2/
# у которых награда меньше 15к


logger = get_logger('moswar_bot')


class MainWindow(QMainWindow, QObject):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.moswar_url = 'http://www.moswar.ru/'

        QWebSettings.globalSettings().setAttribute(QWebSettings.DeveloperExtrasEnabled, True)

        self.ui.view.urlChanged.connect(lambda x: self.ui.url_le.setText(x.toString()))
        self.ui.view.linkClicked.connect(lambda x: self.ui.url_le.setText(x.toString()))

        # При клике на кнопку, мы получаем значение data текущего элемента и вызываем функцию, хранящуюся там
        self.ui.run_pb.clicked.connect(lambda: self.ui.commands_cb.itemData(self.ui.commands_cb.currentIndex())())

        self.thimblerig = Thimblerig(self)

        # Список действий бота
        self.name_action_dict = {
            'Закоулки': self.alley,
            'Площадь': self.square,
            'Метро': self.metro,
            'Задания': self.jobs,
            'Персонаж': self.player,
            'Хата': self.home,
            'Игра в наперстки': self.thimblerig.run,
        }

        # Добавляем команды
        for command in sorted(self.name_action_dict):
            self.ui.commands_cb.addItem(command, self.name_action_dict[command])

    def _get_doc(self):
        return self.ui.view.page().mainFrame().documentElement()

    doc = property(_get_doc)

    def current_url(self):
        """Функция возвращает текущий адрес страницы."""

        return self.ui.view.url().toString()

    def go(self, relative_url):
        """Функция для загрузки страниц через относительные пути."""

        url = urljoin(self.moswar_url, relative_url)
        self.ui.view.load(url)

    def auth(self):
        """Функция загружает страницу мосвара, заполняет поля логина и пароля и нажимает на кнопку Войти."""

        # Открываем страницу мосвара
        self.ui.view.load(self.moswar_url)

        # Ждем окончания загрузки страницы
        loop = QEventLoop()
        self.ui.view.loadFinished.connect(loop.quit)
        loop.exec_()

        login = self.doc.findFirst('input[id=login-email]')
        password = self.doc.findFirst('input[id=login-password]')

        if login.isNull() or password.isNull():
            raise MoswarAuthError('Не найдены поля логина и пароля.')

        login.setAttribute("value", LOGIN)
        password.setAttribute("value", PASSWORD)

        submit = self.doc.findFirst("input[type=submit]")
        if submit.isNull():
            raise MoswarButtonIsMissError('Войти')

        submit.evaluateJavaScript("this.click()")

    # def base_click_a(self, css_path, title_action):
    #     """Базовая функция для эмуляции клика по a тегам."""
    #
    #     a = self.doc.findFirst(css_path)
    #     if a.isNull():
    #         raise MoswarButtonIsMissError(title_action)
    #
    #     a.evaluateJavaScript("window.location.href = this.href;")
    #
    # def click_header_a(self, class_name, title_action):
    #     """Функция, которая ищет тег a с class_name и эмулирует клик.
    #
    #     Клик настроен на кнопки на заголовке сайта, такие как: Персонаж, Закоулки, Хата и т.п.
    #     """
    #
    #     self.base_click_a("a[class={}]".format(class_name), title_action)

    def alley(self):
        self.go('alley')

    def square(self):
        self.go('square')

    def metro(self):
        self.go('metro')

    def jobs(self):
        self.go('nightclub/jobs')

    def player(self):
        self.go('player')

    def home(self):
        self.go('home')

    def money(self):
        """Функция возвращает количество денег персонажа."""

        try:
            csspath = 'li[class="tugriki-block"]'
            tugriki = self.doc.findFirst(csspath)
            tugriki = tugriki.attribute('title')
            tugriki = tugriki.split(': ')[-1]
            return int(tugriki)

        except Exception as e:
            raise MoswarMoneyNotFoundError(e)

    def click_tag(self, css_path):
        code = """
        tag = $("{}")
        tag.click()
        """.format(css_path)

        ok = self.doc.evaluateJavaScript(code)
        if ok is None:
            logger.warn('Выполнение js скрипта неудачно. Code:\n' + code)
