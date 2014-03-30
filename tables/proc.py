#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import re

Han = [
    [0x2E80, 0x2E99],    # Han # So  [26] CJK RADICAL REPEAT, CJK RADICAL RAP
    [0x2E9B, 0x2EF3],    # Han # So  [89] CJK RADICAL CHOKE, CJK RADICAL C-SIMPLIFIED TURTLE
    [0x2F00, 0x2FD5],    # Han # So [214] KANGXI RADICAL ONE, KANGXI RADICAL FLUTE
    0x3005,              # Han # Lm       IDEOGRAPHIC ITERATION MARK
    0x3007,              # Han # Nl       IDEOGRAPHIC NUMBER ZERO
    [0x3021, 0x3029],    # Han # Nl   [9] HANGZHOU NUMERAL ONE, HANGZHOU NUMERAL NINE
    [0x3038, 0x303A],    # Han # Nl   [3] HANGZHOU NUMERAL TEN, HANGZHOU NUMERAL THIRTY
    0x303B,              # Han # Lm       VERTICAL IDEOGRAPHIC ITERATION MARK
    [0x3400, 0x4DB5],    # Han # Lo [6582] CJK UNIFIED IDEOGRAPH-3400, CJK UNIFIED IDEOGRAPH-4DB5
    [0x4E00, 0x9FC3],    # Han # Lo [20932] CJK UNIFIED IDEOGRAPH-4E00, CJK UNIFIED IDEOGRAPH-9FC3
    [0xF900, 0xFA2D],    # Han # Lo [302] CJK COMPATIBILITY IDEOGRAPH-F900, CJK COMPATIBILITY IDEOGRAPH-FA2D
    [0xFA30, 0xFA6A],    # Han # Lo  [59] CJK COMPATIBILITY IDEOGRAPH-FA30, CJK COMPATIBILITY IDEOGRAPH-FA6A
    [0xFA70, 0xFAD9],    # Han # Lo [106] CJK COMPATIBILITY IDEOGRAPH-FA70, CJK COMPATIBILITY IDEOGRAPH-FAD9
    [0x20000, 0x2A6D6],  # Han # Lo [42711] CJK UNIFIED IDEOGRAPH-20000, CJK UNIFIED IDEOGRAPH-2A6D6
    [0x2F800, 0x2FA1D]]  # Han # Lo [542] CJK COMPATIBILITY IDEOGRAPH-2F800, CJK COMPATIBILITY IDEOGRAPH-2FA1D

def build_han_re():
    L = []
    for i in Han:
        if isinstance(i, list):
            f, t = i
            try:
                f = unichr(f)
                t = unichr(t)
                L.append(ur'{0}-{1}'.format(f, t))
            except:
                # A narrow python build, so can't use chars > 65535
                # without surrogate pairs!
                pass
        else:
            try:
                L.append(unichr(i))
            except:
                pass
    han = ur'[{0}]'.format(''.join(L))
    return re.compile(han, re.UNICODE)

def proc():
    fname = "jidian86.txt"
    pat = re.compile(
        ur"""
        INSERT\ INTO\ "phrases"\ VALUES\( # the fixed blahblah
        [0-9]+,                           # id,
        [0-9]+,                           # length of the keys
        [0-9]+,                           # length of the mapped characters
        (?P<k0>[0-9]+|NULL),              # key 1
        (?P<k1>[0-9]+|NULL),              # key 2
        (?P<k2>[0-9]+|NULL),              # key 3
        (?P<k3>[0-9]+|NULL),              # key 4
        [0-9]+,                           # category
        '(?P<sym>.+)',                    # characters
        (?P<freq>[0-9]+|NULL),            # frequence overall
        [0-9]+|NULL\)                     # user frequency
        ;                                 # the ending colon
        """, re.VERBOSE)

    def char(s):
        if u'NULL' == s:
            return ''
        return chr(int(s) + 96)

    rules = { }

    with codecs.open('jidian86.txt', 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            mat = pat.match(line)
            if mat:
                k0 = char(mat.group('k0'))
                k1 = char(mat.group('k1'))
                k2 = char(mat.group('k2'))
                k3 = char(mat.group('k3'))
                sym = mat.group('sym')

                key = u'{0}{1}{2}{3}'.format(k0, k1, k2, k3)

                if key in rules:
                    rules[key].append(sym)
                else:
                    rules[key] = [sym]

    items = iter(sorted(rules.iteritems()))

    with codecs.open('jidian-rules.txt', 'w', encoding='utf-8') as f:
        for it in items:
            key = '"' + it[0] + '"'
            chrs = repr([x.encode('utf-8') for x in it[1]]).decode('string-escape')
            msg = '({key:<7}{chrs})\n'.format(key=key, chrs=chrs)
            f.write(msg.decode('utf-8'))

if __name__ == '__main__':
    proc()
