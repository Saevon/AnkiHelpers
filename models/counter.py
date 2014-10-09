#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from models.kanji_word import KanjiWord


class Counter(KanjiWord):
    TYPE_ID = ['1402788235577']
    FIELDS = (
        'kanji',
        'reading',
        'value',
        'group',
    )



