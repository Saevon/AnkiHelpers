#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from models.anki import AnkiModel
from models.kanji import Kanji
from models.kanji_word import KanjiWord
from utf8_helper import force_UTF8
import kana

import settings

import argparse
import sys
from collections import Counter


def parse(args=None):

    parser = argparse.ArgumentParser(description='Returns a random word')

    parser.add_argument(
        '-n', '--num',
        dest='count', action='store', type=int,
        default=10,
        help='The number of words to display'
    )

    out = parser.parse_args(args)
    return out



if __name__ == '__main__':
    force_UTF8()

    args = parse()

    # Find all the kanji that are in the deck
    all_kanji = set()
    for word in KanjiWord.all():
        for kanji in word.kanji:
            all_kanji.add(kanji)
    for kanji in Kanji.all():
        all_kanji.add(kanji)

    # Count which kanji the input data has
    data = Counter(unicode(sys.stdin.read()))
    for char, count in data.most_common():
        # we don't want kana
        if kana.is_kana(char):
            del data[char]
        # Nor do we want kanji we know
        if char in all_kanji:
            del data[char]
        # Nor any non-kanji chars
        if not kana.is_kanji(char):
            del data[char]

    for char, count in data.most_common(args.count):
        print char, count

