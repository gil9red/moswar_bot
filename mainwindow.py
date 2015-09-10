#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'

from urllib.parse import urljoin

from PySide.QtGui import *
from PySide.QtCore import *
from PySide.QtWebKit import *
from PySide.QtNetwork import QNetworkProxyFactory

from mainwindow_ui import Ui_MainWindow

from thimblerig import Thimblerig
from fight import Fight
from restore_hp import RestoreHP
from utils import get_logger


class MoswarBotError(Exception):
    pass


class MoswarElementIsMissError(MoswarBotError):
    pass


class MoswarButtonIsMissError(MoswarElementIsMissError):
    def __init__(self, title_button):
        super().__init__('Не найдена кнопка "{}".'.format(title_button))


class MoswarAuthError(MoswarBotError):
    pass


LOGIN = 'ilya.petrash@inbox.ru'
PASSWORD = '0JHQu9GPRnVjazop'



# TODO: level up:
# <div id="content" class="levelup">
# После левел апа нужно кликнуть на: <button class="button" type="submit">
# doc = view.page().mainFrame().documentElement()
# level_up = doc.findFirst('.levelup')
# if not level_up.isNull():
#     # Показать столько побед / награблено
#     for td in level_up.findAll('td'):
#         print(' '.join(td.toPlainText().split()))
#
#     # Ищем кнопку 'Вперед, к новым победам!' и кликаем на нее
#     button = doc.findFirst('.levelup .button')
#     if button.isNull():
#         raise MoswarButtonIsMissError('Вперед, к новым победам!')
#
#     button.evaluateJavaScript('this.click()')


# TODO: ограбление корованов: http://www.moswar.ru/desert/
# # Ищем кнопку 'Грабить караваны!' и кликаем на нее
# button = doc.findFirst('.desert .button')
# if button.isNull():
#     raise MoswarButtonIsMissError('Грабить караваны!')
#
# print(button.toPlainText())
# button.evaluateJavaScript('this.click()')
#
# TODO: ограбление проходит в этапа: при патрулировании кликаешь на ограбление корованов и кнопку в
# всплывающем окне, показывающем сколько награблено. Вот этого второго информативного окна нет.



# TODO: кубович на любой странице:
# <div id="leftblock">
# <div id="personal" class="small">
# <div id="tutorial-pers">
# <div class="side-invite">
# <a style="text-decoration:none;" href="/casino/kubovich/" onclick="return AngryAjax.goToUrl(this, event);">
# <div class="side-fractionwar" style="color:#89deff; background:url(/@/images/link/kubovich.jpg) #2a66a1 no-repeat;"> Приз в студию! </div>
#
# TODO: крутить барабан:
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


# TODO: удалить всех из http://www.moswar.ru/phone/contacts/victims/2/
# у которых награда меньше 15к


# TODO: бесплатный спортлото: http://www.moswar.ru/casino/sportloto/


logger = get_logger('moswar_bot')


class MainWindow(QMainWindow, QObject):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.moswar_url = 'http://www.moswar.ru/'

        # Чтобы не было проблем запуска компов с прокси:
        QNetworkProxyFactory.setUseSystemConfiguration(True)

        QWebSettings.globalSettings().setAttribute(QWebSettings.DeveloperExtrasEnabled, True)

        self.ui.view.urlChanged.connect(lambda x: self.ui.url_le.setText(x.toString()))
        self.ui.view.linkClicked.connect(lambda x: self.ui.url_le.setText(x.toString()))

        # При клике на кнопку, мы получаем значение data текущего элемента и вызываем функцию, хранящуюся там
        self.ui.run_pb.clicked.connect(lambda: self.ui.commands_cb.itemData(self.ui.commands_cb.currentIndex())())

        self.thimblerig = Thimblerig(self)
        self.fight = Fight(self)
        self.restore_hp = RestoreHP(self)

        # Список действий бота
        self.name_action_dict = {
            'Закоулки': self.alley,
            'Площадь': self.square,
            'Метро': self.metro,
            'Задания': self.jobs,
            'Персонаж': self.player,
            'Хата': self.home,
            'Игра в наперстки': self.thimblerig.run,
            'Напасть': self.fight.run,
            'Ищем следующего противника': self.fight._next_enemy,
            'Восстановление жизней': self.restore_hp.run,
            'Варка нано-петриков': self.start_petriks,
        }

        # Добавляем команды
        for command in sorted(self.name_action_dict):
            self.ui.commands_cb.addItem(command, self.name_action_dict[command])

        # Выполнение кода в окне "Выполнение скрипта"
        self.ui.button_exec.clicked.connect(lambda x=None: exec(self.ui.code.toPlainText()))

    def _get_doc(self):
        return self.ui.view.page().mainFrame().documentElement()

    doc = property(_get_doc)

    def current_url(self):
        """Функция возвращает текущий адрес страницы."""

        return self.ui.view.url().toString()

    def wait_loading(self):
        """Функция ожидания загрузки страницы. Использовать только при изменении url."""

        # Ждем пока прогрузится страница
        loop = QEventLoop()
        self.ui.view.loadFinished.connect(loop.quit)
        loop.exec_()

    def go(self, relative_url=None):
        """Функция для загрузки страниц.

        Если вызывать без параметров, то загрузит основную страницу.
        Если указывать relative_url, то он будет присоединен к адресу мосвара.
        Функция ожидание окончания загрузки страницы.

        """

        if relative_url is None:
            url = self.moswar_url
        else:
            url = urljoin(self.moswar_url, relative_url)

        self.ui.view.load(url)

        self.wait_loading()

    def auth(self):
        """Функция загружает страницу мосвара, заполняет поля логина и пароля и нажимает на кнопку Войти.
        После нажатия на Войти происходит ожидание загрузки страницы.

        """

        # Открываем страницу мосвара
        self.go()

        login = self.doc.findFirst('#login-email')
        password = self.doc.findFirst('#login-password')

        if login.isNull() or password.isNull():
            raise MoswarAuthError('Не найдены поля логина и пароля.')

        login.setAttribute("value", LOGIN)
        password.setAttribute("value", PASSWORD)

        submit = self.doc.findFirst("input[type=submit]")
        if submit.isNull():
            raise MoswarButtonIsMissError('Войти')

        submit.evaluateJavaScript("this.click()")

        self.wait_loading()


        # TODO: удалить, временно!
        self.fight.run()

        self.timer = QTimer()
        self.timer.setInterval(1000 * 60 * 20)  # каждые 20 минут
        self.timer.timeout.connect(self.fight.run)
        self.timer.start()

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

    def start_petriks(self):
        """Функция используется для производства нано-петриков."""

        # TODO: варка петриков.

        # Кнопка "Начать переработку"
        button = self.doc.findFirst('.petric .button')

        # Полоска прогресса переработки в нано-петрики
        progress = self.doc.findFirst('#petriksprocess')

        # Если есть кнопка "Начать переработку", кликаем
        if not button.isNull():
            button.evaluateJavaScript("this.click()")

        # Иначе, узнаем сколько осталось ждать
        elif not progress.isNull():
            # Сколько осталось секунд
            end_time = progress.attribute('timer')
            print('Осталось {} секунд'.format(end_time))

        else:
            raise MoswarElementIsMissError('Не найдена кнопка "Начать переработку" и полоса '
                                           'прогресса переработки в нано-петрики')

    def money(self):
        """Функция возвращает количество денег персонажа."""

        try:
            css_path = '.tugriki-block'
            tugriki = self.doc.findFirst(css_path)
            tugriki = tugriki.attribute('title')
            tugriki = tugriki.split(': ')[-1]
            return int(tugriki)

        except Exception as e:
            raise MoswarElementIsMissError(e)

    def current_hp(self):
        """Функция возвращает текущее количество жизней персонажа."""

        try:
            css_path = '#personal #currenthp'
            hp = self.doc.findFirst(css_path)
            hp = hp.toPlainText()
            return int(hp)

        except Exception as e:
            raise MoswarElementIsMissError(e)

    def max_hp(self):
        """Функция возвращает текущее количество жизней персонажа."""

        try:
            hp = self.doc.findFirst('#personal #maxhp')
            hp = hp.toPlainText()
            return int(hp)

        except Exception as e:
            raise MoswarElementIsMissError(e)

    def level(self):
        """Функция возвращает уровень персонажа."""

        try:
            level = self.doc.findFirst('#personal b').toPlainText()
            level = level.split()[-1]
            level = level.replace('[', '').replace(']', '')
            return int(level)

        except Exception as e:
            raise MoswarElementIsMissError(e)

    def click_tag(self, css_path):
        """Функция находит html тег по указанному пути и эмулирует клик на него.

        Строки в css_path нужно оборачивать в апострофы.
        Пример:
            # Кликаем на кнопку "Отнять у слабого"
            self.click_tag("div[class='button-big btn f1']")

            # Кликаем на кнопку "Искать другого"
            self.click_tag(".button-search a")
        """

        # Используем для клика jQuery
        code = """
        tag = $("{}");
        tag.click();""".format(css_path)

        ok = self.doc.evaluateJavaScript(code)
        if ok is None:
            logger.warn('Выполнение js скрипта неудачно. Code:\n' + code)
