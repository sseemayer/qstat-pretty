import qstatpretty.ttyutil.color as ttycolor
import qstatpretty.ttyutil.table as ttytable
import qstatpretty.ttyutil.shrink as ttyshrink
import qstatpretty.ttyutil.size as ttysize

STATE_COLORS = {
    'c': ttycolor.COLOR_BLUE,  # completed
    'e': ttycolor.COLOR_RED,  # exited
    'h': ttycolor.COLOR_MAGENTA,  # held
    'q': ttycolor.COLOR_YELLOW,  # queued
    'r': ttycolor.COLOR_GREEN,  # running
    't': ttycolor.COLOR_CYAN,  # moving
    's': ttycolor.COLOR_MAGENTA,  # suspended
}


def state_color(s):
    s = s[0].lower()
    try:
        return STATE_COLORS[s]
    except KeyError:
        return None


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


def date_ellipse(content, width):
    if not content:
        return ''

    return content.strftime(best_date_format(content, width)[0])


def float_ellipse(content, width):
    if width > 7:
        width = 7

    if width > 2:
        try:
            return "{0:.{1}f}".format(content, width - 2)
        except ValueError:
            return str(content)[0:width]
    else:
        return str(content)[0:width]


DEFAULT_TABLE_FORMAT = [
    {
        'key': 'number',
        'title': 'job-ID',
        'color': lambda x: None,
        'ellipsis': ttyshrink.simple_ellipsis(),
        'fval': ttyshrink.simple_value(factor=10, overflow=1)
    },
    {
        'key': 'priority',
        'title': 'priorty',
        'color': lambda x: None,
        'ellipsis': float_ellipse,
        'fval': ttyshrink.simple_value(factor=2, max_width=7)
    },
    {
        'key': 'name',
        'title': 'name',
        'color': lambda x: ttycolor.COLOR_MAGENTA,
        'ellipsis': ttyshrink.simple_ellipsis(),
        'fval': ttyshrink.simple_value(factor=10, overflow=2)
    },
    {
        'key': 'owner',
        'title': 'user',
        'color': lambda x: None,
        'ellipsis': ttyshrink.simple_ellipsis(),
        'fval': ttyshrink.simple_value(factor=3)
    },
    {
        'key': 'queue',
        'title': 'queue',
        'color': lambda x: None,
        'ellipsis': ttyshrink.simple_ellipsis(),
        'fval': ttyshrink.simple_value(factor=2, max_width=10)
    },
    {
        'key': 'state',
        'title': 'state',
        'color': state_color,
        'ellipsis': ttyshrink.simple_ellipsis(),
        'fval': ttyshrink.simple_value(factor=100, max_width=5)
    },
    {
        'key': 't_comp',
        'title': 'runtime',
        'color': lambda x: None,
        'ellipsis': ttyshrink.simple_ellipsis(),
        'fval': ttyshrink.simple_value(factor=2, max_width=20)
    },
    {
        'key': 't_start',
        'title': 'started',
        'color': lambda x: None,
        'ellipsis': date_ellipse,
        'fval': ttyshrink.simple_value(factor=2, max_width=25, overflow=1)
    },
    {
        'key': 't_submit',
        'title': 'submitted',
        'color': lambda x: None,
        'ellipsis': date_ellipse,
        'fval': ttyshrink.simple_value(factor=2, max_width=25, overflow=1)
    },
]


def job_table(jobs, table_format=DEFAULT_TABLE_FORMAT):
    header = [col['title'] for col in table_format]
    body = [[job[col['key']]
             if str(job[col['key']]) else ""
             for col in table_format]
            for job in jobs]

    return [header] + body


def pretty_table(jobs, terminal_width=ttysize.terminal_size()[0], table_format=DEFAULT_TABLE_FORMAT, delimiters=ttytable.DELIMITERS_PROFESSIONAL):

    if jobs:
        tbl = job_table(jobs, table_format)
        tbl, delimiters = ttyshrink.fit_table(
            tbl, terminal_width, table_format, delimiters)
        print(ttytable.pretty_table(tbl, table_format, delimiters=delimiters))
