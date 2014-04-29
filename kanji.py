from lxml import etree

def kanji(character):
    elems = character.findall('.//literal')
    if len(elems) == 0:
        return None
    return elems[0].text

def grade(character):
    elems = character.findall('.//grade')
    if len(elems) == 0:
        return None
    return elems[0].text

def halpern(character):
    elems = character.findall('.//dic_ref[@dr_type="halpern_njecd"]')
    if len(elems) == 0:
        return None
    return elems[0].text

def strokes(character):
    elems = character.findall('.//stroke_count')
    if len(elems) == 0:
        return None
    return elems[0].text


def load_anki_data(kanji_list):
    # TODO: get the known kanji
    path = '/Users/serghei/Documents/Saves/Anki/Saevon/collection.anki2'
    import sqlite3
    conn = sqlite3.connect(path)
    c = conn.cursor()

    def is_ascii(char):
        return ord(char) < 128

    known = set()
    for row in c.execute('SELECT flds from notes WHERE tags LIKE "%kanji%" AND NOT tags LIKE "%kanji-word%" AND NOT tags LIKE "%missing-kanji%";'):
        # The first field is the kanji itself
        known.add(row[0][0])

    expected = set()
    for row in c.execute('SELECT flds from notes;'):
        # Keep all non ascii characters only
        [expected.add(char) for char in row[0] if not is_ascii(char)]

    # Now we filter out any non-kanji characters
    expected = [char for char in expected if char in kanji_list]

    # Make sure to log any missing characters that got filtered out
    unknown = [char for char in expected if char not in kanji_list]
    if len(unknown):
        print 'strange: %s' % unknown

    import sys
    reload(sys)
    sys.setdefaultencoding("UTF-8")

    # Now warn the user of any kanji that don't exist as known Notes
    missing = set(expected) - set(known)
    if len(missing):
        import subprocess

        kanji = ' '.join(missing)

        try:
            subprocess.call(
                u'terminal-notifier -message "%(kanji)s" -title "Missing Kanji Found"' % {
                    'kanji': kanji,
                },
                shell=True,
            )
        except OSError as err:
            print err

        # required sudo gem install terminal-notifier
        print 'missing: %s' % ' '.join(missing)

    conn.close()

    return known, expected


import sys
reload(sys)
sys.setdefaultencoding("UTF-8")

with open('kanjidic2.xml', 'r') as f:
    tree = etree.parse(f)

root = tree.getroot()


# Filter out any useless tags keeping only the actual character list
characters = [i for i in root if i.tag == 'character']

char_map = {}

for char in characters:
    # http://www.csse.monash.edu.au/~jwb/kanjidic2/kd2examph.html
    char_map[kanji(char)] = {
        'kanji': kanji(char),
        'grade': grade(char),
        'halpern': halpern(char),
        'strokes': strokes(char),
    }

# Filter out any characters without a halpern number
for key, value in list(char_map.iteritems()):
    if value['grade'] is None:
        char_map.pop(key)

known, expected = load_anki_data(char_map.keys())

# Mark any kanji that are known
for key, value in char_map.iteritems():
    char_map[key]['known'] = value['kanji'] in known


import cgi

def make_char(char):
    data = char.copy()
    data['known'] = 'known' if data['known'] else ''

    data['kanji'] = cgi.escape(data['kanji']).encode('ascii', 'xmlcharrefreplace')

    return '''<div class="kanji %(known)s grade-%(grade)s">%(kanji)s</div>''' % data

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


def group(kanji_list):
    kanji_list = [make_char(char) for char in kanji_list]

    # Make the lines
    kanji_list = chunks(kanji_list, 10)
    kanji_list = [make_line(line) for line in kanji_list]

    # Make the blocks
    kanji_list = chunks(kanji_list, 8)
    kanji_list = [make_block(line) for line in kanji_list]

    return '\n'.join(kanji_list)


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
with open('header.html') as f:
    data = f.read()

data += '<body>'
for grade, kanji_list in grades.iteritems():
    data += '\n'
    data += group(kanji_list)
data += '</body>'

data += '</html>'

with open('known_kanji.html', 'w') as f:
    f.write(data);


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
with open('header.html') as f:
    data = f.read()

data += '<body>'
for count, kanji_list in strokes.iteritems():
    data += '\n'
    data += group(kanji_list)
data += '</body>'

data += '</html>'

with open('known_kanji_strokes.html', 'w') as f:
    f.write(data);



