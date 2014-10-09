#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from models.anki import AnkiModel
from models.kanji import Kanji
from models.kanji_word import KanjiWord
from utf8_helper import force_UTF8
import kana

import settings


def append_word(data, reading, kanji, word, readings):
    key = '%s-%s' % (kanji, reading)

    if not data.get(key, False):
        data[key] = {
            'kanji': kanji,
            'reading': reading,
            'words': [],
        }

    data[key]['words'].append((word, readings))


if __name__ == '__main__':
    force_UTF8()

    missing = {}

    # Now we need to find if all the readings are found
    for word in KanjiWord.all():
        for reading in word.kanji_readings:
            try:
                kanji = Kanji.find(reading['base'])
            except KeyError:
                if kana.is_kana(reading['base']) and reading['base'] != u'ヶ':
                    raise AnkiModel.Error(u"Kana mismatch: %s word(%s) reading(%s)" % (
                        reading['base'], word.kanji, word.reading
                    ))
                else:
                    # Make sure not to do the rest of the work
                    # otherwise you'll use the previous kanji
                    continue
                    # raise AnkiModel.Error(u"Kanji not found, but in use: %s word(%s)" % (
                    #     reading['base'], word.kanji
                    # ))

            # Now that we have the kanji, check if this reading is used
            if kanji.kanji == '々':
                pass
            elif kana.all_to_hiragana(reading['reading']) in kanji.readings:
                index = kanji.readings.index(reading['reading'])
                kanji.readings[index].add_use(word)
            else:
                append_word(missing, reading['reading'], kanji.kanji, word.kanji, word.reading)

    # Now we check for any readings which are unused
    unused = []
    unused_ids = []
    for kanji in Kanji.all():
        for reading in kanji.readings:
            if len(reading.uses) == 0 and id(reading.reading) not in unused_ids:
                unused_ids.append(id(reading.reading))
                unused.append({
                    'kanji': kanji.kanji,
                    'reading': reading.reading,
                })


    if len(missing):
        print 'Missing: '
        for key, data in missing.iteritems():
            print '    %s(%s) words(%s)' % (
                data['kanji'],
                data['reading'],
                ', '.join(['%s:%s' % val for val in data['words']]),
            )

    '''
    if len(unused):
        print 'Unused: '
    for data in unused:
        print '    %s(%s)' % (
            data['kanji'],
            data['reading'],
        )
    '''


