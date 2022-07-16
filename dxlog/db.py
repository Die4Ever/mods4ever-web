import mysql.connector
import mysql.connector.errorcode
from dxlog.base import *
from dxlog.parsing import parse_content, get_deaths, get_events
from dxlog.twitter import tweet
from dxlog.deaths import *

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
		try:
			content = content.encode('utf8', 'xmlcharrefreplace').decode('ascii')
		except Exception as e:
			logex(e)
			content = content.encode('utf8', 'xmlcharrefreplace').decode('utf8')
		d = parse_content(content)
		d = get_playthrough(cursor, mod, ip, d)
		cursor.execute(
			"INSERT INTO logs SET created=NOW(), "
			+ "firstword=%s, modname=%s, version=%s, ip=%s, message=%s, map=%s, seed=%s, flagshash=%s, playthrough_id=%s",
			(d.get('firstword'), mod, version, ip, content, d.get('map'), d.get('seed'), d.get('flagshash'), d.get('playthrough_id') ))
		log_id = cursor.lastrowid
		debug("inserted logs id "+str(log_id))
		deaths = get_deaths(content)
		events = get_events(content)
		events.extend(deaths)
		if len(events) > 0:
			info('log_id: '+str(log_id)+', got events: '+repr(events))
		for event in events:
			if event['type'] == 'DEATH':
				log_death(cursor, log_id, event)
		tweet(config, d, events, mod, version)
		db.commit()
		ret = {}
		if d.get('firstword'):
			ret = select_deaths(cursor, mod, d.get('map'))
	except Exception as e:
		print("failed to write to db, db values: ", d.get('firstword'), mod, version, ip, content, d.get('map'), d.get('seed'), d.get('flagshash'), d.get('playthrough_id'))
		err("failed to write to db, db values: ", d.get('firstword'), mod, version, ip, content, d.get('map'), d.get('seed'), d.get('flagshash'), d.get('playthrough_id'))
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

