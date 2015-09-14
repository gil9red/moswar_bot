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
        self.button_fight = "div[class='button-big btn f1']"

        # Таймер для ожидания загрузки страницы с выбором противника
        self._timer_enemy_load = QTimer()
        self._timer_enemy_load.setInterval(333)
        self._timer_enemy_load.timeout.connect(self._check_enemy_load)

        # Таймер для поиска противника
        self._timer_next_enemy = QTimer()
        self._timer_next_enemy.setInterval(1000)
        self._timer_next_enemy.setSingleShot(True)
        self._timer_next_enemy.timeout.connect(self._next_enemy)

        # Время, когда возможно нападение. Время используется локальное, а не серверное.
        self._date_ready = None

    # Сигнал вызывается, когда противник на странице найден -- например, страница загрузилась
    _enemy_load_finished = Signal()

    # Сигнал вызывается, когда противник подходит для нападения
    _enemy_found = Signal()

    def is_ready(self):
        """Возвращает True, если вызов метода run будет иметь смысл -- можем напасть, иначе False."""

        if self._date_ready is None:
            return True

        return datetime.today() >= self._date_ready

    def run(self):
        """Функция для нападения на игроков.

        Ищем слабого горожанина (заброшенного персонажа) -- не нужно привлекать внимание к боту.
        Уровень противника в пределах нашего +/- 1
        """

        # Идем в Закоулки
        self._mw.alley()

        # TODO: проверить таймер
        # TODO: таймаут после боя:
        # <a data-no-blinking="1" intitle="1" endtime="1441397312" timer="361" style="" id="timeout" href="/alley/"
        # onclick="return AngryAjax.goToUrl(this, event);" process="1">00:06:02</a>
        # doc = view.page().mainFrame().documentElement()
        # for timeout in doc.findAll('[id*=timeout]'):
        #     timer = timeout.attribute('timer')
        #     if timer and 'alley' in timeout.attribute('href'):
        #         # return int(timer)
        #         print('Осталось:', int(timer))
        #         break

        # TODO: если есть таймер, но есть Сникерс, то не выходим из функции и ищем противника

        for timeout in self._mw.doc.findAll('[id*=timeout]'):
            timer = timeout.attribute('timer')
            print('timer:', timer)
            if timer and 'alley' in timeout.attribute('href'):
                timer = int(timer)
                print('Осталось:', timer)
                if timer > 0:
                    # Указываем время готовности, плюс 5 секунд -- на всякий
                    self._date_ready = datetime.today() + timedelta(seconds=timer + 5)
                    return

        # TODO: если есть тонус, использовать, чтобы сразу напасть
        # print(self._mw.doc.findFirst('div[onclick*=tonus]').toPlainText())

        # Если не получилось съесть Сникерс, восстанавливаем по старинке
        if not self.eat_snickers():
            if self._mw.current_hp() < self._mw.max_hp():
                self._mw.restore_hp.run()

        logger.debug('Нажимаю на кнопку "Отнять у слабого".')

        # Кликаем на кнопку "Отнять у слабого"
        self._mw.click_tag(self.button_fight)

        # Если не нашли подходящего противника, смотрим следующего
        if not self._check_enemy():
            self._timer_next_enemy.start()

            # Ожидаем пока противник не будет найден
            loop = QEventLoop()
            self._enemy_found.connect(loop.quit)
            loop.exec_()

        logger.debug('Нападаем на противника.')

        # Кликаем на кнопку "Напасть"
        self._mw.click_tag(".button-fight a")


        # TODO: результат боя
        # doc = frame.page().mainFrame().documentElement()
        # result = doc.findFirst('.result')
        #
        # print('Монет:', result.findFirst('.tugriki').toPlainText().replace(',', ''))
        # print('Опыт:', result.findFirst('.expa').toPlainText())
        # print('Искры:', result.findFirst('.sparkles').toPlainText())
        #
        # for img in result.findAll('.object-thumb'):
        #     obj = img.findFirst('img').attribute('alt')
        #     count = img.findFirst('.count').toPlainText()
        #     print('{}: {}'.format(obj, count))


        # TODO: сообщение: Вы слишком часто деретесь.
        # <div class="alert alert-error alert1" style="display: block; top: 450.5px; left: 1007px;" data-bind-move="1">
        #   <div class="padding">
        #       <h2 id="alert-title">Ошибка</h2>
        #       <span class="close-cross" style="" onclick="closeAlert(this);">×</span>
        #       <div class="data">
        #           <div id="alert-text">Вы слишком часто деретесь.</div>
        #           <div class="actions">
        #               <div class="button">
        #                   <span class="f" onclick="$(this).parents("div.alert:first").remove();">
        #                       <i class="rl"></i>
        #                       <i class="bl"></i>
        #                       <i class="brc"></i>
        #                       <div class="c">OK</div>
        #                   </span>
        #               </div>
        #           </div>
        #       </div>
        #   </div>
        # </div>
        # for el in self.mw.doc.findAll('.alert'):
        #     title = el.findFirst('#alert-text')
        #     if not title.isNull() and title.toPlainText() == 'Вы слишком часто деретесь.':
        #         logger.debug('Вы слишком часто деретесь.')
        #
        #         self._restore_hp_window = el
        #         self._find_restore_hp_window_finded.emit()
        #         self._timer.stop()
        #         return

        # После выполнения указываем, что доступ есть (правда, по таймерам это может и не быть)
        self._date_ready = None

    # TODO: проверить
    def eat_snickers(self):
        """Функция для съедания Сникерса. Возвращает True, если получилось съесть, иначе False."""

        button = self._mw.doc.findFirst('div[onclick*=snikers]')
        if not button.isNull():
            logger.debug('Съедаю сникерс.')
            self._mw.click_tag('div[onclick*=snikers]')

            # Ждем пока после клика прогрузится страница и появится элемент
            Waitable(self._mw.doc).wait(self.button_fight)
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
        found = is_npc and npc_level - 1 <= self._mw.level() <= npc_level + 1

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
