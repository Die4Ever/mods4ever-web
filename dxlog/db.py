import mysql.connector
import mysql.connector.errorcode
from dxlog.base import *
from dxlog.parsing import parse_content, get_deaths, get_events
from dxlog.twitter import tweet

def db_connect(config):
	db = None
	
	dbconfig = {}
	dbconfig["user"]=config["user"]
	dbconfig["password"]=config["password"]
	dbconfig["host"]=config["host"]
	dbconfig["database"]=config["database"]
	dbconfig["raise_on_warnings"]=config["raise_on_warnings"]
	
	try:
		db = mysql.connector.connect(**dbconfig)
	except Exception as e:
		print("failed to connect to db")
		err("failed to connect to db")
		logex(e)
	return db


def write_db(mod, version, ip, content, config):
	ret = {}
	db = db_connect(config)
	cursor = None
	
	if db == None:
		return ret
	
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
		deaths = get_deaths(content)
		events = get_events(content)
		events.extend(deaths)
		info("got events: "+repr(events))
		for event in events:
			if event['type'] == 'DEATH':
				log_death(cursor, log_id, event)
		tweet(config, d, events, mod, version)
		db.commit()
		ret = {}
		if d.get('firstword'):
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
	if 'playthrough_id' in d and 'seed' in d and 'flagshash' in d:
		return d
	if 'playthrough_id' not in d:
		cursor.execute("SELECT playthrough_id, seed, flagshash FROM logs WHERE ip=%s ORDER BY id DESC LIMIT 1", (ip,))
	else:
		cursor.execute("SELECT playthrough_id, seed, flagshash FROM logs WHERE ip=%s AND playthrough_id=%s ORDER BY id DESC LIMIT 1", (ip,d['playthrough_id']))
	for (r) in cursor:
		if 'playthrough_id' in r:
			d['playthrough_id'] = r['playthrough_id']
		if 'seed' in r and 'seed' not in d:
			d['seed'] = r['seed']
		if 'flagshash' in r and 'flagshash' not in d:
			d['flagshash'] = r['flagshash']
	return d

# for k in [0: 'num', 1: 'name', 2: 'killer', 3: 'damagetype', 4: 'age', 5: 'x', 6: 'y', 7: 'z', 8: 'killerclass']:
def compare_deaths(a, b):
	# name
	if a[1] != b[1]:
		return False

	# age, difference of 1 hour
	if abs(a[4] - b[4]) > 3600:
		return False
	
	# x, y, z, checking for > 100 feet
	dist = math.sqrt((a[5] - b[5]) ** 2 + (a[6] - b[6]) ** 2 + (a[7] - b[7]) ** 2)
	if dist > 16*100:
		return False
	
	return True

def filter_deaths(deaths):
	if not deaths:
		return deaths
	
	for d in deaths.values():
		d[0] = int(d[0])
		d[4] = int(d[4])
		d[5] = float(d[5])
		d[6] = float(d[6])
		d[7] = float(d[7])
	
	keys = sorted(deaths.keys(), key=lambda d: deaths[d][4])
	end = len(keys)
	
	i = 0
	while i < end:
		j = i + 1
		bads = 0
		while j < end:
			if compare_deaths(deaths[keys[i]], deaths[keys[j]]):
				bads += 1
				if bads > 3:
					deaths[keys[i]][0] += 1
					del keys[j]
					end -= 1
					j -= 1
			j += 1
		i += 1
	
	newdeaths = {}
	for k in keys[:50]:
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

	# select more than we want, because filter_deaths will remove the excess
	cursor.execute("SELECT "
		+ "deaths.id as deathid, modname, ip, name, killer, killerclass, damagetype, x, y, z, TIME_TO_SEC(TIMEDIFF(now(), created)) as age "
		+ "FROM deaths JOIN logs on(deaths.log_id=logs.id) "
		+ "WHERE map=%s "
		+ modcondition
		+ " ORDER BY created DESC LIMIT 100", (map,))
	
	for (d) in cursor:
		# need to sanitize these because unrealscript's json parsing isn't perfect
		key = 'deaths.' + str(d['deathid']) #d['x']+','+d['y']+','+d['z']
		d.pop('ip', None)
		d['num'] = 1
		ret[key] = []
		for k in ['num', 'name', 'killer', 'damagetype', 'age', 'x', 'y', 'z', 'killerclass']:
			s = unrealscript_sanitize(d[k])
			if not s:
				s = ''
			ret[key].append(s)
	
	return filter_deaths(ret)

		
def log_death(cursor, log_id, death):
	info(repr(death))
	location = location_split.split(death['location'])
	cursor.execute("INSERT INTO deaths SET log_id=%s, name=%s, killer=%s, killerclass=%s, damagetype=%s, x=%s, y=%s, z=%s",
		(log_id, death['victim'], death.get('killer'), death.get('killerclass'), death.get('dmgtype'), location[0], location[1], location[2]))

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
	create_table(db, "logs", "map varchar(255), created datetime, version varchar(255), ip varchar(100), message varchar(30000), seed int unsigned, flagshash int unsigned, modname varchar(255), firstword varchar(255), playthrough_id int unsigned, INDEX(modname, seed, playthrough_id, created), INDEX(modname, created), INDEX(firstword, created), INDEX(map, created), INDEX(playthrough_id,map,created)" + base)

