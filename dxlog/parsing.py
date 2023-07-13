from dxlog.base import *
import re

parse_content_r1 = re.compile(r'^(?P<loglevel>\w+): (?P<map>[^\.]+)\.(?P<module>[^:]+?)\d+: ((?P<firstword>\w+) )?(?P<remaining>.*)$', flags=re.MULTILINE)
parse_content_r2 = re.compile(r' (?P<key>\w+): (?P<value>[\-\w\d]+)')

def parse_content(content):
	d = {}
	for i in parse_content_r1.finditer(content):
		try:
			t = i.groupdict()
			firstword = t.pop('firstword', None)
			if firstword and 'firstword' not in d and t.get('module')=='DXRFlags':
				d['firstword'] = firstword
			# order is semi-important because we want to keep the first value found for each key
			d = {**d, **t}
			if d.get('remaining') is not None:
				for j in parse_content_r2.finditer(d['remaining']):
					d[j.group('key')] = j.group('value')
			d.pop('remaining', None)
		except Exception as e:
			logex(e)
	if 'map' not in d:
		warn("parse_content didn't find map in: "+content)

	d['events'] = get_events(content)
	return d


def get_json_from_event_msg(eventmsg):
	jsonstr = ""
	
	jsonstart = eventmsg.find("{")
	
	if jsonstart != -1:
		jsonstr = eventmsg[jsonstart:]
		
	return jsonstr

def get_events(content):
	events = []
	for line in content.splitlines():
		try:
			if 'EVENT: ' not in line:
				continue
			eventjsonstr = get_json_from_event_msg(line)
			event = json.loads(eventjsonstr)
			events.append(event)
		except Exception as e:
			err('failed to get_events in line: ' + line)
			logex(e)
	return events
			
		
