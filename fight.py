#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from datetime import datetime, timedelta

from PySide.QtCore import QObject, Signal, QTimer, QEventLoop
from common import get_logger
from waitable import Waitable


logger = get_logger('fight')


class Fight(QObject):
    def __init__(self, mw):
        super().__init__()

        self._mw = mw

        # Кнопка "Отнять у слабого"
        self._css_path_button_fight = "div[class='button-big btn f1']"

        # Кнопка поедания сникерса
        self._css_path_button_snikers = 'div[onclick*=snikers]'

        # Таймер для ожидания загрузки страницы с выбором противника
        self._timer_enemy_load = QTimer()
        self._timer_enemy_load.setInterval(333)
        self._timer_enemy_load.timeout.connect(self._check_enemy_load)

        # Таймер для поиска противника
        self._timer_next_enemy = QTimer()
        self._timer_next_enemy.setInterval(1000)
        self._timer_next_enemy.setSingleShot(True)
        self._timer_next_enemy.timeout.connect(self._next_enemy)

        # TODO: remove
        # # Время, когда возможно нападение. Время используется локальное, а не серверное.
        # self._date_ready = None

    # Сигнал вызывается, когда противник на странице найден -- например, страница загрузилась
    _enemy_load_finished = Signal()

    # Сигнал вызывается, когда противник подходит для нападения
    _enemy_found = Signal()

    def is_ready(self):
        """Возвращает True, если вызов метода run будет иметь смысл -- можем напасть, иначе False."""

        # TODO: для того, чтобы метод self.fight.is_ready() работал правильно, текущим адресом должны
        # быть Закоулки -- метод has_snikers, используемый в is_ready работает только в Закоулках
        # Идем в Закоулки
        self._mw.alley()

        return self._timeout_fight() is None or self.has_snickers()

        # TODO: remove
        # print('self._date_ready:', self._date_ready)
        # print('datetime.today():', datetime.today())
        # if self._date_ready is not None:
        #     print('datetime.today() >= self._date_ready', datetime.today() >= self._date_ready)
        #
        # if self._date_ready is None:
        #     return True
        #
        # return datetime.today() >= self._date_ready

    def _timeout_fight(self):
        """Функция возвращает количество оставшихся секунд до возможности напасть.
        Если секунд осталось 0 или меньше 0, то вернется None."""

        for timeout in self._mw.doc.findAll('[id*=timeout]'):
            timer = timeout.attribute('timer')
            if timer and 'alley' in timeout.attribute('href'):
                timer = int(timer)
                return timer if timer > 0 else None

    def run(self):
        """Функция для нападения на игроков.

        Ищем слабого горожанина (заброшенного персонажа) -- не нужно привлекать внимание к боту.
        Уровень противника в пределах нашего +/- 1
        """

        # TODO: этот метод уже вызывается в is_ready
        # # Идем в Закоулки
        # self._mw.alley()

        # TODO: если есть таймер, и нельзя съесть сникерс, то выходим из функции
        if not self.is_ready() and not self.has_snickers():
            logger.debug('Нападать еще нельзя.')
            return

        # TODO: если есть тонус, использовать, чтобы сразу напасть
        # print(self._mw.doc.findFirst('div[onclick*=tonus]').toPlainText())

        # Если не получилось съесть Сникерс, восстанавливаем по старинке
        if not self.eat_snickers():
            if self._mw.current_hp() < self._mw.max_hp():
                self._mw.restore_hp.run()

        logger.debug('Нажимаю на кнопку "Отнять у слабого".')

        # Кликаем на кнопку "Отнять у слабого"
        self._mw.click_tag(self._css_path_button_fight)

        # Если не нашли подходящего противника, смотрим следующего
        if not self._check_enemy():
            self._timer_next_enemy.start()

            # Ожидаем пока противник не будет найден
            loop = QEventLoop()
            self._enemy_found.connect(loop.quit)
            loop.exec_()

        logger.debug('Нападаем на противника.')

        # Кликаем на кнопку "Напасть"
        self._mw.click_tag('.button-fight a')

        # Логируем результаты боя
        self.print_results()

        # TODO: remove
        # # После выполнения указываем, что доступ есть (правда, по таймерам это может и не быть)
        # self._date_ready = None

    def print_results(self):
        """Логируем результат боя."""

        # TODO: учитывать проигрыш

        result = '.result'

        # Ждем пока после клика прогрузится страница и появится элемент
        Waitable(self._mw.doc).wait(result)

        # Найдем элемент, в котором будут все результаты боя
        result = self._mw.doc.findFirst(result)

        # Сначала покажем выигранные монет и опыт, потом все остальное. Список используется для того, чтобы
        # порядок вывода результата боя был в порядке добавления элементов в этот список
        result_item_keys = ['Монеты', 'Опыт']

        result_dict = {
            'Монеты': result.findFirst('.tugriki').toPlainText().replace(',', ''),
            'Опыт': result.findFirst('.expa').toPlainText(),
        }

        # Искры не всегда будут -- обычно перед праздниками они появляются
        sparkles = result.findFirst('.sparkles')
        if not sparkles.isNull():
            result_item_keys.append('Искры')
            result_dict['Искры'] = sparkles.toPlainText()

        for img in result.findAll('.object-thumb'):
            obj = img.findFirst('img').attribute('alt')
            count = img.findFirst('.count').toPlainText()

            result_dict[obj] = count
            result_item_keys.append(obj)

        result_list = list()
        for key in result_item_keys:
            result_list.append('  {}: {}'.format(key, result_dict[key]))

        logger.debug('Результат боя:\n' + '\n'.join(result_list))

    # TODO: работает только в Закоулках
    def has_snickers(self):
        """Функция возвратит True, если можно съесть Сникерс, иначе False."""

        button = self._mw.doc.findFirst(self._css_path_button_snikers)
        return not button.isNull()

    def eat_snickers(self):
        """Функция для съедания Сникерса. Возвращает True, если получилось съесть, иначе False."""

        if self.has_snickers():
            logger.debug('Съедаю сникерс.')
            self._mw.click_tag(self._css_path_button_snikers)

            # Ждем пока после клика прогрузится страница и появится элемент
            Waitable(self._mw.doc).wait(self._css_path_button_fight)
            return True

        return False

    def _check_enemy_load(self):
        """Функция для ожидания загрузки страницы с выбором противника."""

        enemy = self._mw.doc.findFirst('.fighter2')

        # Если нашли элемент, описывающий противника
        if not enemy.isNull():
            self._enemy_load_finished.emit()
            self._timer_enemy_load.stop()

    def _check_enemy(self):
        """Функция ищет противника на текущей странице и проверяет его тип и уровень.
        Возвращает True если нашелся подходящий противник, иначе False.

        """

        self._timer_enemy_load.start()

        loop = QEventLoop()
        self._enemy_load_finished.connect(loop.quit)
        loop.exec_()

        # Определим тип противника -- нам нужен горожанин (нпс)
        is_npc = self._mw.doc.findFirst('.fighter2 .npc')
        is_npc = not is_npc.isNull()
        logger.info('Противник горожанин -> %s.', is_npc)

        # Узнаем уровень противника
        npc_level = self._mw.doc.findFirst('.fighter2 .level')
        npc_level = npc_level.toPlainText()
        npc_level = npc_level.replace('[', '').replace(']', '')
        npc_level = int(npc_level)
        logger.info('Уровень противники -> %s.', npc_level)

        # Проверяем, что нападаем на горожанина и разница в уровнях небольшая
        # found = is_npc and npc_level - 1 <= self._mw.level() <= npc_level + 1
        # TODO: Тупо ищем противника уровнем выше -- нужно получать максимальное количество искр
        found = is_npc and self._mw.level() + 1 == npc_level

        logger.info('Противник подходящий -> %s.', found)

        return found

    def _next_enemy(self):
        """Функция для поиска следующего противника."""

        logger.debug('Ищем следующего противника.')

        # Кликаем на кнопку "Искать другого"
        self._mw.click_tag(".button-search a")

        # Если нашли противника
        if self._check_enemy():
            self._enemy_found.emit()
            self._timer_next_enemy.stop()
        else:
            # Ищем дальше
            self._timer_next_enemy.start()
