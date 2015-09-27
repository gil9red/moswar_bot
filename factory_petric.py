#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from datetime import datetime, timedelta
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
        """Возвращает True, если вызов метода run будет иметь смысл, иначе False."""

        if self._date_ready is None:
            # return True

            # Узнаем сколько осталось ждать переработки, и нужно ли вообще ждать
            # TODO: довести до ума

            self._mw.factory()

            # Полоска прогресса переработки в нано-петрики
            progress = self._mw.doc.findFirst('#petriksprocess')

            # Если не нашли полосу прогресса переработки, значит переработка закончена
            if progress.isNull():
                return True

            # Сколько осталось секунд
            timer = int(progress.attribute('timer'))

            # TODO: повтор
            # Указываем время готовности, плюс 5 секунд -- на всякий
            self._date_ready = datetime.today() + timedelta(seconds=timer + 5)

            logger.debug('До окончания переработки осталось %s секунд.', timer)

        return datetime.today() >= self._date_ready

    def run(self):
        """Функция используется для производства нано-петриков."""

        if self._mw._used:
            logger.warn('Бот в данный момент занят процессом "%s". Выхожу из функции.', self._mw._used_process)
            return

        # TODO: учеть моментальное проивзодство -- если есть 2 кнопки -- можем готовить
        # TODO: вызывать себя же в таймере, пока не появится полоса загрузки производства
        logger.debug('Выполняю переработку петриков.')

        self._mw.factory()

        # Проверяем перенаправление адресов
        if 'factory' not in self._mw.current_url():
            logger.warn('Перенаправление адреса на "%s". Выхожу из функции.', self._mw.current_url())
            return

        self._mw._used = True
        self._mw._used_process = "Производство нано-петриков"

        # TODO: путь %button% кликает лаборатна за 3 меда, что не очень хорошо -- нужно различать их и
        # кликать только переработку

        # Кнопка "Начать переработку"
        button = self._mw.doc.findFirst('.factory-nanoptric .button')

        # Полоска прогресса переработки в нано-петрики
        progress = self._mw.doc.findFirst('#petriksprocess')

        # Проверим, перерабатываются ли еще петрики
        if not progress.isNull():
            # Сколько осталось секунд
            timer = int(progress.attribute('timer'))

            # TODO: повтор
            # Указываем время готовности, плюс 5 секунд -- на всякий
            self._date_ready = datetime.today() + timedelta(seconds=timer + 5)

            logger.debug('До окончания переработки осталось %s секунд.', timer)

        # Иначе кликаем на кнопку "Начать переработку"
        elif not button.isNull():
            logger.debug('Нажимаю на кнопку "Начать переработку".')

            button.evaluateJavaScript("this.click()")

            # Указываем время готовности -- 1 час, плюс на всякий минуту добавим
            self._date_ready = datetime.today() + timedelta(hours=1, minutes=1)

        else:
            self._mw._used = False
            raise MoswarElementIsMissError('Не найдена кнопка "Начать переработку" и полоса '
                                           'прогресса переработки в нано-петрики')

        self._mw._used = False
