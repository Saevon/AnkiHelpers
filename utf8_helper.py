#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import sys


def is_ascii(char):
    '''
    Checks whether the character is within the basic ascii range
    '''
    return ord(char) < 128

def force_UTF8():
    '''
    Forces the print statement to use UTF-8
    '''
    reload(sys)
    sys.setdefaultencoding("UTF-8")

