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

        # view.loadFinished.connect(auth)
        # self.ui.view.load(self.moswar_url)

        # self.ui.view.loadFinished.connect(lambda x=None: print('finished'))
        # self.ui.view.page().mainFrame().pageChanged.connect(lambda x=None: print('pageChanged'))
        # self.ui.view.page().networkAccessManager().finished.connect(lambda x=None: print('finished', x.isFinished()))

        self.ui.view.urlChanged.connect(lambda x: self.ui.url_le.setText(x.toString()))
        self.ui.view.linkClicked.connect(lambda x: self.ui.url_le.setText(x.toString()))

        # При клике на кнопку, мы получаем значение data текущего элемента и вызываем функцию, хранящуюся там
        self.ui.run_pb.clicked.connect(lambda: self.ui.commands_cb.itemData(self.ui.commands_cb.currentIndex())())

        # self.timer_thimble = QTimer()
        # self.timer_thimble.setInterval(1000)
        # self.timer_thimble.timeout.connect(self.select_thimble)
        #
        # self.timer_round_thimble = QTimer()
        # self.timer_round_thimble.setInterval(1000)
        # self.timer_round_thimble.setSingleShot(True)
        # self.timer_round_thimble.timeout.connect(self.nine_thimble)
        #
        # # TODO: добавить игре в наперстки немного рандома
        # self.ruda_count = 0
        # self.thimble_round_count = 0

        self.thimblerig = Thimblerig(self)

        # Список действий бота
        self.name_action_dict = {
            # 'Авторизация': self.auth,

            'Закоулки': self.alley,
            'Площадь': self.square,
            'Метро': self.metro,
            'Задания': self.jobs,
            'Персонаж': self.player,
            # 'Рейтинг': self.rating,
            'Хата': self.home,
            # 'Клан': self.clan,
            # 'Заначка': self.stash,
            # 'Тверская': self.tverskaya,
            # 'Арбат': self.arbat,
            # 'Бутово': self.butovo,

            # 'Игра в наперстки': self.thimble,
            'Игра в наперстки': self.thimblerig.run,
            # '9': self.nine_thimble,
            # 'select_thimbles': self.select_thimbles,
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

    def base_click_a(self, css_path, title_action):
        """Базовая функция для эмуляции клика по a тегам."""

        a = self.doc.findFirst(css_path)
        if a.isNull():
            raise MoswarButtonIsMissError(title_action)

        a.evaluateJavaScript("window.location.href = this.href;")

    def click_header_a(self, class_name, title_action):
        """Функция, которая ищет тег a с class_name и эмулирует клик.

        Клик настроен на кнопки на заголовке сайта, такие как: Персонаж, Закоулки, Хата и т.п.
        """

        self.base_click_a("a[class={}]".format(class_name), title_action)

    def alley(self):
        # """Функция нажимает на кнопку Закоулки."""
        #
        # self.click_header_a('alley', 'Закоулки')

        self.go('alley')

    def square(self):
        # """Функция нажимает на кнопку Площадь."""
        #
        # self.click_header_a('square', 'Площадь')

        self.go('square')

    def metro(self):
        # """Функция нажимает на кнопку Метро."""
        #
        # self.doc = self.ui.view.page().mainFrame().documentElement()
        # a = self.doc.findFirst('div[id="square-metro-button"] a')
        # if a.isNull():
        #     raise MoswarButtonIsMissError('Метро')
        #
        # a.evaluateJavaScript("window.location.href = this.href;")

        self.go('metro')

    def jobs(self):
        # """Функция нажимает на кнопку Задания."""
        #
        # self.click_header_a('jobs', 'Задания')

        self.go('nightclub/jobs')

    def player(self):
        # """Функция нажимает на кнопку Персонаж."""
        #
        # # self.click_header_a('pers', 'Персонаж')

        self.go('player')

    # def rating(self):
    #     """Функция нажимает на кнопку Рейтинг."""
    #
    #     self.click_a('rating', 'Рейтинг')

    def home(self):
        # """Функция нажимает на кнопку Хата."""
        #
        # self.click_header_a('home', 'Хата')

        self.go('home')

    # def clan(self):
    #     """Функция нажимает на кнопку Клан."""
    #
    #     self.click_header_a('clan', 'Клан')
    #
    # def stash(self):
    #     """Функция нажимает на кнопку Заначка."""
    #
    #     self.click_header_a('stash', 'Заначка')
    #
    # def tverskaya(self):
    #     """Функция нажимает на кнопку Тверская."""
    #
    #     self.click_header_a('square-leftstreet', 'Тверская')
    #
    # def arbat(self):
    #     """Функция нажимает на кнопку Арбат."""
    #
    #     self.click_header_a('square-rightstreet', 'Арбат')
    #
    # def butovo(self):
    #     """Функция нажимает на кнопку Бутово."""
    #
    #     self.click_header_a('square-middlestreet', 'Бутово')

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

        # self.finish_tag_click.emit()

    # finished_thimble_game = Signal()
    #
    # def thimble(self):
    #     """Игра в наперстки."""
    #
    #     if self.current_url() == 'http://www.moswar.ru/thimble/':
    #         return
    #
    #     t = time.clock()
    #
    #     # Эмулируем клик на кнопку "Начать играть"
    #     self.go('thimble/start')
    #
    #     # Ждем пока прогрузится страница
    #     loop = QEventLoop()
    #     self.ui.view.loadFinished.connect(loop.quit)
    #     loop.exec_()
    #
    #     self.ruda_count = 0
    #     self.thimble_round_count = 0
    #
    #     self.timer_round_thimble.start()
    #
    #     # Ждем пока закончится игра
    #     loop = QEventLoop()
    #     self.finished_thimble_game.connect(loop.quit)
    #     loop.exec_()
    #
    #     logger.debug('Длительность игры {:.1f} секунд'.format(time.clock() - t))
    #     logger.debug('Игра в наперстки закончилась за {} раундов'.format(self.thimble_round_count))
    #     logger.debug('Угадано {} руды. Потрачено {} тугриков.'.format(self.ruda_count, self.thimble_round_count * 1500))
    #     logger.debug('Удача {:.2f}%'.format(self.ruda_count / (self.thimble_round_count * 3) * 100))
    #
    #     # Эмулируем клик на кнопку "Я наигрался, хватит"
    #     self.go('thimble/leave')
    #
    # def nine_thimble(self):
    #     # a = self.doc.findFirst('div[id="thimble-controls-buttons"] div[data-count="9"] a div')
    #     # print(a)
    #     # if a.isNull():
    #     #     raise MoswarButtonIsMissError('Метро')
    #     #
    #     # a.evaluateJavaScript("this.click()")
    #
    #     if self.money() < 3000:
    #         self.timer_thimble.stop()
    #         logger.debug("Заканчиваю игру.")
    #         self.finished_thimble_game.emit()
    #         return
    #
    #     self.thimble_round_count += 1
    #
    #     css_path = "div[id='thimble-controls-buttons'] div[data-count='9']"
    #     self.click_tag(css_path)
    #
    #     # self.select_thimbles()
    #     self.timer_thimble.start()
    #
    # # finish_tag_click = Signal()
    #
    # # def select_thimbles(self):
    # #     self.timer_thimble.start()
    #
    # def select_thimble(self):
    #     left = self.doc.findFirst('span[id="naperstki-left"]').toInnerXml()
    #     # Если количество попыток равно 0, то останавливаем таймер
    #     if left == '0':
    #         self.timer_thimble.stop()
    #
    #         ruda = self.doc.findFirst('span[id="naperstki-ruda"]')
    #         ruda = ruda.toPlainText()
    #         ruda = int(ruda)
    #         self.ruda_count += ruda
    #         logger.info("Раунд {}. Угадано {} руды.".format(self.thimble_round_count, ruda))
    #
    #         # Запускаем следующий раунд
    #         self.timer_round_thimble.start()
    #         return
    #
    #     css_path = "i[id='thimble3']"
    #     i = self.doc.findFirst(css_path)
    #     attr = i.attribute('class')
    #     if 'guessed' not in attr and 'empty' not in attr:
    #         self.click_tag(css_path)
    #     #     print(css_path)
    #     # else:
    #     #     print('посещено 1')
    #
    #     css_path = "i[id='thimble4']"
    #     i = self.doc.findFirst(css_path)
    #     attr = i.attribute('class')
    #     if 'guessed' not in attr and 'empty' not in attr:
    #         self.click_tag(css_path)
    #     #     print(css_path)
    #     # else:
    #     #     print('посещено 2')
    #
    #     css_path = "i[id='thimble5']"
    #     i = self.doc.findFirst(css_path)
    #     attr = i.attribute('class')
    #     if 'guessed' not in attr and 'empty' not in attr:
    #         self.click_tag(css_path)
    #     #     print(css_path)
    #     # else:
    #     #     print('посещено 3')
    #
    #     # # Запускаем следующий раунд
    #     # self.timer_round_thimble.start()
    #
    # # def select_thimbles(self):
    # #     import time
    # #
    # #     # loop = QEventLoop()
    # #     # self.finish_tag_click.connect(loop.quit)
    # #     # self.finish_tag_click.connect(lambda x=None: print('finish_tag_click'))
    # #
    # #     print(self.doc.findFirst('p[class="thimbles"]').toOuterXml())
    # #
    # #     css_path = "i[id='thimble3']"
    # #     i = self.doc.findFirst(css_path)
    # #     attr = i.attribute('class')
    # #     if 'guessed' not in attr and 'empty' not in attr:
    # #         self.click_tag(css_path)
    # #         print(css_path, self.doc.findFirst('p[class="thimbles"]').toOuterXml())
    # #         time.sleep(2)
    # #     else:
    # #         print('посещено 1')
    # #
    # #     # time.sleep(3)
    # #     # loop.exec_()
    # #
    # #     css_path = "i[id='thimble4']"
    # #     i = self.doc.findFirst(css_path)
    # #     attr = i.attribute('class')
    # #     if 'guessed' not in attr and 'empty' not in attr:
    # #         self.click_tag(css_path)
    # #         print(css_path, self.doc.findFirst('p[class="thimbles"]').toOuterXml())
    # #         time.sleep(2)
    # #     else:
    # #         print('посещено 2')
    # #
    # #     # time.sleep(3)
    # #     # loop.exec_()
    # #
    # #     css_path = "i[id='thimble5']"
    # #     i = self.doc.findFirst(css_path)
    # #     attr = i.attribute('class')
    # #     if 'guessed' not in attr and 'empty' not in attr:
    # #         self.click_tag(css_path)
    # #         print(css_path, self.doc.findFirst('p[class="thimbles"]').toOuterXml())
    # #         time.sleep(2)
    # #     else:
    # #         print('посещено 3')
    # #
    # #     # <i id="thimble3" class="icon thimble-closed-active thimble-guessed" data-id="3"></i>
    # #     # <i id="thimble4" class="icon thimble-closed-active thimble-empty" data-id="4"></i>
    # #     # <i id="thimble5" class="icon thimble-closed-active" data-id="5"></i>
    # #
