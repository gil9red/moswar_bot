#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from datetime import datetime, timedelta
from common import get_logger


logger = get_logger('patrol')


# TODO: сделать
class Patrol:
    """Класс для походов в Патруль."""

    def __init__(self, mw):
        super().__init__()

        self._mw = mw

        # Время, когда возможна снова работать. Время используется локальное, а не серверное.
        self._date_ready = datetime.today()

        # Индекс выбора времени патрулирования. 1 единица равняется 10 минутам
        # Патрулируем по 40 минут
        self._job_times = 4

    # TODO: также упростить в shaurburgers.py
    def is_ready(self):
        """Возвращает True, если вызов метода run будет иметь смысл, иначе False."""

        # Если еще патрулируем -- не готовы
        if datetime.today() < self._date_ready:
            return False

        self._mw.alley()

        patrol = self._mw.doc.findFirst('.patrol')

        # Если есть кнопка запуска патрулирования -- готовы
        button = patrol.findFirst('#alley-patrol-button')
        if not button.isNull():
            return True

        # Проверяем на полосу прогресса патрулирования
        process = patrol.findFirst('.process .value')
        if not process.isNull():
            timer = int(process.attribute('timer'))
            logger.debug('До окончания патрулирования осталось %s секунд.', timer)

            # Указываем время до окончания, плюс 5 секунд -- на всякий
            self._date_ready = datetime.today() + timedelta(seconds=timer + 5)
            return False

        timeleft = patrol.findFirst('.timeleft').toPlainText()
        if 'На сегодня Вы уже истратили все время патрулирования.' in timeleft:
            # TODO: указать self._date_ready на следующий день
            logger.debug(timeleft)

        return False

    def run(self):
        """Функция используется для Патрулирования."""

        if self._mw._used:
            logger.warn('Бот в данный момент занят процессом "%s". Выхожу из функции.', self._mw._used_process)
            return

        self._mw._used = True
        self._mw._used_process = "Патрулирование"

        logger.debug('Выполняю задание "%s".', self._mw._used_process)

        # Если готовы, выбираем время патрулирования и жмем на кнопку "Начать патрулирование"
        if self.is_ready():
            patrol = self._mw.doc.findFirst('.patrol')

            job_time = patrol.findFirst('select[name=time]')
            times = job_time.findAll('option').count()

            logger.info('Доступно %s минут патрулирования.', times * 10)

            # По-умолчанию, работаем self._job_times, если оставшееся время работы, меньше self._job_times,
            # работаем сколько можно
            select_times = self._job_times if times > self._job_times else times

            job_time.evaluateJavaScript("this.selectedIndex = {}".format(select_times - 1))
            logger.debug("Начинаю патрулировать %s минут.", select_times * 10)

            # Указываем время до окончания, плюс 5 секунд -- на всякий
            self._date_ready = datetime.today() + timedelta(minutes=select_times * 10, seconds=5)

            button = patrol.findFirst('#alley-patrol-button')
            button.evaluateJavaScript('this.click()')

        self._mw._used = False
