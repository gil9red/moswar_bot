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
        self._date_ready = None

        # Индекс выбора времени патрулирования. 1 единица равняется 10 минутам
        # Патрулируем по 40 минут
        self._job_times = 4

    def is_ready(self):
        """Возвращает True, если вызов метода run будет иметь смысл, иначе False."""

        # TODO: узнать сколько осталось патрулировать
        # process = self.doc.findFirst('.patrol .process .value')
        # self.slog(process.attribute('timer'))

        # TODO: проверять: print(self.doc.findFirst('.patrol .timeleft').toOuterXml())
        # <p class="timeleft">Осталось времени на сегодня: 120 минут</p>
        # self.ui.simple_log.clear()
        #
        # timeleft = self.doc.findFirst('.patrol .timeleft')
        # timeleft = timeleft.toPlainText()
        # self.slog(timeleft)
        #
        # import re
        # # Регулярка для удаления любых символов, кроме цифр от 0-9
        # timeleft = re.sub(r'[^\d]', '', timeleft)
        # self.slog('"{}"'.format(timeleft))

        # TODO: довести до ума
        if self._date_ready is None:
            self._mw.alley()

            # work = self._mw.doc.findFirst('.shaurburgers-work')
            # job_process = work.findFirst('.process .value')
            # if job_process.isNull():
            #     return True
            #
            # # TODO: повтор
            # error = work.findFirst('.time .error')
            # if not error.isNull() and 'На сегодня вы отработали свою максимальную смену' in error.toPlainText():
            #     # TODO: повтор
            #     # TODO: указывать точное время оставшееся до начала следующего дня
            #     self._date_ready = datetime.today() + timedelta(hours=3)
            #     logger.debug('На сегодня закончались часы работы в Шаурбургерсе.')
            #     return False
            #
            # # Сколько осталось секунд
            # timer = int(job_process.attribute('timer'))
            #
            # # TODO: повтор
            # # Указываем время до окончания работы, плюс 5 секунд -- на всякий
            # self._date_ready = datetime.today() + timedelta(seconds=timer + 5)
            #
            # logger.debug('До окончания работы в Шаурбургерсе осталось %s секунд.', timer)

        return datetime.today() >= self._date_ready

    def run(self):
        """Функция используется для Патрулирования."""

        if self._mw._used:
            logger.warn('Бот в данный момент занят процессом "%s". Выхожу из функции.', self._mw._used_process)
            return

        self._mw._used = True
        self._mw._used_process = "Патрулирование"

        logger.debug('Выполняю задание "%s".', self._mw._used_process)

        self._mw.alley()

        if self.is_ready():
            patrol = self._mw.doc.findFirst('.patrol')

            # TODO: сделать для патрулирования
            # # TODO: повтор
            # error = patrol.findFirst('.time .error')
            # if not error.isNull() and 'На сегодня вы отработали свою максимальную смену' in error.toPlainText():
            #     # TODO: повтор
            #     # TODO: указывать точное время оставшееся до начала следующего дня
            #     self._date_ready = datetime.today() + timedelta(hours=3)
            #     logger.debug('На сегодня закончались часы работы в Шаурбургерсе.')
            #     self._mw._used = False
            #     return False

            job_time = patrol.findFirst('select[name=time]')
            times = job_time.findAll('option').count()

            logger.info('Доступно %s минут патрулирования.', times * 10)

            # По-умолчанию, работаем self._job_times, если оставшееся время работы, меньше self._job_times,
            # работаем сколько можно
            select_times = self._job_times if times > self._job_times else times

            job_time.evaluateJavaScript("this.selectedIndex = {}".format(select_times - 1))
            logger.debug("Начинаю патрулировать %s минут.", select_times * 10)

            # TODO: повтор
            # Указываем время до окончания работы, плюс 5 секунд -- на всякий
            self._date_ready = datetime.today() + timedelta(minutes=select_times * 10, seconds=5)

            button = self.patrol.findFirst('#alley-patrol-button')
            button.evaluateJavaScript('this.click()')

        self._mw._used = False
