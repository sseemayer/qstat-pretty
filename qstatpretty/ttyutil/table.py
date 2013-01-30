# -*- coding: utf8 -*-


ulen = lambda s: len(unicode(s))

DELIMITERS_DEFAULT = {

    'header_tl':     u"┌",
    'header_t':      u"─",
    'header_tr':     u"┐",
    'header_b':      u"─",
    'header_bl':     u"├",
    'header_l':      u"│",
    'header_r':      u"│",
    'header_br':     u"┤",
    'header_csep_t': u"┬",
    'header_csep_m': u"│",
    'header_csep_b': u"┼",

    'body_r':        u"│",
    'body_br':       u"┘",
    'body_l':        u"│",
    'body_bl':       u"└",
    'body_b':        u"─",
    'body_csep_m':   u"│",
    'body_csep_b':   u"┴",

}


DELIMITERS_MINIMAL = {

    'header_tl':     u"",
    'header_t':      u"",
    'header_tr':     u"",
    'header_b':      u"─",
    'header_bl':     u"",
    'header_l':      u"",
    'header_r':      u"",
    'header_br':     u"",
    'header_csep_t': u"",
    'header_csep_m': u"│",
    'header_csep_b': u"┼",

    'body_r':        u"",
    'body_br':       u"",
    'body_l':        u"",
    'body_bl':       u"",
    'body_b':        u"",
    'body_csep_m':   u"│",
    'body_csep_b':   u"",

}


def pretty_table(tbl, colordef, header_row=True, delimiters=DELIMITERS_DEFAULT):
    from .color import COLOR_BLACK, colortext

    d = delimiters

    max_widths = [max(ulen(c) for c in col) for col in zip(*tbl)]

    tjust = [[u"{:{}s}".format(c, w) for w, c in zip(max_widths, row)] for row in tbl]

    pretty_top = d['header_tl'] + d['header_csep_t'].join(d['header_t'] * w for w in max_widths) + d['header_tr'] + "\n"
    pretty_bottom = d['body_bl'] + d['body_csep_b'].join(d['body_b'] * w for w in max_widths) + d['body_br']

    if header_row:
        header = tjust.pop(0)
        header = [colortext(h, COLOR_BLACK, True) for h in header]

        pretty_colheader = d['header_l'] + d['header_csep_m'].join(header) + d['header_r']
        pretty_underline = d['header_bl'] + d['header_csep_b'].join(d['header_b'] * w for w in max_widths) + d['header_br']
        pretty_header = pretty_colheader + "\n" + pretty_underline + "\n"

        pretty_top = pretty_top + pretty_header

    tjust = [[colortext(t, fmt['color'](t)) for fmt, t in zip(colordef, row)] for row in tjust]

    return pretty_top + "".join(d['body_l'] + d['body_csep_m'].join(row) + d['body_r'] + "\n" for row in tjust) + pretty_bottom
