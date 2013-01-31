import qstatpretty.ttyutil.color as ttycolor
import qstatpretty.ttyutil.table as ttytable
import qstatpretty.ttyutil.shrink as ttyshrink
import qstatpretty.ttyutil.size as ttysize


def state_color(s):

    if "E" in s:
        return ttycolor.COLOR_RED

    if "T" in s:
        return ttycolor.COLOR_RED

    if "d" in s:
        return ttycolor.COLOR_BLUE

    if "h" in s:
        return ttycolor.COLOR_MAGENTA

    if "q" in s:
        return ttycolor.COLOR_YELLOW

    if "r" in s:
        return ttycolor.COLOR_GREEN

    if "t" in s:
        return ttycolor.COLOR_CYAN

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
        return "{:.{}f}".format(content, width - 2)
    else:
        return str(content)[0:width]


DEFAULT_TABLE_FORMAT = [
    {
        'key': 'number',
        'title': 'job-ID',
        'color': lambda x: None,
        'ellipsis': ttyshrink.simple_ellipsis(),
        'fval': ttyshrink.simple_value(factor=10, overflow=0)
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
        'color': lambda x: ttycolor.COLOR_BLUE,
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
        'key': 'state',
        'title': 'state',
        'color': state_color,
        'ellipsis': ttyshrink.simple_ellipsis(),
        'fval': ttyshrink.simple_value(factor=100, max_width=5)
    },
    {
        'key': 't_submit',
        'title': 'submitted',
        'color': lambda x: None,
        'ellipsis': date_ellipse,
        'fval': ttyshrink.simple_value(factor=2, max_width=20)
    },
    {
        'key': 't_start',
        'title': 'started',
        'color': lambda x: None,
        'ellipsis': date_ellipse,
        'fval': ttyshrink.simple_value(factor=2, max_width=20)
    },
    {
        'key': 'queue',
        'title': 'queue',
        'color': lambda x: None,
        'ellipsis': ttyshrink.simple_ellipsis(),
        'fval': ttyshrink.simple_value(factor=2)
    },
    {
        'key': 'slots',
        'title': 'slots',
        'color': lambda x: None,
        'ellipsis': ttyshrink.simple_ellipsis(),
        'fval': ttyshrink.simple_value(max_width=5)
    },
    {
        'key': 'tasks',
        'title': 'tasks',
        'color': lambda x: None,
        'ellipsis': ttyshrink.simple_ellipsis(),
        'fval': ttyshrink.simple_value(max_width=5)
    }
]


def job_table(jobs, table_format=DEFAULT_TABLE_FORMAT):

    header = [col['title'] for col in table_format]
    body = [[job[col['key']] if job[col['key']] else "" for col in table_format] for job in jobs]

    return [header] + body


def pretty_table(jobs, terminal_width=ttysize.terminal_size()[0], table_format=DEFAULT_TABLE_FORMAT, delimiters=ttytable.DELIMITERS_DEFAULT):

    if jobs:
        tbl = job_table(jobs, table_format)
        tbl = ttyshrink.grow_table(tbl, terminal_width, table_format, delimiters)
        print(ttytable.pretty_table(tbl, table_format, delimiters=delimiters))
