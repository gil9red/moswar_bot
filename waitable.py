#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from PySide.QtCore import QObject, QTimer, Signal, QEventLoop
from common import get_logger


logger = get_logger('waitable')


class Waitable(QObject):
    """Класс используется задержки выполнения работы кода пока
    указанный элемента не будет найден в вебдокументе.

    Например, на сайте есть кнопка, которая подгружает какие-то данные и
    если мы хотим в одной функции кликнуть на кнопку и дождаться загрузки
    данных, можно использовать этот класс.
    """

    def __init__(self, doc):
        super().__init__()

        self._doc = doc
        self._found = False
        self._element = None

        # Осталось попыток
        self._attempts_remaining = None

        self._timer = QTimer()
        self._timer.setInterval(333)
        self._timer.timeout.connect(self._found_tick)

    # Сигнал нужен для прерывания QEventLoop'а
    _finished_event_loop = Signal()

    def _found_tick(self):
        """Функция с переодичностью в 333 мс вызывается таймером и ищет указанный элемент.
        Вызывает сигнал _element_found и останавливает таймер если элемент найден.
        """

        if not self._element:
            logger.warn('Элемент не указан.')
            self._timer.stop()
            return

        if not self._doc:
            logger.warn('Документ не указан.')
            self._timer.stop()
            return

        # Ищем элемент
        element = self._doc.findFirst(self._element)

        if not element.isNull():
            logger.debug('Элемент найден.')

            self.found = True
            self._timer.stop()
            self._finished_event_loop.emit()

        self._attempts_remaining -= 1
        if self._attempts_remaining == 0:
            logger.warn('Закончилось количество попыток найти элемент: %s.', self._element)
            self._timer.stop()
            self._finished_event_loop.emit()

    def wait(self, element, max_number_attempts=10):
        """Функция завершается element будет найден в вебдокументе и на это у нее
        есть max_number_attempts попыток."""

        logger.debug('Ищу элемент: %s. Количество попыток: %s.', element, max_number_attempts)

        self._element = element
        self._found = False

        self._attempts_remaining = max_number_attempts

        self._timer.start(333)

        if not self._found:
            loop = QEventLoop()
            self._finished_event_loop.connect(loop.quit)
            loop.exec_()
