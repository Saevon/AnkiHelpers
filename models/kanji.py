#!/usr/bin/python
# -*- coding: UTF-8 -*-
from anki import AnkiModel


class Kanji(AnkiModel):
    TYPE_ID = ['1391635666513']
    FIELDS = (
        'kanji',
        'readings',
        'meanings',
    )

    KEY = 'kanji'

    # ／
    SEP = u'\uff0f'

    def __init__(self, data):
        super(Kanji, self).__init__(data)

        self.readings = self.readings.split(Kanji.SEP)

