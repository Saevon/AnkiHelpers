#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from models.anki import AnkiModel
from models.kanji import Kanji
from models.kanji_word import KanjiWord
from utf8_helper import force_UTF8
import kana

from collections import defaultdict
from itertools import islice

import settings


if __name__ == '__main__':
    force_UTF8()

    # Get the readings of every single kanji
    mapping = defaultdict(list)
    for word in KanjiWord.all():
        for reading in word.kanji_readings:
            mapping[reading['base']].append(reading['reading'])

    # Now remove any that are used
    # try:
    #     kanji = Kanji.find(reading['base'])
    # except KeyError:
    #     if kana.is_kana(reading['base']):
    #         raise AnkiModel.Error(u"Kana mismatch: %s word(%s) reading(%s)" % (
    #             reading['base'], word.kanji, word.reading
    #         ))
    #     else:
    #         raise AnkiModel.Error(u"Kanji not found, but in use: %s word(%s)" % (
    #             reading['base'], word.kanji
    #         ))
    # if reading['reading'] not in kanji.readings and kanji.kanji != '々':
    #     print '%s(%s) word(%s)' % (
    #         kanji.kanji,
    #         reading['reading'],
    #         word.kanji,
    #     )

    for kanji in Kanji.all():
        for reading in kanji._readings:
            possible = map(unicode, reading.get_all())

            # See if we can find the reading in our kanji words list
            found = False
            for use in mapping[kanji.kanji]:
                if use in possible:
                    found = True

            # Ignore any that are used
            if found:
                continue

            # See if its been ignored
            string = "(kanji: %s) %s" % (kanji.kanji, reading)
            if string in Kanji.ignored:
                continue

            # Ask the user if he wants to ignore this one
            inp = raw_input("Ignore? %s: " % string)
            if inp == "y":
                Kanji.add_unused_reading(string)


        # print ', '.join(map(unicode, kanji._readings))

    # The leftovers are the unused readings
    # for kanji, readings in islice(mapping.iteritems(), 0, 10):
    #     print '%s(%s)' % (
    #         kanji,
    #         ', '.join(readings),
    #     )




