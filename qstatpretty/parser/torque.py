import qstatpretty.ttyutil.shrink as ttyshrink
import qstatpretty.ttyutil.color as ttycolor
from qstatpretty.parser import parser

import datetime

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


@parser("torque")
class TorqueParser(object):
    name = 'Torque Resource Manager'
    table_columns = None  # omitted here for readability and defined below

    @staticmethod
    def process_job(j):
        fields = {
            'number': ('Job_Id', str),
            'priority': ('Priority', int),
            'name': ('Job_Name', str),
            'owner': ('Job_Owner', str),
            'state': ('job_state', str),
            't_submit': ('qtime', TorqueParser.parse_time),
            't_start': ('start_time', TorqueParser.parse_time),
            'queue': ('queue', str),
            'host': ('submit_host', str),
        }

        job = {}
        for key, (tag, f) in fields.items():
            val = j.find(tag)
            if val is not None:
                job[key] = f(val)

        job['t_submit_start'] = job['t_submit'] or job['t_start']

        try:
            cput = next(j.iter('cput')).text
            job['t_comp'] = cput

        except StopIteration:
            job['t_comp'] = ''

        # remove HOST
        job['owner'] = job['owner'].replace(job['host'], 'HOST')
        job['number'] = job['number'].replace(job['host'], 'HOST')

        return job

    @staticmethod
    def parse_time(t):
        return datetime.fromtimestamp(float(t))

    @staticmethod
    def parse_xml(self, f):
        try:
            xml = ET.parse(f)
        except ET.ParseError:
            return []  # no jobs!

        root = xml.getroot()

        job_list = root.iter('Job')
        jobs = [TorqueParser.process_job(job) for job in job_list]

        return jobs

    @staticmethod
    def can_parse(f):
        try:
            return ET.parse(f).getroot().find('Job') is not None
        except:
            return False

    @staticmethod
    def suggest_commandline(args):
        return ['qstat', '-x'] + args


STATE_COLORS = {
    'c': ttycolor.COLOR_BLUE,  # completed
    'e': ttycolor.COLOR_RED,  # exited
    'h': ttycolor.COLOR_MAGENTA,  # held
    'q': ttycolor.COLOR_YELLOW,  # queued
    'r': ttycolor.COLOR_GREEN,  # running
    't': ttycolor.COLOR_CYAN,  # moving
    's': ttycolor.COLOR_MAGENTA,  # suspended
}


def torque_state_color(s):
    s = s[0].lower()
    try:
        return STATE_COLORS[s]
    except KeyError:
        return None


TorqueParser.table_format = [
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
        'ellipsis': ttyshrink.float_ellipse,
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
        'color': torque_state_color,
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
        'ellipsis': ttyshrink.date_ellipse,
        'fval': ttyshrink.simple_value(factor=2, max_width=25, overflow=1)
    },
    {
        'key': 't_submit',
        'title': 'submitted',
        'color': lambda x: None,
        'ellipsis': ttyshrink.date_ellipse,
        'fval': ttyshrink.simple_value(factor=2, max_width=25, overflow=1)
    },
]
