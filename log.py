#!/usr/bin/python3
# -*- coding: UTF-8 -*-# enable debugging

from csv import excel_tab
from ctypes import sizeof
import sys
if sys.version_info[0] < 3:
	raise ImportError('Python < 3 is unsupported.')

if sys.version_info[0] == 3 and sys.version_info[1] < 5:
	raise ImportError('Python < 3.5 is unsupported.')

import cgitb
import time
#import requests
import json
import os
import datetime
import pathlib
import mysql.connector
import mysql.connector.errorcode
import re
import traceback

path = os.path.dirname(os.path.realpath(__file__))
logdir = path + "/dxrando_logs/"

def main():
	#cgitb.enable(display=1, logdir=logdir)

	print("Status: 200" )
	print("")
	ip = os.environ.get('REMOTE_ADDR')
	#info( ip )

	content, content_length = get_content()

	if ip is None:
		run_tests()
		return

	response = {}
	if len(content) != content_length:
		response['status'] = "ERROR: only received "+str(len(content))+"/"+str(content_length)+" bytes"
	else:
		response['status'] = "ok received "+str(len(content))+"/"+str(content_length)+" bytes"

	qps = query_params()
	version = qps.get('version', "v1.0.0")
	mod = qps.get('mod')

	if VersionStringToInt(version) < VersionToInt(1, 7, 2, 9):
		response['notification'] = "New v1.7.2 available!"
		response['message'] = "Many updates!|nWould you like to visit https://github.com/Die4Ever/deus-ex-randomizer/releases now?"

	write_log(mod, version, ip, content, response)
	try:
		db_data = write_db(mod, version, ip, content)
		response.update(db_data)
	except Exception as e:
		print("failed to write to db")
		err("failed to write to db")
		logex(e)

	print_response(mod, version, response)


def print_response(mod, version, response):
	if VersionStringToInt(version) >= VersionToInt(1, 7, 3, 3):
		print(json.dumps(response))
	else:
		print(response['status'])
		if 'notification' in response:
			print("notification: " + response['notification'])
			print(response['message'])


def get_db_config():
	with open(path+'/config.json', 'r') as f:
		return json.load(f)
	err("failed to load db config")
	return {}


def db_connect():
	config = get_db_config()
	db = None
	try:
		db = mysql.connector.connect(**config)
	except Exception as e:
		print("failed to connect to db")
		err("failed to connect to db")
		logex(e)
	return db


def write_db(mod, version, ip, content):
	ret = {}
	db = db_connect()
	cursor = None
	try:
		#create_tables(db)
		cursor = db.cursor(dictionary=True)
		d = parse_content(content)
		d = get_playthrough(cursor, mod, ip, d)
		cursor.execute(
			"INSERT INTO logs SET created=NOW(), "
			+ "firstword=%s, modname=%s, version=%s, ip=%s, message=%s, map=%s, seed=%s, flagshash=%s, playthrough_id=%s",
			(d.get('firstword'), mod, version, ip, content, d.get('map'), d.get('seed'), d.get('flagshash'), d.get('playthrough_id') ))
		log_id = cursor.lastrowid
		info("inserted logs id "+str(log_id))
		for d in get_deaths(content):
			log_death(cursor, log_id, d)
		db.commit()
		ret = select_deaths(cursor, mod, d.get('map'))
	except Exception as e:
		print("failed to write to db")
		err("failed to write to db")
		logex(e)
	
	db.commit()
	cursor.close()
	db.close()
	return ret


def get_playthrough(cursor, mod, ip, d):
	if 'playthrough_id' in d:
		return d
	cursor.execute("SELECT playthrough_id FROM logs WHERE ip=%s ORDER BY id DESC LIMIT 1", (ip,))
	for (r) in cursor:
		if 'playthrough_id' in r:
			d['playthrough_id'] = r['playthrough_id']
	return d

def unrealscript_sanitize(s):
	allow = "-_[]\{\}()`~!@#$%^&*\+=|;:<>,."
	s = re.sub('[^\w\d %s]' % allow, '', str(s))
	s = re.sub('\s+', ' ', s)
	return s


def compare_deaths(a, b):
	if a['name'] != b['name']:
		return False
	if abs(a['age'] - b['age']) > 3600:
		return False
	if abs(a['x'] - b['x']) > 16*10:
		return False
	if abs(a['y'] - b['y']) > 16*10:
		return False
	if abs(a['z'] - b['z']) > 16*10:
		return False
	return True

def filter_deaths(deaths):
	for d in deaths.values():
		d['age'] = int(d['age'])
		d['x'] = float(d['x'])
		d['y'] = float(d['y'])
		d['z'] = float(d['z'])
	
	keys = sorted(deaths, key=lambda d: deaths[d]['age'])
	end = len(keys)
	
	i = 0
	while i < end:
		j = i + 1
		bads = 0
		while j < end:
			if compare_deaths(deaths[keys[i]], deaths[keys[j]]):
				bads += 1
				if bads > 3:
					del keys[j]
					end -= 1
					j -= 1
			j += 1
		i += 1
	
	newdeaths = {}
	for k in keys:
		newdeaths[k] = deaths[k]
	return newdeaths


def select_deaths(cursor, mod, map):
	if not map:
		map = "01_nyc_unatcoisland"
	ret = {}
	# we select more than we return because we might combine some, or choose some more spread out ones instead of just going by age?
	modcondition = ""
	if mod == "RevRandomizer":
		modcondition = " AND modname == \"RevRandomizer\" "
	else:
		modcondition = " AND NOT modname <=> \"RevRandomizer\" "

	cursor.execute("SELECT "
		+ "deaths.id as deathid, modname, ip, name, killer, killerclass, damagetype, x, y, z, TIME_TO_SEC(TIMEDIFF(now(), created)) as age "
		+ "FROM deaths JOIN logs on(deaths.log_id=logs.id) "
		+ "WHERE map=%s "
		+ modcondition
		+ " ORDER BY created DESC LIMIT 50", (map,))
	
	for (d) in cursor:
		# need to sanitize these because unrealscript's json parsing isn't perfect
		key = 'deaths.' + str(d['deathid']) #d['x']+','+d['y']+','+d['z']
		d.pop('ip', None)
		ret[key] = [1] # 1 death in the group
		for k in ['name', 'killer', 'damagetype', 'age', 'x', 'y', 'z', 'killerclass']:
			s = unrealscript_sanitize(d[k])
			ret[key].append(s)
	
	return filter_deaths(ret)

def parse_content(content):
	d = {}
	r = re.compile(r'^(?P<level>\w+): (?P<map>[^\.]*)\.(?P<module>[^:]+)\d+: ((?P<firstword>\w+) (?P<remaining>.*)$)?', flags=re.MULTILINE)
	r2 = re.compile(r' (?P<key>\w+): (?P<value>[\w\d]+)')
	for i in r.finditer(content):
		try:
			t = i.groupdict()
			firstword = t.pop('firstword', None)
			if  firstword and 'firstword' not in d and t.get('module')=='DXRFlags':
				d['firstword'] = firstword
			d.update(t)
			if d.get('remaining') is not None:
				for j in r2.finditer(d['remaining']):
					d[j.group('key')] = j.group('value')
			d.pop('remaining', None)
		except Exception as e:
			logex(e)
	if 'map' not in d:
		warn("parse_content didn't find map in: "+content)
	return d

def get_deaths(content):
	deaths = []
	r = re.compile(
		r'^DEATH: [^:]+: (?P<player>.*) was killed( by (?P<killerclass>.*?) (?P<killer>.*?))?( with (?P<dmgtype>.*?) damage)? in (?P<map>.*?) \((?P<x>.*?),(?P<y>.*?),(?P<z>.*?)\)'
		, flags=re.MULTILINE)
	for i in r.finditer(content):
		d = i.groupdict()
		deaths.append(d)
	return deaths

def log_death(cursor, log_id, death):
	info(repr(death))
	cursor.execute("INSERT INTO deaths SET log_id=%s, name=%s, killer=%s, killerclass=%s, damagetype=%s, x=%s, y=%s, z=%s",
		(log_id, death['player'], death['killer'], death['killerclass'], death['dmgtype'], death['x'], death['y'], death['z']))

def try_exec(cursor, query):
	try:
		cursor.execute(query)
	except mysql.connector.Error as e:
		if e.errno == mysql.connector.errorcode.ER_TABLE_EXISTS_ERROR:
			print("table already exists.")
		else:
			logex(e)
		return ()
	except Exception as e:
		logex(e)
		return ()
	return cursor


def create_table(db, name, desc):
	cursor = db.cursor()
	desc = "CREATE TABLE " + name + " (" + desc + ")"
	curr_desc = ""

	results = try_exec(cursor, "SHOW CREATE TABLE "+name)
	for (table, tdesc) in results:
		curr_desc = tdesc
	
	if curr_desc.count(',') != desc.count(','):
		info("old table: "+curr_desc)
		try_exec(cursor, "DROP TABLE old_"+name)
		try_exec(cursor, "RENAME TABLE "+name+" TO old_"+name)
		info("create_table: "+desc)
		try_exec(cursor, desc)
	cursor.close()


def create_tables(db):
	base = ", id int unsigned NOT NULL AUTO_INCREMENT, PRIMARY KEY(id)"
	create_table(db, "deaths", "log_id int unsigned, name varchar(255), killer varchar(255), killerclass varchar(255), damagetype varchar(255), x float, y float, z float" + base)
	create_table(db, "logs", "map varchar(255), created datetime, version varchar(255), ip varchar(100), message varchar(30000), seed int unsigned, flagshash int unsigned, modname varchar(255), firstword varchar(255), playthrough_id int unsigned, INDEX(modname, seed, playthrough_id, created), INDEX(modname, created), INDEX(firstword, created), INDEX(map, created)" + base)


# copied from DXRando
def VersionToInt(major, minor, patch, build):
	return int(major)*1000000+int(minor)*10000+int(patch)*100+int(build)

def VersionStringToInt(version):
	try:
		m = re.search(r'v(\d+)\.(\d+)\.(\d+)(\.(\d+))?', version)
		group5 = m.group(5)
		if group5 is None:
			group5 = "0"
		return VersionToInt(m.group(1), m.group(2), m.group(3), group5)
	except Exception as e:
		print("VersionStringToInt error parsing "+version)
		logex(e)
	return 0

def parse_query_string(q):
	d = {}
	for m in re.finditer(r'(([^=]+)=([^\&]+)&?)', q):
		d[m.group(2)] = m.group(3).replace("%20", " ")
	return d

def query_params():
	if os.environ.get('QUERY_STRING'):
		return parse_query_string(os.environ.get('QUERY_STRING'))
	return {}


def write_log(mod, version, ip, content, response):
	try:
		now = datetime.datetime.now()
		foldername = logdir + now.strftime("%Y-%m") +"/"
		filename = foldername + ip + "_" + version + ".txt"
		pathlib.Path(foldername).mkdir(parents=True, exist_ok=True)
		with open( filename, "a") as file:
			file.write( "\n" + now.strftime("%Y-%m-%d %H:%M:%S") + ": " + version + ": " + response['status'] +"\n" + content + "\n")
	except Exception as e:
		logex(e)


def get_content():
	s_content_length = os.environ.get('CONTENT_LENGTH')
	if s_content_length is None:
		s_content_length = "0"
	else:
		s_content_length = str(s_content_length)

	content_length = int(s_content_length)
	content = ""

	try:
		#while len(args) < content_length AND (datetime.datetime.now() - now).total_seconds() < 10:
		if content_length > 0:
			content = content + sys.stdin.read()
			content = content.replace('\x00','').replace('\r','')
	except Exception as e:
		logex(e)
	
	return content, content_length


class MockFailCursor:
	def execute(self, q):
		raise Exception("MockFailCursor: "+q)

def run_tests():
	info("running tests...")

	# ensure proper error handling
	results = try_exec(MockFailCursor(), "expected failure")
	for t in (results):
		err("we shouldn't hit this")
	
	for d in get_deaths("\nDEATH: 01_NYC_UNATCOIsland.JCDentonMale2: JC Denton was killed by SecurityBot3 UJ-31 with shot damage in 01_NYC_UNATCOISLAND (-502.167694,40.753559,-119.199997)\nDEATH: 01_NYC_UNATCOIsland.JCDentonMale2: Die4Ever was killed in 01_NYC_UNATCOISLAND (-502.167694,40.753559,-119.199997)\nDEATH: 01_NYC_UNATCOIsland.JCDentonMale2: JC Denton was killed with shot damage in 01_NYC_UNATCOISLAND (-502.167694,40.753559,-119.199997)\nDEATH: 01_NYC_UNATCOIsland.JCDentonMale2: JC Denton was killed with  damage in 01_NYC_UNATCOISLAND (-502.167694,40.753559,-119.199997)"):
		info(repr(d))
	
	info("testing parse_content")
	d = parse_content("DX.DXRando0: RandoEnter() firstTime: True, IsTravel: False, seed: 601088 DX\nINFO: DX.DXRando0: randomizing DX using seed 601088\nINFO: DX.DXRFlags0: PreFirstEntry DX DeusEx.DXRFlags - v1.7.3.5 Beta, seed: 601088, flagshash: 90622488, playthrough_id: 1686707255, flagsversion: 1070305, gamemode: 0, difficulty: 1.000000, loadout: 0, brightness: 15, newgameplus_loops: 0, autosave: 2, crowdcontrol: 0, codes_mode: 2\nDEATH: 01_NYC_UNATCOIsland.JCDentonMale8: JC Denton was killed by JCDentonMale JC Denton with exploded damage in 01_NYC_UNATCOISLAND (748.419373,-433.573730,-123.300003)\nINFO: 01_NYC_UNATCOIsland.JCDentonMale8: Speed Enhancement deactivated")
	print(d['firstword'])
	assert d['firstword'] == "PreFirstEntry"

	d = parse_query_string("version=v1.2.3 Alpha&mod=DeusEx&another=param")
	assert d['version'] == "v1.2.3 Alpha"
	assert d['mod'] == "DeusEx"
	assert d['another'] == "param"

	assert VersionStringToInt(d['version']) == VersionToInt(1, 2, 3, 0)
	assert VersionStringToInt("v1.3.1") == VersionToInt(1, 3, 1, 0)
	assert VersionStringToInt("v1.7.2.5") == VersionToInt(1, 7, 2, 5)
	assert VersionStringToInt("v1.7.3.5 Alpha") == VersionToInt(1, 7, 3, 5)

	info(unrealscript_sanitize("this is a test, Die4Ever; ok: another test {      } \\  bye "))

	d = {'name':'Die4Ever', 'age':3600, 'x':0, 'y':0, 'z':0}
	d2 = d.copy()
	d2['name'] = 'TheAstropath'
	d3 = d.copy()
	d3['age'] = '3000'
	d3['x'] = 10
	d4 = d.copy()
	d4['x'] = '1600'
	deaths = filter_deaths({'a':d, 'b':d2, 'c':d3, 'd':d, 'e':d4, 'f':d, 'g':d3, 'h':d})
	info("filter_deaths down to "+repr(deaths))
	assert len(deaths) == 6
	
	info("path: "+os.path.dirname(os.path.realpath(__file__)))
	info("cwd: "+os.getcwd())
	info("logdir: "+logdir)
	info("db config: " + repr(get_db_config()))
	#write_db("0", "test")
	info("test success")

error_log = logdir + "error_log"
def write_error_log(msg):
	print(msg, file=sys.stderr)
	with open(error_log, "a") as file:
			file.write(msg+"\n")


def info(msg):
	write_error_log("INFO: "+msg)

def warn(msg):
	write_error_log("WARNING: "+msg)

def err(msg):
	write_error_log("ERROR: "+msg)

def logex(e):
	write_error_log("ERROR: "+traceback.format_exc())

main()
