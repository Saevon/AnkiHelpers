#!/usr/bin/python
# -*- coding: UTF-8 -*-

from contextlib import contextmanager
import sqlite3


class AnkiModel(object):

    class Error(Exception):
        pass

    FIELD_SEP = '\x1f'

    # Sub-Class Customizations
    DATA_PATH = '/Users/serghei/Documents/Saves/Anki/Saevon/collection.anki2'

    FIELDS = tuple()

    FINDER = '1=1'
    TYPE_ID = None

    KEY = None

    @classmethod
    @contextmanager
    def execute(cls):
        conn = sqlite3.connect(AnkiModel.DATA_PATH)
        cursor = conn.cursor()

        yield cursor

        conn.commit()
        conn.close()

    @classmethod
    def select(cls, command):
        with cls.execute() as cursor:
            out = cursor.execute(command).fetchall()

        return out

    @classmethod
    def update(cls, command):
        with cls.execute() as cursor:
            cursor.execute(command)
            out = cursor.rowcount

        return out


    @classmethod
    def load_all(cls):
        cls._cards = []
        cls._cards_map = {}
        cls._card_pk_map = {}

        finder = cls.FINDER

        if cls.TYPE_ID is not None:
            finder += ' AND mid = %s' % cls.TYPE_ID

        for row in cls.select('SELECT id, flds, tags from notes WHERE %s;' % finder):
            kwargs = {}
            kwargs['tags'] = row[2]
            kwargs['id'] = row[0]
            kwargs['suspended'] = False

            # Now we need to parse the custom FIELDS
            fields = row[1].split(AnkiModel.FIELD_SEP)

            if len(fields) < len(cls.FIELDS):
                raise AnkiModel.Error("Not enough fields found: FIELDS(len %i), Actual(len %i)" % (
                    len(cls.FIELDS),
                    len(fields)
                ))

            # Now actually parse the fields
            for field in cls.FIELDS:
                kwargs[field] = fields.pop(0)

            obj = cls(kwargs)
            cls._cards.append(obj)
            cls._cards_map[obj.id] = obj

        # Now we get extra information about these cards
        ids = map(lambda card: str(card.id), cls._cards)
        for row in cls.select('SELECT nid, queue from cards WHERE nid in (%s)' % ','.join(ids)):
            card_id = row[0]
            suspended = row[1] == -1

            if suspended:
                card = cls.get_id(card_id)
                card.suspended = True

    def mark_suspended(self, boolean):
        '''
        Marks all of the Cards for this Note as Suspended (or not) depending on the boolean
        '''
        # Now we get extra information about these cards
        print 'UPDATE cards SET queue=cards.type WHERE nid=%s' % (
            self.id,
        )
        AnkiModel.update('UPDATE cards SET queue=cards.type WHERE nid=%s;' % (
            self.id,
        ))

    def __init__(self, data):
        for field, value in data.iteritems():
            setattr(self, field, value)

        if self.KEY:
            key = getattr(self, self.KEY)
            self.store(key, self)


    loaded = False
    ensuring = False

    @classmethod
    def reload(cls):
        cls.loaded = False

    @classmethod
    def ensure_load(cls):
        # We need to make sure we can use some of these methods
        # even though technically the cards aren't "loaded" yet
        if cls.ensuring:
            return
        if not cls.loaded:
            cls.ensuring = True
            cls.load_all()
            cls.ensuring = False

            cls.loaded = True

    @classmethod
    def store(cls, key, val):
        cls._card_pk_map[key] = val

    @classmethod
    def find(cls, key):
        cls.ensure_load()

        return cls._card_pk_map[unicode(key)]

    @classmethod
    def get_id(cls, id):
        cls.ensure_load()

        return cls._cards_map[id]

    @classmethod
    def all(cls):
        return list(cls.iter_all())

    @classmethod
    def iter_all(cls):
        cls.ensure_load()
        for item in cls._cards:
            yield item
