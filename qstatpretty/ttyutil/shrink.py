# -*- coding: utf-8 -*-
import math

from qstatpretty.ttyutil.unicode import ulen


def simple_value(formatter=str, factor=1, min_width=0, max_width=None, overflow=1):
    """Basic value function for scoring a column width"""

    def sv(content, width):
        content = formatter(content)

        if max_width and width > max_width:
            width = max_width

        if width < min_width:
            return 0

        return min(width, ulen(content)) * factor + math.log(width + 1) * overflow

    return sv


def simple_ellipsis(formatter=str):
    """Basic ellipsis function for scaling a cell"""

    def se(content, width=None):
        content = formatter(content)
        if width is None:
            width = len(content)

        if(ulen(content) <= width):
            return content
        if width > 2:
            return content[0:width - 2] + u"…" + content[-1]

        elif width == 2:
            return content[0:2]
        else:
            return content[0:width]

    return se


DATE_FORMATS = [
    ('%Y-%m-%d %H:%M:%S', 20),
    ('%m-%d %H:%M:%S', 18),
    ('%a %H:%M:%S', 16),
    ('%H:%M:%S', 10),
    ('%H:%M', 5),
    ('%Hh', 2),
    ('%H', 1),
    ('', 0)
]


def best_date_format(content, width):
    return next(df for df in DATE_FORMATS if len(content.strftime(df[0])) <= width)


def date_ellipse(content, width=None):
    if width is None:
        width = float('inf')

    if not content:
        return ''

    return content.strftime(best_date_format(content, width)[0])


def float_ellipse(content, width=2, max_width=7):
    width = min(width, max_width)

    if width > 2:
        try:
            return "{0:.{1}f}".format(content, width - 2)
        except ValueError:
            return str(content)[0:width]
    else:
        return str(content)[0:width]


def grow_table(tbl, width, tbldef, delimiters):

    column_overhead = 0
    margin = 0
    if delimiters:
        d = delimiters
        column_overhead = ulen(d['body_csep_m'])
        margin = ulen(d['body_l'] + d['body_r'])

    width = width - margin
    colwidths = [0] * len(tbldef)

    def scoresum(col, width):
        column = (r[col] for r in tbl[1:])
        return sum(tbldef[col]['fval'](c, width) for c in column)

    def nonempty_cols():
        return sum(1 for i in colwidths if i > 0) - 1

    # keep growing until width is reached
    while sum(colwidths) + column_overhead * nonempty_cols() < width:

        # determine column that benefits most from growing
        scoregain = [
            scoresum(i, w + 1) - scoresum(i, w)
            if w > 0 else float('Inf')
            for i, w in enumerate(colwidths)
        ]
        bestcol = scoregain.index(max(scoregain))

        # grow best column
        colwidths[bestcol] += 1

    def format_cell(i, c, ellipsis_fn):
        if colwidths[i]:
            cf = ellipsis_fn(c, colwidths[i])
            return cf + " " * (colwidths[i] - ulen(cf))
        else:
            return ""

    header = [
        format_cell(i, c, simple_ellipsis())
        for i, c in enumerate(tbl[0])
        if colwidths[i] > 0
    ]

    body = [
        [
            format_cell(i, c, tbldef[i]['ellipsis'])
            for i, c in enumerate(row)
            if colwidths[i] > 0
        ]
        for row in tbl[1:]
    ]

    return [header] + body, delimiters


def fit_table(tbl, width, tbldef, delimiters):
    '''Pad cells to match maximum column width and stretch delimiters'''

    max_widths = [
        max(len(col[0]), max(len(tbldef[cx]['ellipsis'](c)) for c in col[1:]))
        for cx, col in enumerate(zip(*tbl))
    ]

    for rx, row in enumerate(tbl):
        for cx, (w, cell) in enumerate(zip(max_widths, row)):
            if rx > 0:
                tbl[rx][cx] = tbldef[cx]['ellipsis'](cell, width=w)
            else:
                str(cell)

            tbl[rx][cx] = "{0: <{1}}".format(tbl[rx][cx], w)

    return tbl, delimiters


TABLE_ALGORITHMS = {
    'grow': grow_table,
    'fit': fit_table,
}
