#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from PySide.QtCore import QObject, QTimer, Signal, QEventLoop
from common import get_logger, save_current_html


logger = get_logger('waitable')


class Waitable(QObject):
    """Класс используется задержки выполнения работы кода пока
    указанный элемента не будет найден в вебдокументе.

    Например, на сайте есть кнопка, которая подгружает какие-то данные и
    если мы хотим в одной функции кликнуть на кнопку и дождаться загрузки
    данных, можно использовать этот класс.
    """

    def __init__(self, mw):
        super().__init__()

        self._mw = mw
        self._doc = mw.doc
        self._found = False
        self._element = None

        # Осталось попыток
        self._attempts_remaining = None

        # # Функция проверки ожидания, если функция возвращает True, ожидание прекращается
        # self._wait_check_func = lambda doc, css_path: not doc.findFirst(css_path).isNull()

        self._timer = QTimer()
        self._timer.timeout.connect(self._found_tick)

        logger.debug('Текущий адрес: %s.', mw.current_url())

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

        # TODO: ВОЗМОЖНО, пригодится. Поиск и проверка определены в лямбде _wait_check_func
        # if self._wait_check_func(self._doc, self._element):
        #     logger.debug('Элемент найден.')
        #
        #     self.found = True
        #     self._timer.stop()
        #     self._finished_event_loop.emit()

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
            logger.debug('Текущий адрес: %s.', self._mw.current_url())
            logger.debug('Текущая страница сохранена в файл: %s.', save_current_html(self._doc))

            self._timer.stop()
            self._finished_event_loop.emit()

    # def wait(self, element, max_number_attempts=30, interval=1000, wait_check_func=None):
    def wait(self, element, max_number_attempts=30, interval=1000):
        """Функция завершается, когда element будет найден в вебдокументе и на это у
        нее есть max_number_attempts попыток.

        :param element: css путь поиск элемента
        :param max_number_attempts: максимальное количество попыток
        :param interval: интервал проверки
        :param wait_check_func: функция поиска элемента, ожидание прекращается, когда эта функция вернет True.
        Функция принимает 2 параметра QWebElement и css-путь к элементу, который проверяем.
        """

        logger.debug('Ищу элемент: %s. Количество попыток: %s. Интервал: %s.', element, max_number_attempts, interval)

        self._element = element
        self._found = False

        self._attempts_remaining = max_number_attempts

        # # Если фукнция определена, используем пользовательскую, а не стандартную
        # if wait_check_func is not None:
        #     self._wait_check_func = wait_check_func

        self._timer.start(interval)

        if not self._found:
            loop = QEventLoop()
            self._finished_event_loop.connect(loop.quit)
            loop.exec_()
