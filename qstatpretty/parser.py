from datetime import datetime
import xml.etree.ElementTree as ET
import itertools
import subprocess
import re


class Parser(object):
    _cmd = 'qstat'

    def __str__(self):
        return self._name

    def tagtext(self, t, f):
        if t is not None:
            return f(t.text)
        else:
            return None

    def parse_time(self, t):
        return datetime.fromtimestamp(float(t))

    @classmethod
    def getParser(cls, source):

        SOURCES = {
            'local':
                lambda x: subprocess.Popen(
                    ['man', cls._cmd],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                ).stdout,
            'ssh':
                lambda x: subprocess.Popen(
                    ['ssh', x[1], 'bash', '-lc',
                        '"source /etc/profile; {} -h"'.format(cls._cmd)],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE
                ).stdout
        }

        stream = SOURCES[source[0]](source)
        stream = ''.join(stream.readlines())

        result = re.search(r'(-x)\s+(.*?XML.*?)\.', stream)
        if result is not None:
            return ParserTorque()
        else:
            return ParserGridEngine()

    def getCmd(self):
        return [self._cmd, self._xml_flag]

    def getCmdStr(self):
        return "{} {}".format(self._cmd, self._xml_flag)


class ParserGridEngine(Parser):

    def __init__(self):
        super(ParserGridEngine, self).__init__()
        self._xml_flag = '-xml'
        self._name = 'GridEngine'

    def process_job(self, j):
        fields = {
            'number': ('JB_job_number', int),
            'priority': ('JAT_prio', float),
            'name': ('JB_name', str),
            'owner': ('JB_owner', str),
            'state': ('state', str),
            't_submit': ('JB_submission_time', parse_time),
            't_start': ('JAT_start_time', parse_time),
            'queue': ('queue_name', str),
            'slots': ('slots', int),
            'tasks': ('tasks', str)
        }

        jobs = {}

        for key, tag in fields.items():
            jobs[key] = tagtext(j.find(tag[0]), tag[1])

        jobs['t_submit_start'] = jobs['t_submit'] or jobs['t_start']

        return jobs

    def parse_xml(self, f):
        xml = ET.parse(f)
        root = xml.getroot()

        parse_time = lambda t: datetime.strptime(t,  '%Y-%m-%dT%H:%M:%S')
        job_lists = itertools.chain(
            root.find('queue_info'), root.find('job_info'))
        jobs = [process_job(job_list) for job_list in job_lists]

        return jobs


class ParserTorque(Parser):

    def __init__(self):
        super(ParserTorque, self).__init__()
        self._xml_flag = '-x'
        self._name = 'Torque Resource Manager'

    def process_job(self, j):
        fields = {
            'number': ('Job_Id', str),
            'priority': ('Priority', int),
            'name': ('Job_Name', str),
            'owner': ('Job_Owner', str),
            'state': ('job_state', str),
            't_submit': ('qtime', self.parse_time),
            't_start': ('start_time', self.parse_time),
            'queue': ('queue', str),
            'host': ('submit_host', str),
        }

        def tagtext(t, f):
            if t is not None:
                return f(t.text)
            else:
                return None

        jobs = {}

        for key, tag in fields.items():
            jobs[key] = tagtext(j.find(tag[0]), tag[1])

        jobs['t_submit_start'] = jobs['t_submit'] or jobs['t_start']
        try:
            cput = next(j.iter('cput')).text
            jobs['t_comp'] = cput
        except StopIteration:
            jobs['t_comp'] = ''

        # remove HOST
        jobs['owner'] = jobs['owner'].replace(jobs['host'], 'HOST')
        jobs['number'] = jobs['number'].replace(jobs['host'], 'HOST')

        return jobs

    def parse_xml(self, f):
        try:
            xml = ET.parse(f)
        except ET.ParseError:
            return []  # no jobs!
        root = xml.getroot()

        job_list = root.iter('Job')
        jobs = [self.process_job(job) for job in job_list]

        return jobs
