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

    SEP = [
        # ／
        u'\uff0f',
        # ・
        u'\u30fb',
    ]

    def __init__(self, data):
        super(Kanji, self).__init__(data)

        # Replace all the seperators with the final one
        for sep in Kanji.SEP[:-1]:
            self.readings = self.readings.replace(sep, Kanji.SEP[-1])

        # Now we can do a split in one simple line
        self.readings = self.readings.split(Kanji.SEP[-1])

