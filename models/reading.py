#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from HTMLParser import HTMLParser
from kana import all_to_hiragana, extend_dakuten_reading, extend_mini_reading
from printable import PrintableList



def tuple_to_dict(lst):
    out = {}
    for tpl in lst:
        out[tpl[0]] = tpl[1]

    return out

class StringList(PrintableList):

    def __init__(self, *args, **kwargs):
        super(StringList, self).__init__(*args, **kwargs)

        self.keys = {}
        for index, item in enumerate(list.__iter__(self)):
            self.keys[str(item)] = index

    def __contains__(self, item):
        return item in self.keys.keys() or list.__contains__(self, item)

    def index(self, item):
        index = self.keys.get(item, None)
        if index is not None:
            return index

        return list.index(self, item)


class ReadingString(object):

    def __init__(self, reading, string):
        self.reading = reading
        self.string = string

    def __str__(self):
        return self.string

    def __eq__(self, other):
        return self.string == other

    def __gt__(self, other):
        return self.string > other

    def __len__(self):
        return len(unicode(self))

    def __getitem__(self, key):
        return unicode(self)[key]

    def get_reading(self):
        return self.reading

    def add_use(self, use):
        return self.reading.add_use(use)

    @property
    def uses(self):
        return self.reading.uses


class Reading(object):

    TYPE_END = 'ending'
    TYPE_OPT = 'optional'

    TYPES = (
        TYPE_END,
        TYPE_OPT,
    )

    COLOUR_END = u'#4b60ff'
    COLOUR_OPT = u'#e4240d'
    COLOUR_OPT2 = u'#cd1c2a'

    MAPPING = {
        COLOUR_END: TYPE_END,
        COLOUR_OPT: TYPE_OPT,
        COLOUR_OPT2: TYPE_OPT,

    }

    class Error(Exception):
        pass

    # create a subclass and override the handler methods
    class KanjiParser(HTMLParser):

        @staticmethod
        def attr_to_type(attrs):
            colour = attrs.get('color', False)
            if not colour:
                return False

            type = Reading.MAPPING.get(colour, False)
            if not type:
                raise Reading.Error("Invalid Color: %s" % colour)

            return type


        def handle_data(self, data):
            self.reading.append(all_to_hiragana(data), type=self._type)

        def handle_endtag(self, tag):
            if tag != 'font':
                raise Reading.Error("Invalid Reading End Tag <%s>" % tag)

            self._reset_type()

        def handle_starttag(self, tag, attrs):
            attrs = tuple_to_dict(attrs)

            # Validate the tag
            if tag != 'font':
                raise Reading.Error("Invalid Reading Tag <%s>" % tag)

            # Validate the type
            type = self.attr_to_type(attrs)
            if not type:
                return

            # Validate the state change
            if self._type is not None:
                raise Reading.Error("Invalid State Change, nested type")

            # Now we can do the actual state change
            self._set_type(type)

        def read_parts(self, html):
            self.reading = Reading()
            self._reset_type()

            self.feed(html)
            return self.reading

        def _reset_type(self):
            return self._set_type(None)

        def _set_type(self, type):
            if type is None:
                self._type = None
            else:
                self._type = type

    @classmethod
    def generate(cls, string):
        parser = cls.KanjiParser()
        try:
            return parser.read_parts(string)
        except Exception as err:
            raise Exception("ParseError: '%s' in string: %s" % (err, string))


    def __init__(self):
        self._parts = []

        self._empty = True
        self._special = False
        self._has_ending = False

        self.uses = []

    def append(self, data, type=None):
        # Validate
        if type is None:
            if self._special:
                raise Reading.Error("Normal Characters after Special Characters in Reading: %s, data: %s" % (self, data))
            self._empty = False
        elif type is not None:
            if self._empty:
                raise Reading.Error("Reading starts with special Characters: %s, data: %s" % (self, data))
            if self._has_ending:
                raise Reading.Error("Reading already ended: %s, data: %s" % (self, data))

            if type == Reading.TYPE_END:
                self._has_ending = True

            self._special = True

        # Add the data
        self._parts.append({
            'data': data,
            'type': type,
        })

    def __str__(self):
        out = ''
        for part in self._parts:
            if part['type'] is None:
                out += '<%(data)s>' % part
            else:
                out += '<%(type)s: %(data)s>' % part

        return out

    def get_all(self):
        readings = PrintableList()

        for part in self._parts:
            if part['type'] is None:
                for index, reading in enumerate(readings):
                    readings[index] = reading + part['data']
                else:
                    readings.append(part['data'])
            elif part['type'] == Reading.TYPE_OPT:
                readings.append(readings[-1] + part['data'])

        # Now add all the dakuten extensions
        extended = PrintableList()
        for reading in readings:
            for new_reading in extend_dakuten_reading(reading):
                extended.append(new_reading)

        final = PrintableList()
        for reading in extended:
            for new_reading in extend_mini_reading(reading):
                final.append(new_reading)

        # Now filter out duplicates
        final = set(final)
        final = StringList([self.__wrapper(string) for string in final])

        return final

    def __wrapper(self, string):
        return ReadingString(self, string)

    def add_use(self, use):
        self.uses.append(use)
