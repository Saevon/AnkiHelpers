#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from printable import PrintableDict, PrintableList


class TestFailure(Exception):
    def __init__(self, msg=None, reason=None):
        super(TestFailure, self).__init__()

        self.reason = reason
        if msg is None:
            self.string = None
        else:
            self.string = msg.encode('utf-8','ignore')

    def __str__(self):
        msgs = (self.reason, self.string)

        return ': '.join([val for val in msgs if val is not None])

class BoolFailure(TestFailure):
    pass


def test_equal(a, b, reason=None):
    if a != b:
        raise TestFailure(u"(%s != %s):" % (a, b), reason=reason)


def test_true(val, reason=None):
    if not val:
        raise BoolFailure(reason=reason)

def test_list_equal(lsta, lstb, reason=None):
    lsta = list(lsta)
    lstb = list(lstb)

    if len(lsta) != len(lstb):
        raise TestFailure(u"(%s != %s):" % (PrintableList(lsta), PrintableList(lstb)), reason=reason)

    for index in range(len(lsta)):
        if lsta[index] != lstb[index]:
            raise TestFailure(u"(%s != %s):" % (PrintableList(lsta), PrintableList(lstb)), reason=reason)


