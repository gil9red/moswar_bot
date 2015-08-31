#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import time
from PySide.QtCore import QTimer, Signal, QEventLoop
from mainwindow import get_logger


logger = get_logger('thimblerig')


class Thimblerig:
    """Класс для игры в наперстки в мосваре."""

    def __init__(self, mw):
        self.mw = mw

        # Таймер для отсчета раундов игры
        self._timer_round_thimble = QTimer()
        self._timer_round_thimble.setInterval(1000)
        self._timer_round_thimble.setSingleShot(True)
        self._timer_round_thimble.timeout.connect(self.nine_thimble)

        # Таймер для выбора наперстков
        self._timer_thimble = QTimer()
        self._timer_thimble.setInterval(1000)
        self._timer_thimble.timeout.connect(self.select_thimble)

        # TODO: добавить игре в наперстки немного рандома
        self.ruda_count = 0
        self.thimble_round_count = 0

    finished_thimble_game = Signal()

    def run(self):
        """Игра в наперстки."""

        if self.mw.current_url() == 'http://www.moswar.ru/thimble/':
            return

        t = time.clock()

        # Эмулируем клик на кнопку "Начать играть"
        self.mw.go('thimble/start')

        # Ждем пока прогрузится страница
        loop = QEventLoop()
        # TODO: от mv напрямую или сигнал loadFinished ловить, или иметь доступ к view
        self.mw.ui.view.loadFinished.connect(loop.quit)
        loop.exec_()

        self.ruda_count = 0
        self.thimble_round_count = 0

        self._timer_round_thimble.start()

        # Ждем пока закончится игра
        loop = QEventLoop()
        self.finished_thimble_game.connect(loop.quit)
        loop.exec_()

        logger.debug('Длительность игры {:.1f} секунд'.format(time.clock() - t))
        logger.debug('Игра в наперстки закончилась за {} раундов'.format(self.thimble_round_count))
        logger.debug('Угадано {} руды. Потрачено {} тугриков.'.format(self.ruda_count, self.thimble_round_count * 1500))
        logger.debug('Удача {:.2f}%'.format(self.ruda_count / (self.thimble_round_count * 3) * 100))

        # Эмулируем клик на кнопку "Я наигрался, хватит"
        self.mw.go('thimble/leave')

    def nine_thimble(self):
        """Функция для начала игры в девять наперстков."""

        if self.mw.money() < 3000:
            self._timer_thimble.stop()
            logger.debug("Заканчиваю игру.")
            self.finished_thimble_game.emit()
            return

        self.thimble_round_count += 1

        css_path = "div[id='thimble-controls-buttons'] div[data-count='9']"
        self.mw.click_tag(css_path)

        self._timer_thimble.start()

    def select_thimble(self):
        """Функция для клика на один из наперстков."""

        doc = self.mw.doc

        # Количество оставшихся попыток. Для девяти наперсток их максимум будет 3
        left = doc.findFirst('span[id="naperstki-left"]').toInnerXml()

        # Если количество попыток равно 0, то останавливаем таймер клика на наперстки
        if left == '0':
            self._timer_thimble.stop()

            # Получаем количество угаданной за раунд руды
            ruda = doc.findFirst('span[id="naperstki-ruda"]').toPlainText()
            self.ruda_count += int(ruda)
            logger.info("Раунд {}. Угадано {} руды.".format(self.thimble_round_count, ruda))

            # Запускаем следующий раунд
            self._timer_round_thimble.start()
            return

        css_path = "i[id='thimble3']"
        i = doc.findFirst(css_path)
        attr = i.attribute('class')
        if 'guessed' not in attr and 'empty' not in attr:
            self.mw.click_tag(css_path)

        css_path = "i[id='thimble4']"
        i = doc.findFirst(css_path)
        attr = i.attribute('class')
        if 'guessed' not in attr and 'empty' not in attr:
            self.mw.click_tag(css_path)

        css_path = "i[id='thimble5']"
        i = doc.findFirst(css_path)
        attr = i.attribute('class')
        if 'guessed' not in attr and 'empty' not in attr:
            self.mw.click_tag(css_path)
