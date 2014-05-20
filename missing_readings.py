#!/usr/bin/python
# -*- coding: UTF-8 -*-
from models.anki import AnkiModel
from models.kanji import Kanji
from models.kanji_word import KanjiWord
from utf8_helper import force_UTF8

import settings


if __name__ == '__main__':
    force_UTF8()

    # Now we need to find if all the readings are found
    for word in KanjiWord.all():
        for reading in word.kanji_readings:
            try:
                kanji = Kanji.find(reading['base'])
            except KeyError:
                if reading['base'] in KanjiWord.KANA:
                    raise AnkiModel.Error(u"Kana mismatch: %s word(%s) reading(%s)" % (
                        reading['base'], word.kanji, word.reading
                    ))
                else:
                    raise AnkiModel.Error(u"Kanji not found, but in use: %s word(%s)" % (
                        reading['base'], word.kanji
                    ))
            if reading['reading'] not in kanji.readings and kanji.kanji != '々':
                print '%s(%s) word(%s)' % (
                    kanji.kanji,
                    reading['reading'],
                    word.kanji,
                )


