#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from datetime import datetime, timedelta
from common import get_logger


logger = get_logger('shaurburgers')


class Shaurburgers:
    """Класс для работы в Шаурбургерсе."""

    def __init__(self, mw):
        super().__init__()

        self._mw = mw

        # Время, когда возможна снова работать. Время используется локальное, а не серверное.
        self._date_ready = None

        # Сколько часов работать
        self._job_hours = 4

    def is_ready(self):
        """Возвращает True, если вызов метода run будет иметь смысл, иначе False."""

        # TODO: довести до ума
        if self._date_ready is None:
            if 'shaurburgers' not in self._mw.current_url():
                self._mw.go_shaurburgers()

            work = self._mw.doc.findFirst('.shaurburgers-work')
            job_process = work.findFirst('.process .value')
            if job_process.isNull():
                return True

            # TODO: повтор
            error = work.findFirst('.time .error')
            if not error.isNull() and 'На сегодня вы отработали свою максимальную смену' in error.toPlainText():
                # TODO: повтор
                # TODO: указывать точное время оставшееся до начала следующего дня
                self._date_ready = datetime.today() + timedelta(hours=3)
                logger.debug('На сегодня закончались часы работы в Шаурбургерсе.')
                return False

            # Сколько осталось секунд
            timer = int(job_process.attribute('timer'))

            # TODO: повтор
            # Указываем время до окончания работы, плюс 5 секунд -- на всякий
            self._date_ready = datetime.today() + timedelta(seconds=timer + 5)

            logger.debug('До окончания работы в Шаурбургерсе осталось %s секунд.', timer)

        return datetime.today() >= self._date_ready

    # TODO: проверить, что работает: работа в Шаурбургерсе
    def run(self):
        """Функция используется для работы в Шаурбургерсе."""

        if self._mw._used:
            logger.warn('Бот в данный момент занят процессом "%s". Выхожу из функции.', self._mw._used_process)
            return

        self._mw._used = True
        self._mw._used_process = "Работа в Шаурбургерсе"

        if 'shaurburgers' not in self._mw.current_url():
            self._mw.go_shaurburgers()

        if self.is_ready():
            work = self._mw.doc.findFirst('.shaurburgers-work')

            # TODO: повтор
            error = work.findFirst('.time .error')
            if not error.isNull() and 'На сегодня вы отработали свою максимальную смену' in error.toPlainText():
                # TODO: повтор
                # TODO: указывать точное время оставшееся до начала следующего дня
                self._date_ready = datetime.today() + timedelta(hours=3)
                logger.debug('На сегодня закончались часы работы в Шаурбургерсе.')
                self._mw._used = False
                return False

            job_time = work.findFirst('select[name=time]')
            hours = job_time.findAll('option').count()

            logger.info('Доступно %s часов работы в Шаурбургерсе.', hours)

            # По-умолчанию, работаем self._job_hours часа, если оставшееся время работы, меньше self._job_hours часов,
            # работаем сколько можно
            select_hours = self._job_hours if hours > self._job_hours else hours

            job_time.evaluateJavaScript("this.selectedIndex = {}".format(select_hours - 1))
            logger.debug("Начинаю работать в Шаурбургерсе %s часов.", select_hours)

            # TODO: повтор
            # Указываем время до окончания работы, плюс 5 секунд -- на всякий
            self._date_ready = datetime.today() + timedelta(hours=select_hours, seconds=5)

            self._mw.click_tag('.shaurburgers-work .button')

        self._mw._used = False
