#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from models.anki import AnkiModel
from models.kanji import Kanji
from models.kanji_word import KanjiWord
from utf8_helper import force_UTF8

import settings

import argparse
import random


def parse(args=None):

    parser = argparse.ArgumentParser(description='Returns a random word')

    parser.add_argument(
        '-t', '--tags',
        dest='tags', nargs='+', default=None,
        help='an integer for the accumulator'
    )
    parser.add_argument(
        '-n', '--num',
        dest='count', action='store', type=int,
        default=10,
        help='The number of words to display'
    )

    out = parser.parse_args(args)
    if out.tags is None:
        out.tags = []

    return out


def create_filter(tags):
    def pos(tag):
        return lambda val: tag in val
    def neg(tag):
        return lambda val: tag not in val

    filters = []
    for tag in tags:
        if tag.startswith("~"):
            filters.append(neg(tag[1:]))
        else:
            filters.append(pos(tag))

    def word_filter(tags):
        for filter in filters:
            if not filter(tags):
                return False
        return True
    return word_filter


def main(args=None):
    args = parse(args)

    word_filter = create_filter(args.tags)

    words = KanjiWord.all()
    words = filter(lambda val: word_filter(val.tags), words)
    sample = random.sample(words, args.count)
    for word in sample:
        print word.kanji

if __name__ == '__main__':
    force_UTF8()
    main()


