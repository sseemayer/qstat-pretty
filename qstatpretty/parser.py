from datetime import datetime
import xml.etree.ElementTree as ET
import itertools


def parse_xml(f):
    xml = ET.parse(f)
    root = xml.getroot()

    parse_time = lambda t: datetime.strptime(t,  '%Y-%m-%dT%H:%M:%S')

    def process_job(j):
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

        def tagtext(t, f):
            if t is not None:
                return f(t.text)
            else:
                return None


        jobs = {}

        for key, tag in fields.items():
                jobs[key] = tagtext(j.find(tag[0]), tag[1])

        return jobs

        #return {key: tagtext(j.find(tag[0]), tag[1]) for key, tag in fields.items()}

    job_lists = itertools.chain( root.find('queue_info'), root.find('job_info'))

    jobs = [process_job(job_list) for job_list in job_lists]

    return jobs
