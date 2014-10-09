#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from anki import AnkiModel
from kanji import Kanji
from HTMLParser import HTMLParser
import kana


import json
import sys
import os


class KanjiPart(dict):
    def __repr__(self):
        if self['is_kanji']:
            return u'Kanji< %(base)s(%(reading)s) >' % self
        else:
            return u'Kana< %(base)s >' % self

    def __add__(self, other):
        out = KanjiPart(self.copy())
        out['base'] = self['base'] + other['base']
        return out

class KanjiWord(AnkiModel):
    TYPE_ID = ['1392404679934']
    FIELDS = (
        'kanji',
        'reading',
        'meanings',
        'english',
    )

    KEY = 'kanji'

    SEP = Kanji.SEP

    # create a subclass and override the handler methods
    class KanjiParser(HTMLParser):
        def handle_data(self, data):
            self.parts.append(data)

        def read_parts(self, html):
            self.parts = []
            self.feed(html)
            return self.parts

    def __init__(self, data):
        super(KanjiWord, self).__init__(data)

        try:
            self._load_kanji_readings()
        except Exception:
            sys.stderr.write(str(data))
            sys.stderr.write('\n')
            raise

    @classmethod
    def setup(cls, path):
        cls.COMPLEX_PATH = path

        # Ensure the file exists, if not create it
        if not os.path.isfile(cls.COMPLEX_PATH):
            with open(cls.COMPLEX_PATH, 'w') as fh:
                json.dump([], fh)

        with open(cls.COMPLEX_PATH, 'r') as fh:
            cls.exceptions = json.load(fh)

    def _load_kanji_readings(self):
        self.kanji_readings = []

        # Group up the readings field
        readings = [kana.all_to_hiragana(unicode(val)) for val in KanjiWord.KanjiParser().read_parts(self.reading)]
        self.reading = ''.join(readings)

        readings = readings
        bases = self.group_kana(self.kanji)

        # Now we need to filter out the any bits that match from both
        right_pos = 0
        left_pos = 0
        while True:
            right = bases[right_pos]['base']
            left = readings[left_pos]

            if left == right:
                bases.pop(right_pos)
                readings.pop(left_pos)
            else:
                right_pos += 1

            if right_pos >= len(bases):
                left_pos += 1
                right_pos = 0

            if left_pos >= len(readings):
                break

        # If the two don't match then there might be a problem
        if self.kanji in KanjiWord.exceptions:
            return
        elif len(bases) == 0:
            # Then the reading is either screwed up, or is a pure kana word (which shouldn't be a kanji-word)
            raise AnkiModel.Error(u"Reading is identical to Kanji: %s" % (
                self.kanji
            ))
        elif len(bases) != len(readings):
            # Then this is fucked up  beyond our current capability
            print(u"Is this a complex reading? %s(%s): " % (
                self.kanji,
                ''.join(readings),
            )),
            inp = raw_input()
            if inp == 'y':
                KanjiWord.add_exception(self.kanji)
                return

            raise AnkiModel.Error(u"Readings count(%s) doesn't match kanji(%s)" % (
                len(bases), readings,
            ))

        # Now map the readings to the kanji
        for kanji, reading in zip(bases, readings):
            kanji['reading'] = reading
            self.kanji_readings.append(kanji)

    def group_kana(self, string):
        # Group up the kanji field
        part = None
        out = []

        for kanji in string:
            if kanji in KanjiWord.SEP:
                # For now we ignore things past the seperator for alternate readings
                break
            elif kana.is_kana(kanji):
                if part is None:
                    part = self._new_part(is_kanji=False)
                    part['is_kanji'] = False

                part['base'] += kanji
            else:
                # Close any KANA parts first
                if part is not None:
                    out.append(part)
                    part = None

                # Add a new kanji
                part2 = self._new_part(is_kanji=True)
                part2['base'] = kanji
                out.append(part2)

        # Close any KANA parts left over
        if part is not None:
            out.append(part)

        return out


    def _new_part(self, is_kanji=True):
        out = KanjiPart()

        out['base'] = ''
        out['reading'] = ''
        out['is_kanji'] = is_kanji

        return out

    @staticmethod
    def add_exception(kanji):
        KanjiWord.exceptions.append(unicode(kanji))

        # Make sure it is a set, but json dumpable
        KanjiWord.exceptions = list(set(KanjiWord.exceptions))

        data = json.dumps(KanjiWord.exceptions, ensure_ascii=False).encode('utf8')
        with open(KanjiWord.COMPLEX_PATH , 'w') as fh:
            fh.write(data)



