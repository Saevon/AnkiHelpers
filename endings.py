#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from utf8_helper import force_UTF8

import random

def random_bool():
    return random.choice((True, False))


DURATION = [
    "times a duration",

    "back when",
    "after",
    "before",
    "while doing",

    "last (time)", # この前の金曜日
    "next (time)", # 次の金曜日

    "until",
    "in prep for",
]

SEEMS = [
    "quoting",

    "seems like",
    "looks like",
    "similar to",
    "resembles",
    "hearsay",
    "judgement",
    "Showing no sign of X",
]

DIFF = [
    "easy to do",
    "hard to do",

]

ORDERS = [
    "imperative",
    "please do",
    "please do (casual)",
    "do this (なさい)",
    "do this (なさい casual)",
    "don't do this (なさい casual)",
]

ENDINGS = [
    DIFF,
    SEEMS,
    ORDERS,
    DURATION,


    "how to do",
    "only",

    [
        "probably",
        "should be",
        "possibly",
    ],

    "determined",
    "I think",

    [
        "glad that",
        "nice if",
        "should have done",
    ],

    [
        "want to do",
        "want someone else to do",
        "want both",
        "want neither",
    ],

    [
        "thanks for doing",
        "sorry for doing",
    ],

    [
        "something",
        "nothing",
        "everything",
        "anything",
    ],

    "superlative (than anyone)",

    "excepting X",
    "regarding X",
    "for the sake of X",
    "Thanks to X",
    "In exchange for X",
    "when compared to X",
    "according to X",

    "Explanatory",

    "passive",
    "causative",

    "accidentally",

    "potential",
    "suggestive",
    "permissive",
    "advice",
    "must",

    "experience doing",
    "plan to",

    "favours",
    "gifts",

    "make it X",
    "become X",
    "strive to become",
    "achieve (became x)",
    "decide to do",

    "try and do",
    "state",
    "purposeful state",
    "doing",

    "past",

    "if",

    "comparison",
    "improvement",
]

CONJUNCT = [
    "けれども",
    "けれど",
    "けど",
    "しかし",
    "それとも",
    "それでも",
    "それに",
    "それで",
    "つまり",
    "そして",
    "それから",
    "ところで",
    "そういえば",
    "ただし",
    "が",
    "から",
    "ので",
    "のに",
    "ても",
    "くせに",
]


if __name__ == '__main__':
    force_UTF8()

    from random_word import main
    main("-t verb".split())
    print "======="

    choices = random.sample(ENDINGS, random.randint(2, 5))
    for choice in choices:
        if isinstance(choice, list):
            choice = random.choice(choice)
        print choice


    if random_bool():
        print u"ない"

    print random.choice(CONJUNCT)






