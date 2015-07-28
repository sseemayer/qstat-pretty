from datetime import datetime
import xml.etree.ElementTree as ET
import itertools
import time


def parse_xml(f):
    xml = ET.parse(f)
    root = xml.getroot()

    def parse_time(t):
        return datetime.fromtimestamp(float(t))

    def process_job(j):
        fields = {
            'number': ('Job_Id', str),
            'priority': ('Priority', int),
            'name': ('Job_Name', str),
            'owner': ('Job_Owner', str),
            'state': ('job_state', str),
            't_submit': ('qtime', parse_time),
            't_start': ('start_time', parse_time),
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

    job_list = root.iter('Job')
    jobs = [process_job(job) for job in job_list]

    return jobs
