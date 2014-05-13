#!/usr/bin/python
# -*- coding: UTF-8 -*-
from models.anki import AnkiModel
from models.kanji import Kanji
from models.kanji_word import KanjiWord
from utf8_helper import force_UTF8


if __name__ == '__main__':
    force_UTF8()

    # First we need to read out whitelist
    whitelist = set()
    for kanji in Kanji.all():
        if not kanji.suspended:
            whitelist.add(kanji.kanji)

    # Now we filter out any KanjiWords that use other kanji
    for kanji_word in KanjiWord.all():
        if kanji_word.suspended:
            continue

        fine = True
        for kanji in kanji_word.kanji:
            if kanji not in KanjiWord.KANA and kanji not in whitelist:
                fine = False

        if fine:
            kanji_word.mark_suspended(False)

