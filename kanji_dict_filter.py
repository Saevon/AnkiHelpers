#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import settings

import jlpt
import xml_helpers


import sys
reload(sys)
sys.setdefaultencoding("UTF-8")


import xml.etree.ElementTree as etree
tree = etree.parse(settings.FULL_KANJI_DICT)
root = tree.getroot()


# Filter out any useless tags keeping only the actual character list
characters = [i for i in root if i.tag == 'character']

char_map = {}

for char in characters:
    # http://www.csse.monash.edu.au/~jwb/kanjidic2/kd2examph.html
    kanji = xml_helpers.get_kanji(char)

    char_map[kanji] = {
        'kanji': kanji,
        'grade': xml_helpers.grade(char),
        'halpern': xml_helpers.halpern(char),
        'strokes': xml_helpers.strokes(char),
        'jlpt': jlpt.get_level(kanji),
        'node': char,
    }

# Filter out any characters without a halpern number
for key, value in list(char_map.iteritems()):
    if value['grade'] is None and value['jlpt'] is None:
        root.remove(value['node'])

tree.write(settings.KANJI_DICT)



