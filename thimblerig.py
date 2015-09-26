#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import random
import time
from PySide.QtCore import QObject, QTimer, Signal, QEventLoop
from common import get_logger


logger = get_logger('thimblerig')


# TODO: Уменьшить время выбора наперстков


class Thimblerig(QObject):
    """Класс для игры в наперстки в мосваре."""

    def __init__(self, mw):
        super().__init__()

        self._mw = mw

        # Таймер для отсчета раундов игры
        self._timer_round_thimble = QTimer()
        self._timer_round_thimble.setInterval(1000)
        self._timer_round_thimble.setSingleShot(True)
        self._timer_round_thimble.timeout.connect(self.nine_thimble)

        # Таймер для выбора наперстков
        self._timer_thimble = QTimer()
        self._timer_thimble.setInterval(1000)
        self._timer_thimble.timeout.connect(self.select_thimbles)

        # Варианты порядка открытия наперстков
        self._variants = [
            # С первого по третий ряд
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],

            # Диагонально
            [0, 4, 8],
            [6, 4, 2],
        ]

        # Номера наперстков, которые будет открывать бот
        self._thimble1, self._thimble2, self._thimble3 = 0, 0, 0

        self._ruda_count = 0
        self._thimble_round_count = 0

    finished_thimble_game = Signal()

    def _get_ruda_count(self):
        return self._ruda_count

    def _get_thimble_round_count(self):
        return self._thimble_round_count

    ruda_count = property(_get_ruda_count)

    thimble_round_count = property(_get_thimble_round_count)

    def run(self):
        """Игра в наперстки."""

        if self._mw._used:
            logger.warn('Бот в данный момент занят процессом "%s". Выхожу из функции.', self._mw._used_process)
            return

        logger.debug('Начинаю игру в Наперстки.')

        self._mw._used = True
        self._mw._used_process = "Игра в наперстки"

        t = time.clock()

        # Эмулируем клик на кнопку "Начать играть"
        if 'thimble' not in self._mw.current_url():
            self._mw.go('thimble/start')

        # TODO: проверять на сообщение которое говорит, что билеты для игры закончились
# <div class="alert infoalert alert-error alert1" rel="" style="display: block; top: 428px;" data-bind-move="1">
# <div class="padding">
# <h2 id="alert-title">Ошибка</h2>
# <div class="data">
# <div id="alert-text">
# Вы сегодня уже играли в наперстки с Моней Шацом много раз, и его интерес к вам сильно поубавился. Но если же вы хотите во что бы то ни стало рискнуть еще разок, то
# <a href="/berezka/" onclick="return AngryAjax.goToUrl(this, event);">купите билетик</a>
# в Березке.
# </div>
# <div class="actions">
# </div>
# </div>
# </div>

        # TODO: проверить, что работает
        for el in self._mw.doc.findAll('.alert'):
            text = el.findFirst('#alert-text')
            if not text.isNull() and 'Вы сегодня уже играли в наперстки с Моней Шацом' in text.toPlainText():
                logger.warn('Закончились билеты для игры в наперстки.')
                self._mw._used = False
                return

        self._ruda_count = 0
        self._thimble_round_count = 0

        self._timer_round_thimble.start()

        # Ждем пока закончится игра
        loop = QEventLoop()
        self.finished_thimble_game.connect(loop.quit)
        loop.exec_()

        logger.debug('Длительность игры {:.1f} секунд'.format(time.clock() - t))
        logger.debug('Игра в наперстки закончилась за {} раундов'.format(self._thimble_round_count))
        logger.debug('Угадано {} руды. Потрачено {} тугриков.'.format(self._ruda_count,
                                                                      self._thimble_round_count * 1500))
        logger.debug('Удача {:.2f}%'.format(self._ruda_count / (self._thimble_round_count * 3) * 100))

        # Эмулируем клик на кнопку "Я наигрался, хватит"
        self._mw.go('thimble/leave')

        self._mw._used = False

    def nine_thimble(self):
        """Функция для начала игры в девять наперстков."""

        # TODO: нижний предел суммы сделать настраивым
        if self._mw.money() < 3000:
            self._timer_thimble.stop()
            logger.debug("Заканчиваю игру.")
            self.finished_thimble_game.emit()
            return

        self._thimble_round_count += 1

        # Выбираем кнопку для игры в 9 наперстков
        css_path = "#thimble-controls-buttons div[data-count='9']"
        self._mw.click_tag(css_path)

        # Выбираем случайный ряд наперстков
        numbers_thimble = random.choice(self._variants)

        # Порядок кликания на наперстки. Если True, то справа на лево
        right_to_left = random.choice([True, False])

        if right_to_left:
            numbers_thimble.sort(reverse=True)

        self._thimble1, self._thimble2, self._thimble3 = ["#thimble{}".format(i) for i in numbers_thimble]
        logger.info('Порядок открытия наперстков: {}, {}, {}'.format(self._thimble1, self._thimble2, self._thimble3))

        self._timer_thimble.start()

    def _check_click_thimble(self, css_path):
        """Функция, вернет True, если на Наперсток уже кликали."""

        tag = self._mw.doc.findFirst(css_path)
        attr = tag.attribute('class')

        # Проверяем, что на наперсток кликнули
        check = 'guessed' in attr or 'empty' in attr

        logger.info('Проверяем наперсток "%s". Атрибут элемента: "%s". -> "%s".', css_path, attr, check)
        return check

    def select_thimbles(self):
        """Функция для клика на наперстки."""

        doc = self._mw.doc

        # Количество оставшихся попыток. Для девяти наперсток их максимум будет 3
        left = doc.findFirst('#naperstki-left').toInnerXml()

        # Если количество попыток равно 0, то останавливаем таймер клика на наперстки
        if left == '0':
            self._timer_thimble.stop()

            # Получаем количество угаданной за раунд руды
            ruda = doc.findFirst('#naperstki-ruda').toPlainText()
            self._ruda_count += int(ruda)
            logger.info("Раунд {}. Угадано {} руды.".format(self._thimble_round_count, ruda))

            # Запускаем следующий раунд
            self._timer_round_thimble.start()
            return

        # Проверяем, что на наперсток не кликали и кликаем
        if not self._check_click_thimble(self._thimble1):
            self._mw.click_tag(self._thimble1)
        elif not self._check_click_thimble(self._thimble2):
            self._mw.click_tag(self._thimble2)
        elif not self._check_click_thimble(self._thimble3):
            self._mw.click_tag(self._thimble3)
