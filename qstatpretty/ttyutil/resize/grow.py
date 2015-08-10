from qstatpretty.ttyutil.unicode import ulen
from qstatpretty.ttyutil.resize import simple_ellipsis, table_algorithm


@table_algorithm('grow')
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
