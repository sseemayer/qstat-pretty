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


TABLE_ALGORITHMS = {}


def table_algorithm(name):
    def inner(f):
        TABLE_ALGORITHMS[name] = f
        return f
    return inner


import qstatpretty.ttyutil.resize.fit
import qstatpretty.ttyutil.resize.grow
