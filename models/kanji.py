#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from models.anki import AnkiModel
from models.reading import Reading, StringList


class Kanji(AnkiModel):
    TYPE_ID = ['1391635666513']
    FIELDS = (
        'kanji',
        '_readings',
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
            self._readings = self._readings.replace(sep, Kanji.SEP[-1])

        # Now we can do a split in one simple line
        self._readings = self._readings.split(Kanji.SEP[-1])
        self.init_readings()


    def init_readings(self):
        readings = []

        for reading in self._readings:
            readings.append(Reading.generate(reading))

        self._readings = readings

    @property
    def readings(self):
        readings = StringList()

        for reading in self._readings:
            readings += reading.get_all()

        return readings





