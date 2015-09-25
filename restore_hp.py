#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from PySide.QtCore import QObject, Signal, QTimer, QEventLoop
from common import get_logger


logger = get_logger('restore_hp')


class RestoreHP(QObject):
    def __init__(self, mw):
        super().__init__()

        self.mw = mw
        self._restore_hp_window = None

        self._timer = QTimer()
        self._timer.setInterval(333)
        self._timer.timeout.connect(self._find_restore_hp_window)

    _find_restore_hp_window_finded = Signal()

    def _find_restore_hp_window(self):
        for el in self.mw.doc.findAll('.alert'):
            title = el.findFirst('#alert-title')
            if not title.isNull() and title.toPlainText() == 'Восстановить здоровье':
                logger.debug('Найдено окно восстановления жизней.')

                self._restore_hp_window = el
                self._find_restore_hp_window_finded.emit()
                self._timer.stop()
                return

    def run(self):
        """Функция восставливления жизней."""

        logger.debug('Выполняю восстановление жизней.')

        if self.mw.current_hp() == self.mw.max_hp():
            logger.info('Жизни полные!')
            return

        self.mw.click_tag(".life .plus-icon")

        self._timer.start()

        loop = QEventLoop()
        self._find_restore_hp_window_finded.connect(loop.quit)
        loop.exec_()

        logger.debug('Нажимаю на кнопку "Вылечиться".')

        button = self._restore_hp_window.findFirst('button')
        button.evaluateJavaScript('this.click()')
