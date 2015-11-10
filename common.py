#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from datetime import datetime
import sys
import logging


def save_current_html(doc):
    """Функция принимает QWebElement и сохраняет в файл, возвращая имя файла."""

    t = datetime.today().time()
    file_name = t.strftime("%H.%M.%S") + ".html"

    with open(file_name, mode='w', encoding='utf8') as f:
        f.write(doc.toOuterXml())

    return file_name


def get_logger(name, file='log.txt', encoding='utf8'):
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)

    formatter = logging.Formatter('[%(asctime)s] %(filename)s[LINE:%(lineno)d] %(levelname)-8s %(message)s')

    fh = logging.FileHandler(file, encoding=encoding)
    fh.setLevel(logging.DEBUG)

    ch = logging.StreamHandler(stream=sys.stdout)
    ch.setLevel(logging.DEBUG)

    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    log.addHandler(fh)
    log.addHandler(ch)

    return log


class MoswarBotError(Exception):
    pass


class MoswarElementIsMissError(MoswarBotError):
    pass


class MoswarClosedError(MoswarBotError):
    def __init__(self, reason):
        super().__init__('Сайт закрыт. Причина:\n"{}".'.format(reason))


class MoswarButtonIsMissError(MoswarElementIsMissError):
    def __init__(self, title_button):
        super().__init__('Не найдена кнопка "{}".'.format(title_button))


class MoswarAuthError(MoswarBotError):
    pass


LOGIN = 'ilya.petrash@inbox.ru'
PASSWORD = '0JHQu9GPRnVjazop'

CONFIG_FILE = 'config'
