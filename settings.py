#
# Customizations and settings for this app
#
import os

# Path to your Anki Database
ANKI_PATH = '/Users/serghei/Documents/Saves/Anki/'
ANKI_USER = 'Saevon'
ANKI_DB = 'collection.anki2'


# Relative path for the output folder
OUTPUT = 'output'

# Relative path for the input data folder
DATA = 'data'

# Path for the complex readings file
COMPLEX_READINGS = 'complex.json'

# Path for Kanji dictionary
KANJI_DICT = os.path.join(DATA, 'kanjidic2.xml')

DATA_HEADER = os.path.join(DATA, 'header.html')
DATA_CSS    = os.path.join(DATA, 'main.css')


EXTRA_DICT_KANJI = os.path.join(DATA, 'extra_dict.json')






# Now we setup all the models
from models.anki import AnkiModel
from models.kanji_word import KanjiWord

AnkiModel.setup(os.path.join(ANKI_PATH, ANKI_USER, ANKI_DB))
KanjiWord.setup(os.path.join(DATA, COMPLEX_READINGS))