#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from models.anki import AnkiModel
from models.reading import Reading, StringList

import json
import os


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

    @classmethod
    def setup(cls, path):
        cls.UNUSED_PATH = path

        # Ensure the file exists, if not create it
        if not os.path.isfile(cls.UNUSED_PATH):
            with open(cls.UNUSED_PATH, 'w') as fh:
                json.dump([], fh)

        with open(cls.UNUSED_PATH, 'r') as fh:
            cls.ignored = json.load(fh)

    @staticmethod
    def add_unused_reading(string):
        Kanji.ignored.append(unicode(string))

        # Make sure it is a set, but json dumpable
        Kanji.ignored = list(set(Kanji.ignored))

        data = json.dumps(Kanji.ignored, ensure_ascii=False).encode('utf8')
        with open(Kanji.UNUSED_PATH , 'w') as fh:
            fh.write(data)


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







