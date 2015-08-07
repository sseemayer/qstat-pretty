import qstatpretty.ttyutil.shrink as ttyshrink
import qstatpretty.ttyutil.color as ttycolor
from qstatpretty.parser import parser

import datetime
import itertools

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


@parser("gridengine")
class GridEngineParser(object):
    name = 'GridEngine'
    table_columns = None  # omitted here for readability and defined below

    @staticmethod
    def parse_time(t):
        return datetime.datetime.strptime(t, '%Y-%m-%dT%H:%M:%S')

    @staticmethod
    def process_job(j):
        fields = {
            'number': ('JB_job_number', int),
            'priority': ('JAT_prio', float),
            'name': ('JB_name', str),
            'owner': ('JB_owner', str),
            'state': ('state', str),
            't_submit': ('JB_submission_time', GridEngineParser.parse_time),
            't_start': ('JAT_start_time', GridEngineParser.parse_time),
            'queue': ('queue_name', str),
            'slots': ('slots', int),
            'tasks': ('tasks', str)
        }

        job = {}
        for key, (tag, f) in fields.items():
            val = j.find(tag)
            job[key] = f(val.text) if val is not None else None

        job['t_submit_start'] = job['t_submit'] or job['t_start']

        return job

    @staticmethod
    def parse_xml(f):
        xml = ET.parse(f)
        root = xml.getroot()

        job_lists = itertools.chain(root.find('queue_info'), root.find('job_info'))
        jobs = [GridEngineParser.process_job(job_list) for job_list in job_lists]

        return jobs

    @staticmethod
    def can_parse(f):
        try:
            return ET.parse(f).getroot().find('queue_info') is not None
        except:
            return False

    @staticmethod
    def suggest_commandline(args):
        return ['qstat', '-xml'] + args


def gridengine_state_color(s):

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


GridEngineParser.table_columns = [
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
        'ellipsis': ttyshrink.float_ellipse,
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
        'color': gridengine_state_color,
        'ellipsis': ttyshrink.simple_ellipsis(),
        'fval': ttyshrink.simple_value(factor=100, max_width=5)
    },
    {
        'key': 't_submit_start',
        'title': 'submitted/started',
        'color': lambda x: None,
        'ellipsis': ttyshrink.date_ellipse,
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
