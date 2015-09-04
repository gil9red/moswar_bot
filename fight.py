#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from PySide.QtCore import QObject, Signal, QTimer, QEventLoop
from utils import get_logger


logger = get_logger('fight')


class Fight(QObject):
    def __init__(self, mw):
        super().__init__()

        self._mw = mw

        # Таймер для ожидания загрузки страницы с выбором противника
        self._timer_enemy_load = QTimer()
        self._timer_enemy_load.setInterval(333)
        self._timer_enemy_load.timeout.connect(self._check_enemy_load)

        # Таймер для поиска противника
        self._timer_next_enemy = QTimer()
        self._timer_next_enemy.setInterval(1000)
        self._timer_next_enemy.setSingleShot(True)
        self._timer_next_enemy.timeout.connect(self._next_enemy)

    # Сигнал вызывается, когда противник на странице найден -- например, страница загрузилась
    _enemy_load_finished = Signal()

    # Сигнал вызывается, когда противник подходит для нападения
    _enemy_found = Signal()

    def run(self):
        """Функция для нападения на игроков.

        Ищем слабого горожанина (заброшенного персонажа) -- не нужно привлекать внимание к боту.
        Уровень противника в пределах нашего +/- 1
        """

        # Идем в Закоулки
        self._mw.alley()

        # TODO: проверить таймер

        if self._mw.current_hp() < self._mw.max_hp():
            self.restore_hp.run()

        # Кликаем на кнопку "Отнять у слабого"
        self._mw.click_tag("div[class='button-big btn f1']")

        # Если не нашли подходящего противника, смотрим следующего
        if not self._check_enemy():
            self._timer_next_enemy.start()

            # Ожидаем пока противник не будет найден
            loop = QEventLoop()
            self._enemy_found.connect(loop.quit)
            loop.exec_()

        logger.debug('Нападаем на противника.')

        # Кликаем на кнопку "Напасть"
        # self._mw.click_tag("div[class='button button-fight'] a")
        self._mw.click_tag(".button-fight a")

        # TODO: перематывать бой
        # <i id="controls-forward" class="icon icon-forward disabled" onclick="fightForward();"></i>

        # TODO: результат боя
        # Деньги: .result .tugriki
        # Опыт: .result .expa
        # Искры: .result .sparkles

        # TODO: таймаут после боя:
        # <a data-no-blinking="1" intitle="1" endtime="1441397312" timer="361" style="" id="timeout" href="/alley/"
        # onclick="return AngryAjax.goToUrl(this, event);" process="1">00:06:02</a>

        # TODO: неактивные таймеры
        # <a id="timeout" data-no-blinking="1" intitle="1" endtime="" timer="" style="display:none;" href="//" onclick="return AngryAjax.goToUrl(this, event);"></a>
        # <a id="timeout2" data-no-blinking="1" intitle="1" endtime="" timer="" style="display:none;" href="//" onclick="return AngryAjax.goToUrl(this, event);"></a>

    def _check_enemy_load(self):
        """Функция для ожидания загрузки страницы с выбором противника."""

        # enemy = self._mw.doc.findFirst('div[class="fighter2"]')
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
        # is_npc = self._mw.doc.findFirst('div[class="fighter2"] i')
        # is_npc = is_npc.attribute('class') == "npc"
        is_npc = self._mw.doc.findFirst('.fighter2 .npc')
        is_npc = not is_npc.isNull()
        logger.info('Противник горожанин -> %s.', is_npc)

        # Узнаем уровень противника
        # npc_level = self._mw.doc.findFirst('div[class="fighter2"] span[class="level"]')
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
        # self._mw.click_tag("div[class='button button-search'] a")
        self._mw.click_tag(".button-search a")

        # Если нашли противника
        if self._check_enemy():
            self._enemy_found.emit()
            self._timer_next_enemy.stop()
        else:
            # Ищем дальше
            self._timer_next_enemy.start()
