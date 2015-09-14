#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from datetime import datetime, timedelta

# TODO: вынести в другой модуль, например, utils, или common
from common import get_logger, MoswarElementIsMissError


logger = get_logger('factory_petric')


class FactoryPetric:
    """Класс для производства нано-петриков."""

    def __init__(self, mw):
        super().__init__()

        self._mw = mw

        # Время, когда возможна переработка петриков. Время используется локальное, а не серверное.
        self._date_ready = None

    def is_ready(self):
        """Возвращает True, если вызов метода run будет иметь смысл -- можем напасть, иначе False."""

        if self._date_ready is None:
            return True

        return datetime.today() >= self._date_ready

    def run(self):
        """Функция используется для производства нано-петриков."""

        # TODO: учеть моментальное проивзодство -- если есть 2 кнопки -- можем готовить
        # TODO: вызывать себя же в таймере, пока не появится полоса загрузки производства
        logger.debug('Выполняю переработку петриков.')

        self._mw.factory()

        # Кнопка "Начать переработку"
        button = self._mw.doc.findFirst('.factory-nanoptric .button')

        # Полоска прогресса переработки в нано-петрики
        progress = self._mw.doc.findFirst('#petriksprocess')

        # Проверим, перерабатываются ли еще петрики
        if not progress.isNull():
            # Сколько осталось секунд
            timer = int(progress.attribute('timer'))

            # Указываем время готовности, плюс 5 секунд -- на всякий
            self._date_ready = datetime.today() + timedelta(seconds=timer + 5)

            logger.debug('До окончания переработки осталось %s секунд.', timer)

        # Иначе кликаем на кнопку "Начать переработку"
        elif not button.isNull():
            logger.debug('Нажимаю на кнопку "Начать переработку".')

            button.evaluateJavaScript("this.click()")

            # После выполнения указываем, что доступ есть (правда, по таймерам это может и не быть)
            self._date_ready = None
        else:
            raise MoswarElementIsMissError('Не найдена кнопка "Начать переработку" и полоса '
                                           'прогресса переработки в нано-петрики')
