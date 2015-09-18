#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from urllib.parse import urljoin

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

        # Кнопка поедания Сникерса
        self._css_path_button_snikers = 'div[onclick*=snikers]'

        # Кнопка использования Тонуса
        self._css_path_button_use_tonus = 'div[onclick*=tonus]'

        # Таймер для ожидания загрузки страницы с выбором противника
        self._timer_enemy_load = QTimer()
        self._timer_enemy_load.setInterval(333)
        self._timer_enemy_load.timeout.connect(self._check_enemy_load)

        # Таймер для поиска противника
        self._timer_next_enemy = QTimer()
        self._timer_next_enemy.setInterval(1000)
        self._timer_next_enemy.setSingleShot(True)
        self._timer_next_enemy.timeout.connect(self._next_enemy)

        # Информация о противнике: имя, уровень, url, выигрыш
        self.enemy_name = None
        self.enemy_level = None
        self.enemy_url = None
        self.enemy_received_money = None

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

        # TODO: рефакторинг с self._timeout_fight()
        if self._timeout_fight() is not None:
            logger.info('Напасть можно будет через %s секунд.', self._timeout_fight())

        logger.info('self._timeout_fight() = %s.', self._timeout_fight())
        logger.info('self.has_snickers() = %s.', self.has_snickers())
        logger.info('self.is_ready() = %s.', self._timeout_fight() is None or self.has_snickers())

        # True, если таймер закончился или есть Сникерс
        return self._timeout_fight() is None or self.has_snickers()

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

        # TODO: оптимиизровать использование сникерсов -- если они есть, сразу использовать и нападать и так,
        # пока не будут потрачены все

        if not self.is_ready():
            logger.debug('Нападать еще нельзя.')
            return

        self._mw._used = True
        self._mw._used_process = "Нападение на игроков"

        # TODO: если есть тонус, использовать, чтобы сразу напасть
        # TODO: флаг на разрешение использования тонуса, чтобы сразу напасть
        # self.use_tonus()

        # Если не получилось съесть Сникерс, восстанавливаем по старинке
        if not self.eat_snickers():
            if self._mw.current_hp() < self._mw.max_hp():
                self._mw.restore_hp.run()

        logger.debug('Нажимаю на кнопку "Отнять у слабого".')
        # TODO: в одном из запусков дальше этой строки, похоже дело не пошло, возможно, страница с кнопкой
        # не прогрузилась

        # Кликаем на кнопку "Отнять у слабого"
        self._mw.click_tag(self._css_path_button_fight)

        # Если не нашли подходящего противника, смотрим следующего
        if not self._check_enemy():
            self._timer_next_enemy.start()

            # Ожидаем пока противник не будет найден
            loop = QEventLoop()
            self._enemy_found.connect(loop.quit)
            loop.exec_()

        logger.debug('Нападаем на "%s" [%s]: %s.', self.enemy_name, self.enemy_level, self.enemy_url)

        # Кликаем на кнопку "Напасть"
        self._mw.click_tag('.button-fight a')

        # Обрабатываем результаты боя
        self.handle_results()

        self._mw._used = False

    def handle_results(self):
        """Обработка результата боя."""

        # TODO: учитывать проигрыш

        result = '.result'

        # Ждем пока после клика прогрузится страница и появится элемент
        Waitable(self._mw.doc).wait(result)

        # Найдем элемент, в котором будут все результаты боя
        result = self._mw.doc.findFirst(result)

        tugriki = result.findFirst('.tugriki').toPlainText().replace(',', '')
        tugriki = int(tugriki)
        self.enemy_received_money = tugriki

        # Сначала покажем выигранные монет и опыт, потом все остальное. Список используется для того, чтобы
        # порядок вывода результата боя был в порядке добавления элементов в этот список
        result_item_keys = ['Монеты', 'Опыт']

        result_dict = {
            'Монеты': tugriki,
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

    # TODO: проверить
    # TODO: работает только в Закоулках
    def has_tonus(self):
        """Функция возвратит True, если можно использовать Тонус для сброса таймера, иначе False."""

        button = self._mw.doc.findFirst(self._css_path_button_use_tonus)
        return not button.isNull()

    # TODO: проверить работу
    def use_tonus(self):
        """Функция для использования Тонуса, для сброса таймаута между драками.
        Возвращает True, если получилось, иначе False."""

        if self.has_tonus():
            logger.debug('Использую Тонус.')
            self._mw.click_tag(self._css_path_button_use_tonus)

            # TODO: если Тонуса будет не хватать, то появится окошко с предложением восстановить за плату

            # Ждем пока после клика прогрузится страница и появится элемент
            Waitable(self._mw.doc).wait(self._css_path_button_use_tonus)
            return True

        return False

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

        enemy = self._mw.doc.findFirst('.fighter2')

        # Определим тип противника -- нам нужен горожанин (нпс)
        is_npc = enemy.findFirst('.npc')
        is_npc = not is_npc.isNull()

        # Узнаем уровень противника
        level = enemy.findFirst('.level')
        level = level.toPlainText()
        level = level.replace('[', '').replace(']', '')
        level = int(level)

        # Гиперссылка на профиль противника
        a = enemy.findFirst('a')

        # Имя противника
        name = a.toPlainText()

        # Адрес противника
        url = urljoin(self._mw.moswar_url, a.attribute('href'))

        # Проверяем, что нападаем на горожанина и разница в уровнях небольшая
        found = is_npc and level - 1 <= self._mw.level() <= level + 1
        # TODO: диапазон уровней, на которые нападаем делать настраивыми
        # # TODO: Тупо ищем противника уровнем выше -- нужно получать максимальное количество искр
        # found = is_npc and self._mw.level() + 1 == level

        if found:
            self.enemy_name = name
            self.enemy_level = level
            self.enemy_url = url

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
