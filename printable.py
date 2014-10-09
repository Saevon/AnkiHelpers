#!/usr/bin/env python
# -*- coding: UTF-8 -*-


class PrintableList(list):
    '''
    A list which prints kanji properly (for debug)
    '''

    def __values(self):
        for value in self:
            yield u'"%s"' % (value)

    def __unicode__(self):
        return u'[%s]' % u', '.join(self.__values())

def print_list(obj):
    print unicode(PrintableList(obj))

class PrintableDict(dict):
    '''
    A list which prints kanji properly (for debug)
    '''

    def __pairings(self):
        for key, value in self.iteritems():
            yield u'"%s": "%s"' % (key, value)

    def __unicode__(self):
        data = u', '.join(self.__pairings())

        return u'{%s}' % data

def print_dict(obj):
    print unicode(PrintableDict(obj))
