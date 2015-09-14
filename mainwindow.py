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
from factory_petric import FactoryPetric
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
# <form class="patrol" action="/alley/" method="post" id="patrolForm" inited="inited">
# <input type="hidden" name="action" value="patrol"><p><img src="/@/images/obj/set_new/hat1_m.png" align="left">В темных улочках столицы происходит <b>много событий</b>. Отправляйся <b>в патруль</b> на улицу, и кто знает, быть может тебя ждут веселые встречи и <b>ценные находки</b>.</p>
# <table class="process"><tbody><tr>
# <td class="label">Патрулирование:</td>
# <td class="progress"><div class="exp"><div class="bar"><div><div class="percent" style="width: 5%; " id="patrolbar"></div></div></div></div></td>
# <td class="value" timer="1714" timer2="1800" id="patrol" intitle="1" endtime="1441838940" process="1">00:28:35</td>
# </tr></tbody></table>
# <div style="margin:5px 0;" id="leave-patrol-button"><span class="button" onclick="alleyPatrolLeave();"><span class="f"><i class="rl"></i><i class="bl"></i><i class="brc"></i><div class="c">Улизнуть с патрулирования</div></span></span></div>
# <p>Ваши действия привлекли уличного мага Девида Блейна.
# 															</p><div class="button"><a class="f" href="/desert/" onclick="return AngryAjax.goToUrl(this, event);"><i class="rl"></i><i class="bl"></i><i class="brc"></i><div class="c">Далее</div></a></div><p></p>
# <p class="timeleft">Осталось времени на сегодня: 50 минут</p>
# <p class="major">Мажоры, привыкшие к бессонным ночным гулянкам, могут патрулировать вдвое больше. <a href="/stash/#major" onclick="return AngryAjax.goToUrl(this, event);">Стать мажором</a>.</p>
# <input type="hidden" name="__ajax" value="1"><input type="hidden" name="return_url" value="/alley/"></form>
#
#
# # Ищем кнопку 'Грабить караваны!' и кликаем на нее
# button = doc.findFirst('.desert .button')
# if button.isNull():
#     raise MoswarButtonIsMissError('Грабить караваны!')
#
# print(button.toPlainText())
# button.evaluateJavaScript('this.click()')
#
#
# <div id="content" class="desert"><div class="welcome">
# <i class="tlc"></i><i class="trc"></i><div class="block-rounded">
# <i class="blc"></i><i class="brc"></i><div class="text">
# <p>К сожалению, верблюды вас перехитрили, и вы не смогли ограбить караван.</p>
# <div style="text-align:center"><div class="button" onclick="AngryAjax.goToUrl('/alley/');"><span class="f"><i class="rl"></i><i class="bl"></i><i class="brc"></i><div class="c">Вернуться</div></span></div></div>
# </div>
# </div>
# <div class="jobs-points"></div></div></div>



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
        self.factory_petric = FactoryPetric(self)

        # Список действий бота
        self.name_action_dict = {
            'Закоулки': self.alley,
            'Площадь': self.square,
            'Метро': self.metro,
            'Завод': self.factory,
            'Задания': self.jobs,
            'Персонаж': self.player,
            'Хата': self.home,
            'Игра в наперстки': self.thimblerig.run,
            'Напасть': self.fight.run,
            'Ищем следующего противника': self.fight._next_enemy,
            'Восстановление жизней': self.restore_hp.run,
            # 'Варка нано-петриков': self.start_petriks,
            'Варка нано-петриков': self.factory_petric.run,
        }

        # Добавляем команды
        for command in sorted(self.name_action_dict):
            self.ui.commands_cb.addItem(command, self.name_action_dict[command])

        # Выполнение кода в окне "Выполнение скрипта"
        self.ui.button_exec.clicked.connect(lambda x=None: exec(self.ui.code.toPlainText()))

        # Таймер используемый для вызова функции для запуска задач
        self._task_timer = QTimer()
        self._task_timer.setInterval(3 * 60 * 1000)  # Каждые 3 минуты
        self._task_timer.timeout.connect(self._task_tick)

    def _task_tick(self):
        """Функция для запуска задач."""

        logger.debug('Запуск задач.')

        # TODO: настраивать лимиты, при которых деньги в руду сливаются через наперстки
        if self.money() >= 200000:
            self.thimblerig.run()
            return

        # TODO: проверять, что класс готов для запуска (is_ready)
        if self.fight.is_ready():
            self.fight.run()
            return

        # TODO: проверять, что класс готов для запуска (is_ready)
        if self.factory_petric.is_ready():
            self.factory_petric.run()
            return

    def _get_doc(self):
        return self.ui.view.page().mainFrame().documentElement()

    doc = property(_get_doc)

    def current_url(self):
        """Функция возвращает текущий адрес страницы."""

        return self.ui.view.url().toString()

    def wait_loading(self):
        """Функция ожидания загрузки страницы. Использовать только при изменении url."""

        logger.debug('Начинаю ожидание загрузки страницы.')

        # Ждем пока прогрузится страница
        loop = QEventLoop()
        self.ui.view.loadFinished.connect(loop.quit)
        loop.exec_()

        logger.debug('Закончено ожидание загрузки страницы.')

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

        logger.debug('Перехожу по адресу "%s"', url)

        self.ui.view.load(url)

        self.wait_loading()

    def auth(self):
        """Функция загружает страницу мосвара, заполняет поля логина и пароля и нажимает на кнопку Войти.
        После нажатия на Войти происходит ожидание загрузки страницы.

        """

        logger.debug('Авторизуюсь.')

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

        logger.debug('Запуск таймера выполнения задач.')

        # Запускаем выполнение задач
        self._task_timer.start()

        # # TODO: удалить, временно!
        # self.fight.run()
        #
        # self.timer = QTimer()
        # self.timer.setInterval(1000 * 60 * 20)  # каждые 20 минут
        # self.timer.timeout.connect(self.fight.run)
        # self.timer.start()

    def alley(self):
        self.go('alley')

    def square(self):
        self.go('square')

    # TODO: проверить корректность метода
    def factory(self):
        self.go('factory')

    def metro(self):
        self.go('metro')

    def jobs(self):
        self.go('nightclub/jobs')

    def player(self):
        self.go('player')

    def home(self):
        self.go('home')

    # # TODO: вынести в отдельный класс
    # def start_petriks(self):
    #     """Функция используется для производства нано-петриков."""
    #
    #     # TODO: варка петриков.
    #
    #     # Кнопка "Начать переработку"
    #     # TODO: не .petric использовать, а что-то с nanofactory
    #     button = self.doc.findFirst('.petric .button')
    #
    #     # Полоска прогресса переработки в нано-петрики
    #     progress = self.doc.findFirst('#petriksprocess')
    #
    #     # Если есть кнопка "Начать переработку", кликаем
    #     if not button.isNull():
    #         button.evaluateJavaScript("this.click()")
    #
    #     # Иначе, узнаем сколько осталось ждать
    #     elif not progress.isNull():
    #         # Сколько осталось секунд
    #         end_time = progress.attribute('timer')
    #         print('Осталось {} секунд'.format(end_time))
    #
    #     else:
    #         raise MoswarElementIsMissError('Не найдена кнопка "Начать переработку" и полоса '
    #                                        'прогресса переработки в нано-петрики')

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

        logger.debug('Выполняю клик по тегу: %s', css_path)

        # Используем для клика jQuery
        code = """
        tag = $("{}");
        tag.click();""".format(css_path)

        ok = self.doc.evaluateJavaScript(code)
        if ok is None:
            logger.warn('Выполнение js скрипта неудачно. Code:\n' + code)
