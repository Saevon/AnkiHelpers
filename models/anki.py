#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from contextlib import contextmanager
import sqlite3
from random import randrange
from functools import wraps


class AnkiModel(object):

    class Error(Exception):
        pass

    FIELD_SEP = u'\x1f'

    # Sub-Class Customizations
    DATA_PATH = None

    FIELDS = tuple()

    FINDER = '1=1'
    TYPE_ID = None

    KEY = None

    @classmethod
    def setup(cls, **settings):
        path = settings.get('path', None)
        if path is not None:
            cls.DATA_PATH = path

    @classmethod
    @contextmanager
    def execute(cls):
        if AnkiModel.DATA_PATH is None:
            raise AnkiModel.Error('Database not setup')

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
            finder += ' AND mid in (%s)' % ','.join(cls.TYPE_ID)

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
                kwargs[field] = unicode(fields.pop(0))

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
        # Don't change any cards which are already at the right status
        if self.suspended == boolean:
            return

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
    def reload(cls, lazy=True):
        cls.loaded = False

        # Make sure you can force the reload to happen right away
        if not lazy:
            cls.ensure_load()

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

    def needs_loaded(func):
        '''
        Helper decorator, ensures the class is properly loaded before
        the method is called (classmethods only).
        '''
        @wraps(func)
        def wrapper(cls, *args, **kwargs):
            cls.ensure_load()
            return func(cls, *args, **kwargs)

        return wrapper


    @classmethod
    def store(cls, key, val):
        cls._card_pk_map[key] = val

    @classmethod
    @needs_loaded
    def find(cls, key):
        return cls._card_pk_map[unicode(key)]

    @classmethod
    @needs_loaded
    def random(cls):
        return cls._cards[randrange(0, len(cls._cards))]

    @classmethod
    @needs_loaded
    def get_id(cls, id):
        return cls._cards_map[id]

    @classmethod
    def all(cls):
        return list(cls.iter_all())

    @classmethod
    @needs_loaded
    def iter_all(cls):
        for item in cls._cards:
            yield item
