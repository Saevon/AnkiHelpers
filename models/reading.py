#!/usr/bin/python
# -*- coding: UTF-8 -*-
from HTMLParser import HTMLParser


def tuple_to_dict(lst):
    out = {}
    for tpl in lst:
        out[tpl[0]] = tpl[1]

    return out

class PrintableList(list):
    def __str__(self):
        out = '['
        out += ', '.join(self)
        out += ']'
        return out


class Reading(object):

    TYPE_END = 'ending'
    TYPE_OPT = 'optional'

    TYPES = (
        TYPE_END,
        TYPE_OPT,
    )

    COLOUR_END = u'#4b60ff'
    COLOUR_OPT = u'#e4240d'

    MAPPING = {
        COLOUR_END: TYPE_END,
        COLOUR_OPT: TYPE_OPT,
    }

    class Error(Exception):
        pass

    # create a subclass and override the handler methods
    class KanjiParser(HTMLParser):

        @staticmethod
        def attr_to_type(attrs):
            type = attrs.get('color', False)
            if not type:
                return False

            type = Reading.MAPPING.get(type, False)
            if not type:
                return False

            return type


        def handle_data(self, data):
            self.reading.append(data, type=self._type)

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
        return parser.read_parts(string)

    def __init__(self):
        self._parts = []

        self._empty = True
        self._special = False
        self._has_ending = False

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

        return readings
