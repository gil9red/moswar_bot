#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import sys
import logging


def get_logger(name, file='log.txt', encoding='utf8'):
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s')

    fh = logging.FileHandler(file, encoding=encoding)
    fh.setLevel(logging.DEBUG)

    ch = logging.StreamHandler(stream=sys.stdout)
    # ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    log.addHandler(fh)
    log.addHandler(ch)

    return log