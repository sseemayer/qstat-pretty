
from collections import OrderedDict, defaultdict
import xml.etree.ElementTree as ET

def parse_xml(f):
	xml = ET.parse(f)
	root = xml.getroot()

	def process_job(j):
		fields = {
			 'number': ('JB_job_number', int)
			,'priority': ('JAT_prio', float)
			,'name': ('JB_name', str)
			,'owner': ('JB_owner', str)
			,'state': ('state', str)
			,'t_submit': ('JB_submission_time', str)
			,'t_start': ('JAT_start_time', str)
			,'queue': ('queue_name', str)
			,'slots': ('slots', int)
			,'tasks': ('JB_ja_tasks', int)
		}

		def tagtext(t, f):
			if t != None: 
				return f(t.text)
			else: 
				return None

		return { key: tagtext(j.find(tag[0]), tag[1]) for key,tag in fields.items() }

	jobs = [ process_job(job_list) for job_list in  root.find('queue_info') ]

	return jobs
