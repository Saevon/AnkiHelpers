#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from models.anki import AnkiModel
from models.kanji import Kanji
from models.kanji_word import KanjiWord
from utf8_helper import force_UTF8

import settings



if __name__ == '__main__':
    force_UTF8()

    for i in range(10):
        print KanjiWord.random().kanji



