import qstatpretty.ttyutil.resize as ttyresize
import qstatpretty.ttyutil.color as ttycolor
from qstatpretty.parser import parser

import datetime
import re


try:
    from io import StringIO
except ImportError:
    from cStringIO import StringIO


@parser("lsf")
class LSFParser(object):
    name = 'LSF'
    table_columns = None  # omitted here for readability and defined below
    extline_spaces = 21

    re_dictline_split = re.compile(r'>(?:, ?)|$')

    @staticmethod
    def parse_time(t):
        thisyear = datetime.datetime.now().year
        return datetime.datetime.strptime("{0} {1}".format(thisyear, t), '%Y %a %b %d %H:%M:%S: ')

    @staticmethod
    def starts_with_timestamp(l):
        try:
            LSFParser.parse_time(l[:LSFParser.extline_spaces])
            return True
        except:
            return False

    @staticmethod
    def extline_iter(f):
        """Generator to iterate over and re-join extended lines"""

        buf = StringIO()
        for line in f:
            ext_line = line.startswith(" " * LSFParser.extline_spaces)

            if ext_line:
                buf.write(line[LSFParser.extline_spaces:])

            else:
                if buf.getvalue():
                    yield buf.getvalue()

                buf = StringIO()
                buf.write(line)

        if buf.getvalue():
            yield(buf.getvalue())

    @staticmethod
    def parse_logline(line):
        if "<" in line:
            return LSFParser.parse_dictline(line)
        else:
            return line

    @staticmethod
    def parse_dictline(line):
        res = {}

        for token in LSFParser.re_dictline_split.split(line):
            if " <" in token:
                key, val = token.split(" <", 1)
                res[key] = val
            else:
                res[key] = True

        return res

    @staticmethod
    def get_deep(obj, path, default=None):
        if len(path) == 0:
            return obj

        nxt = path[0]
        if nxt not in obj:
            return default

        return LSFParser.get_deep(obj[nxt], path[1:], default)

    @staticmethod
    def process_buffer(buf, jobs):
        if not buf:
            return

        bl = LSFParser.extline_iter(buf.split("\n"))
        job = {"log": {}}

        line = next(bl)

        while line:
            if not line.strip():
                continue

            if line.startswith(" RUNLIMIT"):
                job['runlimit'] = next(bl).strip()

            elif line.startswith(" MEMORY USAGE"):
                job['memory'] = next(bl).strip()

            elif line.startswith(" SCHEDULING PARAMETERS"):
                job['scheduling'] = [
                    next(bl, "").strip()
                    for _ in range(6)
                ]

            elif line.startswith(" RESOURCE REQUIREMENT DETAILS"):
                job['resources'] = [
                    next(bl, "").strip()
                    for _ in range(4)
                ]

            elif line.startswith("Job"):
                job['log']['init'] = LSFParser.parse_dictline(line)

            elif LSFParser.starts_with_timestamp(line):
                time = LSFParser.parse_time(line[:LSFParser.extline_spaces])
                job['log'][time] = LSFParser.parse_logline(line[LSFParser.extline_spaces:])

            line = next(bl, None)

        res = {
            'number': LSFParser.get_deep(job, ['log', 'init', 'Job'], ""),
            'name': LSFParser.get_deep(job, ['log', 'init', 'Job Name'], ""),
            'owner': LSFParser.get_deep(job, ['log', 'init', 'User'], ""),
            'state': LSFParser.get_deep(job, ['log', 'init', 'Status'], ""),
            'queue': LSFParser.get_deep(job, ['log', 'init', 'Queue'], ""),
            # slots
            # tasks
        }

        for date, log in job['log'].items():
            if not isinstance(log, dict):
                continue

            for logk, logv in log.items():
                if logk.startswith('Submitted from'):
                    res['t_submit'] = date
                elif 'tarted on' in logk:
                    res['t_start'] = date

                    hosts = logv.split("> <")
                    res['slots'] = ", ".join(hosts)

        res['t_submit_start'] = res['t_submit'] or res['t_start']

        jobs.append(res)

    @staticmethod
    def parse(f):

        jobs = []
        buffer = StringIO()
        for line in f:
            if line.startswith("--------"):
                LSFParser.process_buffer(buffer.getvalue(), jobs)
                buffer = StringIO()
            else:
                buffer.write(line)

        LSFParser.process_buffer(buffer.getvalue(), jobs)

        return jobs

    @staticmethod
    def can_parse(f):
        return False  # TODO

    @staticmethod
    def suggest_commandline(args):
        return ['bjobs', '-l'] + args


def lsf_state_color(s):
    s = s.strip()

    if s == 'PEND':
        return ttycolor.COLOR_YELLOW

    if s == 'RUN':
        return ttycolor.COLOR_GREEN

    if s == 'ERROR':
        return ttycolor.COLOR_RED

    return None


LSFParser.table_columns = [
    {
        'key': 'number',
        'title': 'job-ID',
        'color': lambda x: None,
        'ellipsis': ttyresize.simple_ellipsis(),
        'fval': ttyresize.simple_value(factor=10, overflow=0)
    },
    {
        'key': 'name',
        'title': 'name',
        'color': lambda x: ttycolor.COLOR_BLUE,
        'ellipsis': ttyresize.simple_ellipsis(),
        'fval': ttyresize.simple_value(factor=10, overflow=2)
    },
    {
        'key': 'owner',
        'title': 'user',
        'color': lambda x: None,
        'ellipsis': ttyresize.simple_ellipsis(),
        'fval': ttyresize.simple_value(factor=3)
    },
    {
        'key': 'state',
        'title': 'state',
        'color': lsf_state_color,
        'ellipsis': ttyresize.simple_ellipsis(),
        'fval': ttyresize.simple_value(factor=100, max_width=5)
    },
    {
        'key': 't_submit_start',
        'title': 'submitted/started',
        'color': lambda x: None,
        'ellipsis': ttyresize.date_ellipse,
        'fval': ttyresize.simple_value(factor=2, max_width=20)
    },
    {
        'key': 'queue',
        'title': 'queue',
        'color': lambda x: None,
        'ellipsis': ttyresize.simple_ellipsis(),
        'fval': ttyresize.simple_value(factor=2)
    },
    {
        'key': 'slots',
        'title': 'slots',
        'color': lambda x: None,
        'ellipsis': ttyresize.simple_ellipsis(),
        'fval': ttyresize.simple_value()
    },
]
