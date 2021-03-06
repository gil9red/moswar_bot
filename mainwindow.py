#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'

import io
from urllib.parse import urljoin
from random import random, randint

from PySide.QtGui import *
from PySide.QtCore import *
from PySide.QtWebKit import *
from PySide.QtNetwork import QNetworkProxyFactory

from mainwindow_ui import Ui_MainWindow

from thimblerig import Thimblerig
from fight import Fight
from restore_hp import RestoreHP
from factory_petric import FactoryPetric
from shaurburgers import Shaurburgers
from patrol import Patrol
from common import *


# TODO: свой обработчик логов:
# http://python-lab.blogspot.ru/2013/03/blog-post.html
# http://stackoverflow.com/questions/2819791/how-can-i-redirect-the-logger-to-a-wxpython-textctrl-using-a-custom-logging-hand
# http://stackoverflow.com/questions/3118059/how-to-write-custom-python-logging-handler


# TODO: спорт-лото выигрыш, но без кнопки забирания выигрыша -- по ошибки тыкнул
# <div class="center clear">
# <h3>
# <div class="clear casino-sportloto-drawing" style="position:relative;">
# <div style="float:left; width:49%;">
# <div style="float:right; width:49%;">
# <table class="tickets list">
# <div id="prize-error" class="error" style="text-align:center; display: none;"></div>
# <p class="borderdata" style="margin:5px 0;">
# <div class="hint" style="text-align:center">Купите билетик на завтра</div>
# </div>
# </div>
# </div>


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


# TODO: научить бота покупать "шокочай" и жрать его -- для собирания коллекций
# positive_gifts = self.doc.findAll('.shop li[data-gift-category=positive]')
# if positive_gifts.count() == 0:
#     logger.warn("Подарки не найдены.")
#     return
#
# # Шоколадки «Пралине» #chocolates_17 (2500 тугриков 15 руды 25 нефти)
# # Шоколад #chocolates_12 (1000 тугриков 9 руды)
# # Шоколад #chocolates_11 (500 тугриков 9 руды)
# # Шоколад #chocolates_10 (100 тугриков 5 руды)
#
# # Чай в пирамидках #chocolates_16 (2500 тугриков 15 руды 25 нефти)
# # Чай #chocolates_15 (1000 тугриков 9 руды)
# # Чай #chocolates_14 (500 тугриков 9 руды)
# # Чай #chocolates_13 (100 тугриков 5 руды)
#
# # Кликаем на покупку
# self.click_tag('.shop #chocolates_13 .f')
#
# # Ищем диалог "Подарить подарок"
# present_dialog = self.doc.findFirst('#present-panel')
# if present_dialog.isNull():
#     logger.warn("Диалог дарения подарка не найден.")
#     return
#
# # Кнопка "Подарить"
# give = present_dialog.findFirst('[type=button]')
#
# # Нажимаем на кнопку
# give.evaluateJavaScript('this.click()')
#
#
# TODO: зайти в персонажа и открыть шокочаи
# TODO: зайти в персонажа и использовать чайные пакетики и шоколадные конфеты
#
# # TODO: идея неплохая, но id нужно заменить прямыми id, типа #chocolates_13
# # # Список id подарков типа "Чай" и "Шоколад", начиная с самых
# # # низкоуровневых
# # chocoteas = [
# #     "326",  # Чай (100 тугриков 5 руды)
# #     "327",  # Чай (500 тугриков 9 руды)
# #     "328",  # Чай (1000 тугриков 9 руды)
# #     "2936",  # Чай в пирамидках (2500 тугриков 15 руды 25 нефти)
# #
# #     "323",  # Шоколад (100 тугриков 5 руды)
# #     "324",  # Шоколад (500 тугриков 9 руды)
# #     "325",  # Шоколад (1000 тугриков 9 руды)
# #     "2937",  # Шоколадки «Пралине» (2500 тугриков 15 руды 25 нефти)
# # ]
# # chocoteas.clear()
# # for gift in positive_gifts:
# #     if gift.attribute("rel") in chocoteas:
# #         name = gift.findFirst("h2").toPlainText()
# #         print(name, gift.findFirst('.button').attribute('id'))


# TODO: прокачка вещей


logger = get_logger('moswar_bot')


class MainWindow(QMainWindow, QObject):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Все действия к прикрепляемым окнам поместим в меню
        for dock in self.findChildren(QDockWidget):
            self.ui.menuDockWindow.addAction(dock.toggleViewAction())

        # Все действия к toolbar'ам окнам поместим в меню
        for tool in self.findChildren(QToolBar):
            self.ui.menuTools.addAction(tool.toggleViewAction())

        self.progress_bar = QProgressBar()
        self.progress_bar_timer = QTimer()
        self.progress_bar_timer.setInterval(1000)
        self.progress_bar_timer.timeout.connect(lambda x=None: self.progress_bar.setValue(self.progress_bar.value() - 1))
        self.progress_bar.valueChanged.connect(lambda value: self.progress_bar_timer.stop() if self.progress_bar.value() <= 0 else None)
        self.ui.statusbar.addWidget(self.progress_bar)

        # TODO: показывать историю бота: self.view.history()

        self.moswar_url = 'http://www.moswar.ru/'

        # Чтобы не было проблем запуска компов с прокси:
        QNetworkProxyFactory.setUseSystemConfiguration(True)

        QWebSettings.globalSettings().setAttribute(QWebSettings.DeveloperExtrasEnabled, True)

        self.ui.view.urlChanged.connect(lambda x: self.ui.url_le.setText(x.toString()))
        self.ui.view.linkClicked.connect(lambda x: self.ui.url_le.setText(x.toString()))
        self.ui.pushButtonBackWebPage.clicked.connect(self.ui.view.back)

        # При клике на кнопку, мы получаем значение data текущего элемента и вызываем функцию, хранящуюся там
        self.ui.run_pb.clicked.connect(lambda: self.ui.commands_cb.itemData(self.ui.commands_cb.currentIndex())())

        self.thimblerig = Thimblerig(self)
        self.fight = Fight(self)
        self.restore_hp = RestoreHP(self)
        self.factory_petric = FactoryPetric(self)
        self.shaurburgers = Shaurburgers(self)
        self.patrol = Patrol(self)

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
            'Варка нано-петриков': self.factory_petric.run,
            'Убрать таймаут Тонусом': self.fight.use_tonus,
            'Шаурбургерс': self.shaurburgers.go,
            'Работать в Шаурбургерсе': self.shaurburgers.run,
            'Патрулировать': self.patrol.run,
        }

        # Добавляем команды
        for command in sorted(self.name_action_dict):
            self.ui.commands_cb.addItem(command, self.name_action_dict[command])

        # Выполнение кода в окне "Выполнение скрипта"
        self.ui.button_exec.clicked.connect(lambda x=None: exec(self.ui.code.toPlainText()))

        # Таймер используемый для вызова функции для запуска задач
        self._task_timer = QTimer()
        self._task_timer.setSingleShot(True)
        self._task_timer.timeout.connect(self._task_tick)

        self.ui.actionStartTimer.triggered.connect(self._task_tick)
        self.ui.actionStopTimer.triggered.connect(self._task_timer.stop)
        self.ui.actionStopTimer.triggered.connect(self.progress_bar_timer.stop)

        # Если стоит True -- происходит выполнение задачи и функция _task_tick прерывается
        self._used = False

        # Название процесса, из-за которого в данный момент  _task_tick не может выполниться
        self._used_process = None

        # Минимальная сумма для игры в Наперстки
        self.min_money_for_thimblerig = 200000

    def _task_tick(self):
        """Функция для запуска задач."""

        if self._used:
            logger.debug('Запуск задач отменяется -- процесс занят "%s".', self._used_process)
        else:
            logger.debug('Запуск задач.')

            try:
                # Если уже играем в Наперстки или набрали нужную сумму для игры в Наперстки
                if 'thimble' in self.current_url() or self.money() >= self.min_money_for_thimblerig:
                    self.thimblerig.run()

                elif self.shaurburgers.is_ready():
                    self.shaurburgers.run()

                elif self.patrol.is_ready():
                    self.patrol.run()

                elif self.factory_petric.is_ready():
                    self.factory_petric.run()

                elif self.fight.is_ready():
                    self.fight.run()

            except MoswarClosedError as e:
                logger.exception("Error:")

                # В случаи закрытия сайт, каждый час проверяем
                interval = 60 * 60 * 1000

            except MoswarBotError as e:
                logger.exception("Error:")

                # Возможно, в следующий раз ошибки не будет
                interval = 1 * 1000

            except Exception as e:
                logger.exception("Error:")

                # Возможно, в следующий раз ошибки не будет
                interval = 1 * 1000

            else:
                # TODO: настраивать interval: спрашивать у другиз модулей их таймауты (если есть) и выбирать
                # наименьший, он и будет interval. Если же interval не был изменен, то задавать рандомное время
                # Это позволит увеличить эффективность бота

                # Запускаем таймер выполнение задач
                # Следующий вызов будет случайным от 3 до 10 минут + немного случайных секунд
                interval = int((randint(3, 10) + random()) * 60 * 1000)

        self._start_task_timer(interval)

    def _start_task_timer(self, interval):
        secs = interval / 1000
        logger.debug('Повторный запуск задач через %s секунд.', secs)
        self._task_timer.start(interval)

        self.progress_bar.setRange(0, secs)
        self.progress_bar.setValue(secs)
        self.progress_bar_timer.start()

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

    def go(self, relative_url):
        """Функция для загрузки страниц.

        Если вызывать без параметров, то загрузит основную страницу.
        Если указывать relative_url, то он будет присоединен к адресу мосвара.
        Функция ожидание окончания загрузки страницы.

        Выбрасывает исключение MoswarClosedError, когда сайта закрыт (closed.html)

        """

        url = urljoin(self.moswar_url, relative_url)
        logger.debug('Перехожу по адресу "%s"', url)

        self.ui.view.load(url)
        self.wait_loading()

        # TODO: вынести обработку переадресаций в отдельную функцию
        # Проверяем, что не случилось переадресации. Она возможна, например, при игре
        # в наперстки или попадании в милицию
        current_url = self.current_url()

        # Сравниваем url'ы между собой. Такая проверка для обхода ситуации, когда QWebView отдает url
        # со слешем на конце. Если сравнить их обычной проверкой (== или !=), то это будет неправильно.
        # http://www.moswar.ru/shaurburgers/
        #
        # А сравниваем с:
        # http://www.moswar.ru/shaurburgers
        equal = url in current_url or current_url in url

        # Если адреса не равны
        if not equal:
            self.slog(url + " -> " + current_url)
            self.slog('Текущий заголовок: "{}"'.format(self.title()))
            logger.warn('Похоже, случилась переадресация: шли на %s, а попали на %s.', url, current_url)

            # TODO: Для http://www.moswar.ru/closed.html описывать причину -- брать из auth()
            # Проверка на временное отсутствие доступа к сайту
            if 'closed.html' in current_url:
                reason = self.doc.toPlainText().strip()
                logger.warn('Закрыто, причина:\n%s', reason)

                raise MoswarClosedError(reason)

            # TODO: руды может не хватать, поэтому предусмотреть ситуацию, когда придется платить деньгами
            # Обработка ситуации: Задержка за бои
            # url полиции police, но url'ы иногда неправильно возвращаются, поэтому надежнее смотреть
            # на заголовок страницы
            if self.title() == 'Милиция':
                logger.debug('Задержаны в милиции.')

                # Ищем кнопку для налаживания связей рудой
                button = self.doc.findFirst('.police-relations .button')
                if not button.isNull():
                    logger.debug('Плачу взятку рудой.')

                    # Нажать на кнопку что-то не получается, поэтому просто шлем запрос,
                    # который и так бы отослался при клике на кнопку
                    self.go('police/relations')

            # TODO: если новый уровень выпал в момент выполнения задания, то возможна такая неприятная
            # ситуация: попадаем на is_ready таски, делается переход к локации такси, перенапрявляет нас
            # на страницу поздравления, мы это определяем, кликаем на кнопку, в этот момент is_ready
            # возвращает True, и мы попадаем в функцию выполнения, которая снова переходит на страницу локации
            # и снова нас перенапрявляет, мы это определяем, кликаем и это так может случится несколько раз
            # TODO: возвращать признак перенаправления и по нему таска сама решает -- отменить или нет свое
            # выполнение
            #
            # Проверка на новый уровень
            if 'quest' in current_url:
                level_up = self.doc.findFirst('.levelup')
                if not level_up.isNull():
                    # Показать столько побед / награблено
                    for td in level_up.findAll('td'):
                        logger.debug('Получен новый уровень! Результат:\n' + ' '.join(td.toPlainText().split()))

                    # Ищем кнопку 'Вперед, к новым победам!' и кликаем на нее
                    button = self.doc.findFirst('.levelup .button')
                    if button.isNull():
                        raise MoswarButtonIsMissError('Вперед, к новым победам!')

                    button.evaluateJavaScript('this.click()')

    def auth(self):
        """Функция загружает страницу мосвара, заполняет поля логина и пароля и нажимает на кнопку Войти.
        После нажатия на Войти происходит ожидание загрузки страницы.

        """

        logger.debug('Авторизуюсь.')

        # Открываем страницу мосвара
        url = self.moswar_url
        logger.debug('Перехожу по адресу "%s"', url)

        self.ui.view.load(url)
        self.wait_loading()

        # Если закрыт доступ к сайту
        if 'closed.html' in self.current_url():
            logger.warn('Закрыто, причина:\n%s', self.doc.toPlainText().strip())

            # Попробуем снова авторизоваться через 1 час
            QTimer.singleShot(60 * 60 * 1000, self.auth)
            return

        login = self.doc.findFirst('#login-email')
        password = self.doc.findFirst('#login-password')

        if login.isNull() or password.isNull():
            raise MoswarAuthError('Не найдены поля логина и пароля.')

        login.setAttribute("value", LOGIN)
        password.setAttribute("value", PASSWORD)

        submit = self.doc.findFirst("input[type=submit]")
        if submit.isNull():
            raise MoswarButtonIsMissError('Войти')

        logger.debug('Захожу в игру.')
        submit.evaluateJavaScript("this.click()")

        self.wait_loading()

        logger.debug('Запуск таймера выполнения задач.')

        # Выполнение первых задач
        self._task_tick()

    def alley(self):
        self.go('alley')

    def square(self):
        self.go('square')

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

    def name(self):
        """Функция возвращает имя текущего персонажа."""

        try:
            css_path = '#personal .name'
            name = self.doc.findFirst(css_path).toPlainText()
            name = name[:name.rindex('[')]
            return name.strip()
        except Exception as e:
            raise MoswarElementIsMissError(e)

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

    def title(self):
        """Функция возвращает заголовок текущей страницы."""

        title = self.doc.findFirst('head title')
        if title.isNull():
            logger.warn('Не найден заголовок текущей страницы (%s).', self.current_url())

        return title.toPlainText()

    # TODO: добавить возможность выбрать область поиска элемента для клика, а то она все время вся страница -- self.doc
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

    def alert(self, text):
        """Функция показывает окно сообщений в браузере, используя javascript функцию alert."""

        self.doc.evaluateJavaScript('alert("{}")'.format(text))

    def slog(self, *args, **kwargs):
        """Функция для добавления текста в виджет-лог, находящегося на форме."""

        # Используем стандартный print для печати в строку
        str_io = io.StringIO()
        kwargs['file'] = str_io
        kwargs['end'] = ''

        print(*args, **kwargs)

        text = str_io.getvalue()
        self.ui.simple_log.appendPlainText(text)

    def read_settings(self):
        # TODO: при сложных настройках, лучше перейти на json или yaml
        config = QSettings(CONFIG_FILE, QSettings.IniFormat)
        self.restoreState(config.value('MainWindow_State'))
        self.restoreGeometry(config.value('MainWindow_Geometry'))

    def write_settings(self):
        config = QSettings(CONFIG_FILE, QSettings.IniFormat)
        config.setValue('MainWindow_State', self.saveState())
        config.setValue('MainWindow_Geometry', self.saveGeometry())

    def closeEvent(self, *args, **kwargs):
        self.write_settings()
        super().closeEvent(*args, **kwargs)
