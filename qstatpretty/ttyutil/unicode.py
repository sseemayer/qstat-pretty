# -*- coding: utf8 -*-

if "unicode" not in dir(__builtins__):
    unicode = lambda x: x
else:
    unicode = unicode

ulen = lambda s: len(unicode(s))
