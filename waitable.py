#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from PySide.QtCore import QObject, QTimer, Signal, QEventLoop


# TODO: логиование
# TODO: ограничение времени / количества работы класса


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

        self._timer = QTimer()
        self._timer.setInterval(333)
        self._timer.timeout.connect(self._found_tick)

    # Сигнал нужен для прерывания QEventLoop'а, вызывается, когда
    # требуемый элемент найден
    _element_found = Signal()

    def _found_tick(self):
        """Функция с переодичностью в 333 мс вызывается таймером и ищет указанный элемент.
        Вызывает сигнал _element_found и останавливает таймер если элемент найден.
        """

        if not self._element:
            print('Элемент не указан')
            self._timer.stop()
            return

        if not self._doc:
            print('Документ не указан')
            self._timer.stop()
            return

        # Ищем элемент
        element = self._doc.findFirst(self._element)

        if not element.isNull():
            self.found = True
            self._timer.stop()
            self._element_found.emit()

    def wait(self, element):
        """Функция завершается только тогда, когда element будет найден в вебдокументе."""

        self._element = element
        self._found = False

        print('Начинаю искать элемент:', self._element)

        self._timer.start(333)

        if not self._found:
            loop = QEventLoop()
            self._element_found.connect(loop.quit)
            loop.exec_()
