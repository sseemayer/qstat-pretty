from qstatpretty.ttyutil.unicode import ulen
from qstatpretty.ttyutil.resize import table_algorithm


@table_algorithm('fit')
def fit_table(tbl, width, tbldef, delimiters):
    '''Pad cells to match maximum column width and stretch delimiters'''

    max_widths = [
        max(ulen(col[0]), max(ulen(tbldef[cx]['ellipsis'](c)) for c in col[1:]))
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
