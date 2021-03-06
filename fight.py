#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from urllib.parse import urljoin

from PySide.QtCore import QObject, Signal, QTimer, QEventLoop

from common import get_logger, MoswarBotError, MoswarClosedError, MoswarElementIsMissError
from waitable import Waitable


logger = get_logger('fight')


# TODO: что-то случилось и боя не дождался, в итоге больше ничего не делал
# [2015-09-22 23:48:22,908] mainwindow.py[LINE:284] DEBUG    Запуск задач.
# [2015-09-22 23:48:22,908] mainwindow.py[LINE:343] DEBUG    Перехожу по адресу "http://www.moswar.ru/alley"
# [2015-09-22 23:48:22,909] mainwindow.py[LINE:320] DEBUG    Начинаю ожидание загрузки страницы.
# [2015-09-22 23:48:24,222] mainwindow.py[LINE:327] DEBUG    Закончено ожидание загрузки страницы.
# [2015-09-22 23:48:24,223] fight.py[LINE:66] INFO     Напасть можно будет через 692 секунд.
# [2015-09-22 23:48:24,223] fight.py[LINE:68] INFO     self._timeout_fight() = 692.
# [2015-09-22 23:48:24,223] fight.py[LINE:69] INFO     self.has_snickers() = True.
# [2015-09-22 23:48:24,223] fight.py[LINE:70] INFO     self.is_ready() = True.
# [2015-09-22 23:48:24,224] mainwindow.py[LINE:343] DEBUG    Перехожу по адресу "http://www.moswar.ru/alley"
# [2015-09-22 23:48:24,225] mainwindow.py[LINE:320] DEBUG    Начинаю ожидание загрузки страницы.
# [2015-09-22 23:48:24,884] mainwindow.py[LINE:327] DEBUG    Закончено ожидание загрузки страницы.
# [2015-09-22 23:48:24,884] fight.py[LINE:66] INFO     Напасть можно будет через 691 секунд.
# [2015-09-22 23:48:24,884] fight.py[LINE:68] INFO     self._timeout_fight() = 691.
# [2015-09-22 23:48:24,884] fight.py[LINE:69] INFO     self.has_snickers() = True.
# [2015-09-22 23:48:24,885] fight.py[LINE:70] INFO     self.is_ready() = True.
# [2015-09-22 23:48:24,885] fight.py[LINE:222] DEBUG    Съедаю сникерс.
# [2015-09-22 23:48:24,885] mainwindow.py[LINE:498] DEBUG    Выполняю клик по тегу: div[onclick*=snikers]
# [2015-09-22 23:48:25,233] waitable.py[LINE:75] DEBUG    Ищу элемент: div[class='button-big btn f1']. Количество попыток: 10.
# [2015-09-22 23:48:25,573] waitable.py[LINE:59] DEBUG    Элемент найден.
# [2015-09-22 23:48:25,573] fight.py[LINE:115] DEBUG    Нажимаю на кнопку "Отнять у слабого".
# [2015-09-22 23:48:25,574] mainwindow.py[LINE:498] DEBUG    Выполняю клик по тегу: div[class='button-big btn f1']


# TODO: такое ощущение, что вместо клика на кнопку нападения перса, бот как-то кликает на имя противника, что
# является ссылкой и после ждет результатов боя
# [2015-09-29 21:42:12,927] fight.py[LINE:144] DEBUG    Нажимаю на кнопку "Отнять у слабого".
# [2015-09-29 21:42:12,927] mainwindow.py[LINE:469] DEBUG    Выполняю клик по тегу: div[class='button-big btn f1']
# [2015-09-29 21:42:13,794] fight.py[LINE:160] DEBUG    Нападаем на " seryvolk" [13]: http://www.moswar.ru/player/22038/.
# [2015-09-29 21:42:13,794] mainwindow.py[LINE:469] DEBUG    Выполняю клик по тегу: .button-fight a
# [2015-09-29 21:42:14,338] waitable.py[LINE:40] DEBUG    Текущий адрес: http://www.moswar.ru/alley/.
# [2015-09-29 21:42:14,338] waitable.py[LINE:99] DEBUG    Ищу элемент: .result. Количество попыток: 30. Интервал: 1000.
# [2015-09-29 21:42:44,744] waitable.py[LINE:80] WARNING  Закончилось количество попыток найти элемент: .result.
# [2015-09-29 21:42:44,745] waitable.py[LINE:81] DEBUG    Текущий адрес: http://www.moswar.ru/alley/.
# Traceback (most recent call last):
#   File "C:\Users\ipetrash\Projects\moswar_bot\mainwindow.py", line 287, in _task_tick
# [2015-09-29 21:42:44,749] waitable.py[LINE:82] DEBUG    Текущая страница сохранена в файл: 21.42.44.html.
#     self.fight.run()
#   File "C:\Users\ipetrash\Projects\moswar_bot\fight.py", line 166, in run
#     self.handle_results()
#   File "C:\Users\ipetrash\Projects\moswar_bot\fight.py", line 184, in handle_results
#     tugriki = int(tugriki)
# ValueError: invalid literal for int() with base 10: ''


# TODO: каким-то фигом имя и ссылка противника оказались неправильными, возможно не успели прогрузиться,
# но при этом нападение прошло удачно
# [2015-10-02 01:34:30,426] mainwindow.py[LINE:469] DEBUG    Выполняю клик по тегу: div[class='button-big btn f1']
# [2015-10-02 01:34:31,157] fight.py[LINE:187] DEBUG    Нападаем на "" [10]: http://www.moswar.ru/clan/3658/.
# [2015-10-02 01:34:31,157] mainwindow.py[LINE:469] DEBUG    Выполняю клик по тегу: .button-fight a
# [2015-10-02 01:34:31,472] waitable.py[LINE:40] DEBUG    Текущий адрес: http://www.moswar.ru/alley/.
# [2015-10-02 01:34:31,472] waitable.py[LINE:99] DEBUG    Ищу элемент: .result. Количество попыток: 30. Интервал: 1000.
# [2015-10-02 01:34:32,481] waitable.py[LINE:72] DEBUG    Элемент найден.
# [2015-10-02 01:34:32,482] fight.py[LINE:240] DEBUG    Результат боя:
#   Монеты: 8768
#   Опыт: 2
#   Кирпич: 2


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

        # Информация о противнике: имя, уровень, url
        self.enemy_name = None
        self.enemy_level = None
        self.enemy_url = None

        # Выигрыш / проигрыш. Если проигрыш, self.is_winner будет равен False
        self.received_money = None

        # True если победили мы, False если противник и None если ничья
        self.is_winner = None

        # Минимальная разница в уровне с противником. Эта величина вычитается из текущего уровня персонажа.
        self.min_diff_levels = 0

        # Максимальная разница в уровне с противником. Эта величина добавляется к текущему уровню персонажа.
        # Нельзя нападать на противника, у которого уровень больше трех от нашего
        self.max_diff_levels = 3

    # Сигнал вызывается, когда противник на странице найден -- например, страница загрузилась
    _enemy_load_finished = Signal()

    # Сигнал вызывается, когда противник подходит для нападения
    _enemy_found = Signal()

    def is_ready(self):
        """Возвращает True, если вызов метода run будет иметь смысл -- можем напасть, иначе False."""

        try:
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

        except MoswarClosedError:
            raise

        except Exception as e:
            raise MoswarBotError(e)

        return False

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

        try:
            if self._mw._used:
                logger.warn('Бот в данный момент занят процессом "%s". Выхожу из функции.', self._mw._used_process)
                return

            self._mw._used_process = "Нападение на игроков"
            logger.debug('Выполняю задание "%s".', self._mw._used_process)

            self._mw.alley()

            # TODO: оптимиизровать использование сникерсов -- если они есть, сразу использовать и нападать и так,
            # пока не будут потрачены все

            if not self.is_ready():
                logger.debug('Нападать еще нельзя.')
                return

            self._mw._used = True

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

            # Перемотка битвы
            forward = '#controls-forward'

            # Ждем пока после клика прогрузится страница и появится элемент
            Waitable(self._mw).wait(forward)

            # Перематываем бой
            self._mw.click_tag(forward)

            # Обрабатываем результаты боя
            self.handle_results()

        except MoswarClosedError:
            raise

        except Exception as e:
            raise MoswarBotError(e)

        finally:
            self._mw._used = False

    def name_winner(self):
        """Функция возвращает имя победителя в драке."""

        try:
            name = self._mw.doc.findFirst('.result div').toPlainText()
            name = name.replace('Победитель:', '')
            name = name[:name.rindex('[')]
            return name.strip()
        except Exception as e:
            raise MoswarElementIsMissError(e)

    def handle_results(self):
        """Обработка результата боя."""

        result = '.result'

        # Ждем пока после клика прогрузится страница и появится элемент
        Waitable(self._mw).wait(result)

        # Найдем элемент, в котором будут все результаты боя
        result = self._mw.doc.findFirst(result)

        if 'Ничья!' in result.toPlainText():
            self.is_winner = None
            self.received_money = 0
            logger.debug('Результат боя: Ничья.')
            return

        # Проверим по именам кто победил
        self.is_winner = self._mw.name() == self.name_winner()

        tugriki = result.findFirst('.tugriki').toPlainText().replace(',', '')
        tugriki = int(tugriki)
        self.received_money = tugriki

        # Сначала покажем выигранные монет и опыт, потом все остальное. Список используется для того, чтобы
        # порядок вывода результата боя был в порядке добавления элементов в этот список
        result_item_keys = ['Монеты', 'Опыт']

        result_dict = {
            'Монеты': tugriki,
            'Опыт': result.findFirst('.expa').toPlainText(),
        }

        neft = result.findFirst('.neft')
        if not neft.isNull():
            result_item_keys.append('Нефть')
            result_dict['Нефть'] = int(neft.toPlainText())

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

        result_str = 'Результат боя:'
        if not self.is_winner:
            result_str += ' Бой проигран. Вся награда достается противнику.'

        result_str += '\n'
        result_str += '\n'.join(result_list)

        logger.debug(result_str)

    # TODO: работает только в Закоулках
    def has_tonus(self):
        """Функция возвратит True, если можно использовать Тонус для сброса таймера, иначе False."""

        button = self._mw.doc.findFirst(self._css_path_button_use_tonus)
        return not button.isNull()

    def use_tonus(self):
        """Функция для использования Тонуса, для сброса таймаута между драками.
        Возвращает True, если получилось, иначе False."""

        if self.has_tonus():
            logger.debug('Использую Тонус.')
            self._mw.click_tag(self._css_path_button_use_tonus)

            # TODO: если Тонуса будет не хватать, то появится окошко с предложением восстановить за плату

            # Ждем пока после клика прогрузится страница и появится элемент
            Waitable(self._mw).wait(self._css_path_button_use_tonus)
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
            Waitable(self._mw).wait(self._css_path_button_fight)
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

        my_level = self._mw.level()

        # TODO: добавить ограничение на количество попыток найти гражданина, перед тем как напасть на игрока

        # Проверяем, что уровень противника находится в пределе диапазона
        check_level = my_level - self.min_diff_levels <= level <= my_level + self.max_diff_levels

        found = is_npc and check_level
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
