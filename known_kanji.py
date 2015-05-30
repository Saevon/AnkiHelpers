#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import settings
import os
import json

from models.kanji import Kanji
from models.kanji_word import KanjiWord
from models.counter import Counter

import kana
import jlpt
import xml_helpers

from utf8_helper import force_UTF8



def message(title, msg):
    # required sudo gem install terminal-notifier
    # WARN: not safe yeat, should sanitize title, msg

    data = {
        'msg': msg,
        'title': title,
    }


    # temporarily disabled
    '''
    import subprocess
    try:
        subprocess.call(
            u'terminal-notifier -message "%(msg)s" -title "%(title)s"' % data,
            shell=True,
        )
    except OSError as err:
        print err
    '''

    # Make sure we print properly
    force_UTF8()

    # Print out the message to console too JIK
    print '%(title)s: %(msg)s' % data

def load_extra(path):
    # Make sure the file exists
    if not os.path.isfile(path):
        with open(path, 'w') as fh:
            json.dump([], fh)

    # Load any exceptional kanji
    with open(path, 'r') as fh:
        extra = set(json.load(fh))

    return extra


def load_anki_data(kanji_list):
    kanji_list = set(kanji_list)

    # Find out which kanji we actually have cards for
    expected = set()
    for kanji in Kanji.all():
        if kanji.suspended:
            continue
        expected.add(kanji.kanji)

    # Kanji words also get to add to the whitelist
    actual = set()
    for word in Counter.all() + KanjiWord.all():
        if word.suspended:
            continue

        # Add all the kanji in the word
        for kanji in word.kanji:
            # Make sure we only add kanji
            if kana.is_kana(kanji):
                continue

            actual.add(kanji)

    extra = load_extra(settings.EXTRA_DICT_KANJI)

    # Find which kanji we have no cards for
    missing = actual - expected
    if len(missing):
        message("Missing Kanji Found", ' '.join(missing))

    # Notify the user of any kanji that don't have examples (no kanji-words)
    no_example = expected - actual
    if len(no_example):
        message("Kanji with no Examples", ' '.join(no_example))

    # Notify the user of any kanji that aren't in our dictionary
    unknown = (expected | actual) - (kanji_list | extra)
    if len(unknown):
        message("Unknown Kanji, not in Dict:", ' '.join(unknown))

    # Now we finally make our known kanji list
    known = (expected | actual)

    return known














import sys
reload(sys)
sys.setdefaultencoding("UTF-8")


import xml.etree.ElementTree as etree
tree = etree.parse(settings.KANJI_DICT)
root = tree.getroot()


# Filter out any useless tags keeping only the actual character list
characters = [i for i in root if i.tag == 'character']


full_char_map = {}
char_map = {}

for char in characters:
    # http://www.csse.monash.edu.au/~jwb/kanjidic2/kd2examph.html
    kanji = xml_helpers.get_kanji(char)

    char_map[kanji] = {
        'kanji': kanji,
        'grade': xml_helpers.grade(char),
        'halpern': xml_helpers.halpern(char),
        'strokes': xml_helpers.strokes(char),
        'jlpt': jlpt.get_level(kanji)
    }
    full_char_map[kanji] = char_map[kanji]

# Filter out any characters without a halpern number
for key, value in list(char_map.iteritems()):
    if value['grade'] is None:
        char_map.pop(key)

known = load_anki_data(char_map.keys())

# Mark any kanji that are known
for key, value in full_char_map.iteritems():
    full_char_map[key]['known'] = value['kanji'] in known



















import cgi

def make_char(char):
    data = char.copy()
    data['known'] = 'known' if data['known'] else ''

    data['kanji'] = cgi.escape(data['kanji']).encode('ascii', 'xmlcharrefreplace')
    data['halpern'] = data.get('halpern', 'none')
    data['jlpt'] = '' if data['jlpt'] is None else 'jlpt-n' + str(data['jlpt'])

    return '''<div class="kanji %(known)s %(jlpt)s grade-%(grade)s halpern-%(halpern)s">%(kanji)s</div>''' % data

def make_line(chars):
    return '''
        <div class="line">
            %(data)s
        </div>
    ''' % {
        'data': '\n'.join(chars),
    }

def make_block(lines):
    return '''
        <div class="block">
            %(data)s
        </div>
    ''' % {
        'data': '\n'.join(lines),
    }

def chunks(list, num):
    i = 0
    while i < len(list):
        yield list[i:i+num]
        i = i + num


def group(kanji_list, row=10, col=8):
    kanji_list = [make_char(char) for char in kanji_list]

    # Make the lines
    kanji_list = chunks(kanji_list, row)
    kanji_list = [make_line(line) for line in kanji_list]

    # Make the blocks
    kanji_list = chunks(kanji_list, col)
    kanji_list = [make_block(line) for line in kanji_list]

    return '\n'.join(kanji_list)














###########################################
# Create the Kanji by Grade list
grades = {}
for key, value in list(char_map.iteritems()):
    grade = int(value['grade'])
    val = grades.get(grade, None)
    if val is None:
        grades[grade] = []

    grades[grade].append(value)

# Load up the html header
data = '<html>'
with open(settings.DATA_HEADER, 'r') as f:
    data = f.read()

data += '<body class="grade-colours">'
for grade, kanji_list in grades.iteritems():
    data += '\n'
    data += group(kanji_list)
data += '</body>'

data += '</html>'

with open(os.path.join(settings.OUTPUT, 'known_kanji.html'), 'w') as f:
    f.write(data);


###########################################
# Create the Kanji by Strokes list
strokes = {}
for key, value in list(char_map.iteritems()):
    count = int(value['strokes'])
    val = strokes.get(count, None)
    if val is None:
        strokes[count] = []

    strokes[count].append(value)

# Load up the html header
data = '<html>'
with open(settings.DATA_HEADER, 'r') as f:
    data = f.read()

data += '<body class="jlpt-colours">'
for count, kanji_list in strokes.iteritems():
    data += '\n'
    data += group(kanji_list)
data += '</body>'

data += '</html>'

with open(os.path.join(settings.OUTPUT, 'known_kanji_strokes.html'), 'w') as f:
    f.write(data);


###########################################
# Create the Kanji by Halpern list
halpern = []
for key, value in list(char_map.iteritems()):
    count = value.get('halpern', False)
    if count:
        halpern.append(value)


halpern = sorted(halpern, key=lambda v: v['halpern'])


# Load up the html header
data = '<html>'
with open(settings.DATA_HEADER, 'r') as f:
    data = f.read()

data += '<body>'
data += group(halpern, col=10, row=10)
data += '</body>'

data += '</html>'

with open(os.path.join(settings.OUTPUT, 'known_kanji_halpern.html'), 'w') as f:
    f.write(data);


###########################################
# Create the Kanji by JLPT list
jlpt_kanji = {}
for kanji in jlpt.get_all():
    value = full_char_map[kanji]
    level = value['jlpt']

    # for inverse sorting
    level = jlpt.MAX_LEVEL - level

    val = jlpt_kanji.get(level, None)
    if val is None:
        jlpt_kanji[level] = []

    jlpt_kanji[level].append(value)

# Load up the html header
data = '<html>'
with open(settings.DATA_HEADER, 'r') as f:
    data = f.read()

data += '<body class="jlpt-colours">'
for grade, kanji_list in jlpt_kanji.iteritems():
    data += '\n'
    data += group(kanji_list)
data += '</body>'

data += '</html>'

with open(os.path.join(settings.OUTPUT, 'known_kanji_jlpt.html'), 'w') as f:
    f.write(data);

