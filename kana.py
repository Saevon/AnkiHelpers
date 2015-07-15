#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from jcconv import kata2hira, hira2kata
from itertools import chain

from printable import PrintableDict, PrintableList


__by_vowels = PrintableDict(**{
    u'ア': u'ワラヤャマハナタサカアァ',
    u'イ': u'リミヒニちシキイィ',
    u'ウ': u'ルユュムフヌツスクウゥ',
    u'エ': u'レメヘネテセケエェ',
    u'オ': u'ヲロヨョモホノトソコオォ',
})

__to_dakuten = PrintableDict(**{
    u'か': u'が',
    u'き': u'ぎ',
    u'く': u'ぐ',
    u'け': u'げ',
    u'こ': u'ご',
    u'さ': u'ざ',
    u'し': u'じ',
    u'す': u'ず',
    u'せ': u'ぜ',
    u'そ': u'ぞ',
    u'た': u'だ',
    u'ち': u'ぢ',
    u'つ': u'づ',
    u'て': u'で',
    u'と': u'ど',
    u'は': u'ばぱ',
    u'ひ': u'びぴ',
    u'ふ': u'ぶぷ',
    u'へ': u'べぺ',
    u'ほ': u'ぼぽ',
})

__to_mini = PrintableDict(**{
    u'く': u'っ',
    u'つ': u'っ',
    u'や': u'ゃ',
    u'よ': u'ょ',
    u'ゆ': u'ゅ',

    u'わ': u'ゎ',
    u'か': u'ゕ',
    u'け': u'ゖ',

    u'あ': u'ぁ',
    u'い': u'ぃ',
    u'う': u'ぅ',
    u'え': u'ぇ',
    u'お': u'ぉ',
})

EXTENDABLE_MINIS = (
    u'つ',
    u'く',
)

__by_dakuten = PrintableDict()
for vowel, letters in __to_dakuten.iteritems():
    for letter in letters:
        __by_dakuten[letter] = vowel

__to_vowels = PrintableDict()
for vowel, letters in __by_vowels.iteritems():
    for letter in letters:
        __to_vowels[letter] = vowel



def codepoint_range(start, end):
    for val in range(start, end):
        try:
            yield unichr(val)
        except ValueError:
            # Sometimes certain codepoints can't be used on a machine
            pass

def char_set(value):
    if isinstance(value, list) or isinstance(value, tuple):
        return codepoint_range(*value)
    else:
        return [value]

def unipairs(lst):
    return PrintableList(reduce(lambda a, b: chain(a, b), map(char_set, lst)))

__KATAKANA = (
    # Katakana: http://en.wikipedia.org/wiki/Katakana
    (0x30A0, 0x30FF + 1),
    (0x31F0, 0x31FF + 1),
    (0x3200, 0x32FF + 1),
    (0xFF00, 0xFFEF + 1),
)

__HIRAGANA = (
    # Hiragana: http://en.wikipedia.org/wiki/Hiragana
    (0x3040, 0x309F + 1),
    (0x1B000, 0x1B0FF + 1),
)

__KANJI = (
    (0x4e00, 0x9faf + 1),
)

__BONUS_KANA = (
    u'〜',
)


KATAKANA = unipairs(__KATAKANA)
HIRAGANA = unipairs(__HIRAGANA)
KANA = PrintableList(KATAKANA + HIRAGANA + unipairs(__BONUS_KANA))
KANJI = unipairs(__KANJI)



def __is_katakana(char):
    return char in KATAKANA

def is_katakana(string):
    for char in string:
        if not __is_katakana(char):
            return False
    return True

def __is_hiragana(char):
    return char in HIRAGANA

def is_hiragana(string):
    for char in string:
        if not __is_hiragana(char):
            return False
    return True

def __is_kana(char):
    return char in KANA

def is_kana(string):
    for char in string:
        if not __is_kana(char):
            return False
    return True

def __is_kanji(char):
    return char in KANJI

def is_kanji(string):
    for char in string:
        if not __is_kanji(char):
            return False
    return True

def kana_minus_dakuten(char):
    if is_katakana(char):
        hira = kata2hira(char)
        hira = __by_dakuten.get(hira, hira)
        return hira2kata(hira)
    else:
        return __by_dakuten.get(char, char)

def kana_plus_dakuten(char):
    yield char

    is_kata = is_katakana(char)
    if is_kata:
        char = kata2hira(char)

    for char in __to_dakuten.get(char, ''):
        yield hira2kata(char) if is_kata else char

def kana_plus_mini(char):
    yield char

    is_kata = is_katakana(char)
    if is_kata:
        char = kata2hira(char)

    for char in __to_mini.get(char, ''):
        yield hira2kata(char) if is_kata else char


def extend_dakuten_reading(string):
    if len(string) == 0:
        yield ''
        return

    char = string[0]
    for mult in kana_plus_dakuten(char):
        yield mult + string[1:]

def extend_mini_reading(string):
    if len(string) == 0:
        yield ''
        return

    char = string[-1]
    if char not in EXTENDABLE_MINIS:
        yield string
        return

    for substr in kana_plus_mini(char):
        yield string[:-1] + substr



def char_to_base_vowel(char):
    char = kana_minus_dakuten(char)
    translated = __to_vowels.get(char, False) or __to_vowels.get(hira2kata(char), False)

    if translated is False:
        raise Exception(u"Can't convert")

    return translated


def all_to_hiragana(string):
    out = u''

    for index, char in enumerate(string):
        if char == u'ー' or char == u'｜':
            char = char_to_base_vowel(out[-1])

        char = kata2hira(char)

        out += char

    return out

if __name__ == u'__main__':
    from tester import *

    test_equal(kana_minus_dakuten(u'は'), u'は', u"No Dakuten failure")
    test_equal(kana_minus_dakuten(u'ば'), u'は', u"No Dakuten failure")
    test_equal(kana_minus_dakuten(u'ぱ'), u'は', u"No Dakuten failure")

    test_equal(kana_minus_dakuten(u'ジ'), u'シ', u"Katakana failure")
    test_equal(kana_minus_dakuten(u'本'), u'本', u"Kanji changed")


    test_true(is_katakana(u'ハ'), u"Katakana check wrong")
    test_true(is_katakana(u'ー'), u"Katakana check wrong")
    test_true(is_katakana(u'ジ'), u"Katakana check wrong")
    test_true(is_katakana(u'ッ'), u"Katakana check wrong")

    test_true(not is_katakana(u'本'), u"Katakana Kanji check wrong")
    test_true(not is_katakana(u'っ'), u"Katakana small hiragana check wrong")
    test_true(not is_katakana(u'は'), u"Katakana hiragana wrong")


    test_true(is_hiragana(u'っ'), u"Hiragana check wrong")
    test_true(is_hiragana(u'つ'), u"Hiragana check wrong")
    test_true(is_hiragana(u'を'), u"Hiragana check wrong")

    test_true(not is_hiragana(u'本'), u"Hiragana Kanji check wrong")
    test_true(not is_hiragana(u'ッ'), u"Hiragana small katakana check wrong")
    test_true(not is_hiragana(u'ハ'), u"Hiragana katakana check wrong")


    test_true(is_kana(u'っ'), u"Kana check wrong")
    test_true(is_kana(u'つ'), u"Kana check wrong")
    test_true(is_kana(u'を'), u"Kana check wrong")
    test_true(is_kana(u'ッ'), u"Kana check wrong")
    test_true(is_kana(u'ハ'), u"Kana check wrong")
    test_true(is_kana(u'〜・'), u"Kana special check wrong")
    test_true(not is_kana(u'本'), u"Kana check wrong")


    test_equal(kana_minus_dakuten(u'は'), u'は')
    test_equal(kana_minus_dakuten(u'ば'), u'は')
    test_equal(kana_minus_dakuten(u'バ'), u'ハ')
    test_equal(kana_minus_dakuten(u'本'), u'本')


    test_equal(''.join(kana_plus_dakuten(u'は')), u'はばぱ')
    test_equal(''.join(kana_plus_dakuten(u'本')), u'本')
    test_equal(''.join(kana_plus_dakuten(u'シ')), u'シジ')

    test_list_equal(extend_dakuten_reading(u'しゃし'), [u'しゃし', u'じゃし'])
    test_list_equal(extend_mini_reading(u'し'), [u'し'])
    test_list_equal(extend_mini_reading(u'いつ'), [u'いつ', u'いっ'])


    test_equal(all_to_hiragana(u'ジータ'), u'じいた')

