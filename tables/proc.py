#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import re

def proc(fname, ):
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
    freqs = { }
    freq_sum = 0.0

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

                freq = int(mat.group('freq'))
                freqs[sym] = freq

                freq_sum += freq

                key = u'{0}{1}{2}{3}'.format(k0, k1, k2, k3)

                if key in rules:
                    rules[key].append(sym)
                else:
                    rules[key] = [sym]

    for k, v in freqs.iteritems():
        freqs[k] = v / freq_sum * 100.0

    return rules, freqs

if __name__ == '__main__':
    jidian, freq1 = proc('jidian86.txt')
    haifeng, freq2 = proc('haifeng86.txt')

    def merge(d1, d2, fn):
        result = dict(d1)
        for k,v in d2.iteritems():
            if k in result:
                result[k] = fn(result[k], v)
            else:
                result[k] = v
        return result

    merged = merge(jidian, haifeng, lambda x, y: list(set(x)|set(y)))
    freqs = merge(freq1, freq2, lambda x, y: x+y)

    with codecs.open('chinese-wubu-rules.txt', 'w', encoding='utf-8') as f:
        for it in iter(sorted(merged.iteritems())):
            key = '"' + it[0] + '"'
            arr = sorted(it[1], key=lambda x: freqs[x], reverse=True)
            chrs = repr([format(x.encode('utf-8')) for x in arr]).decode('string-escape')
            msg = '({key:<7}{chrs})\n'.format(key=key, chrs=chrs)
            f.write(msg.decode('utf-8'))
