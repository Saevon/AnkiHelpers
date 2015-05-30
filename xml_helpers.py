#!/usr/bin/env python
# -*- coding: UTF-8 -*-


def get_child(elem, tag):
    if elem is None:
        return None

    for child in elem:
        if child.tag == tag:
            return child
    return None


def get_kanji(character):
    elem = get_child(character, 'literal')

    if elem is None:
        return None
    return elem.text

def grade(character):
    elem = get_child(character, 'misc')
    elem = get_child(elem, 'grade')

    if elem is None:
        return None
    return int(elem.text)

def halpern(character):
    elem = get_child(character, 'dic_number')
    if elem is None:
        return None

    for child in elem:
        if child.attrib['dr_type'] == "halpern_kkld":
            return int(child.text)

    return None

def strokes(character):
    elem = get_child(character, 'misc')
    elem = get_child(elem, 'stroke_count')

    if elem is None:
        return None
    return int(elem.text)
