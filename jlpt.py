#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import json


JLPT_MAP = {}
JLPT_KANJI_MAP = {}

JLPT_PATH = None
JLPT_ALL = []

MAX_LEVEL = 5

def setup_jlpt(path):
    global JLPT_PATH
    JLPT_PATH = path

def load_jlpt():
    global JLPT_MAP
    global JLPT_KANJI_MAP
    global JLPT_ALL

    if JLPT_PATH is None:
        raise Exception('JLPT File not Found, please setup path')

    # Read the file, should exist
    with open(JLPT_PATH, 'r') as fh:
        JLPT_MAP = json.load(fh)

    # Inverse the map
    for level, kanji_list in JLPT_MAP.iteritems():
        level = int(filter(lambda char: char in '0123456789', level))

        for kanji in kanji_list:
            if kanji in JLPT_ALL:
                continue
                # print u'Duplicate: %s (%s:%s)' % (kanji, level, JLPT_KANJI_MAP[kanji])

            JLPT_ALL.append(kanji)
            JLPT_KANJI_MAP[kanji] = level


LOADED = False

def get_level(kanji):
    global LOADED
    global JLPT_KANJI_MAP

    if not LOADED:
        load_jlpt()
        LOADED = True

    # See if the Kanji is in the JLPT
    return JLPT_KANJI_MAP.get(kanji, None)

def get_all():
    global JLPT_ALL
    return tuple(JLPT_ALL)
