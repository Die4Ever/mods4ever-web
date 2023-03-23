import mysql.connector
import mysql.connector.errorcode
from dxlog.base import *
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
	dbconfig["charset"]='utf8'
	dbconfig["use_unicode"]=True
	
	try:
		db = mysql.connector.connect(**dbconfig)
	except Exception as e:
		print("failed to connect to db")
		err("failed to connect to db")
		logex(e)
	return db

def try_encodings(content:str, encodings:list):
	bcontent = b''
	ret = ''
	for e in encodings:
		try:
			bcontent = b''
			if len(e) > 1:
				bcontent = content.encode(e[0], e[1])
			else:
				bcontent = content.encode(e[0])
			if len(e) > 1:
				c = bcontent.decode(e[0], e[1])
			else:
				c = bcontent.decode(e[0])
			if not ret and c:
				ret = c
		except Exception as ex:
			try:
				logex(ex)
				err(bcontent, e)
			except Exception as e2:
				logex(e2)
				err(e)

	return ret


def write_db(mod, version, ip, content:str, config, data):
	ret = {}
	db = db_connect(config)
	cursor = None
	
	if db == None:
		return ret
	
	try:
		d=data
		cursor = db.cursor(dictionary=True)
		d = get_playthrough(cursor, mod, ip, d)
		log_id = 0
		try:
			cursor.execute(
				"INSERT INTO logs SET created=NOW(), "
				+ "firstword=%s, modname=%s, version=%s, ip=%s, map=%s, seed=%s, flagshash=%s, playthrough_id=%s",
				(d.get('firstword'), mod, version, ip, d.get('map'), d.get('seed'), d.get('flagshash'), d.get('playthrough_id') ))
			log_id = cursor.lastrowid
			debug("inserted logs id "+str(log_id))
		except Exception as e:
			print("failed to write to db, db values: ", d.get('firstword'), mod, version, ip, d.get('map'), d.get('seed'), d.get('flagshash'), d.get('playthrough_id'))
			err("failed to write to db, db values: ", d.get('firstword'), mod, version, ip, d.get('map'), d.get('seed'), d.get('flagshash'), d.get('playthrough_id'))
			logex(e)
			err(content)
			return
		
		try:
			cursor.execute(
				'INSERT INTO logs_messages SET id=%s, message=%s',
				(log_id, content)
			)
		except Exception as e:
			err("failed to write to db logs_messages, db values: ", d.get('firstword'), mod, version, ip, d.get('map'), d.get('seed'), d.get('flagshash'), d.get('playthrough_id'))
			logex(e)
			err(content)
		
		if ip not in config.get('banned_ips',[]):
			events = d.get('events', [])
			if len(events) > 0:
				info('log_id: '+str(log_id)+', got events: '+repr(events))
			for event in events:
				if event['type'] == 'DEATH':
					log_death(cursor, log_id, event)
				if event["type"] == "BeatGame":
					log_beatgame(cursor, log_id, event, d)
			tweet(config, d, events, mod, version)
		else:
			warn("IP " + ip + " is banned!")
		
		db.commit()
		ret = {}
		if d.get('firstword'):
			ret = select_deaths(cursor, mod, d.get('map'))
	except Exception as e:
		print("failed to write to db, db values: ", d.get('firstword'), mod, version, ip, content, d.get('map'), d.get('seed'), d.get('flagshash'), d.get('playthrough_id'))
		err("failed to write to db, db values: ", d.get('firstword'), mod, version, ip, content, d.get('map'), d.get('seed'), d.get('flagshash'), d.get('playthrough_id'))
		logex(e)
		err(content)
	
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


def log_beatgame(cursor, log_id, event, data):
	try:
		#cursor.execute(
		#	"INSERT INTO leaderboard SET log_id=%s, name=%s",
		#	(log_id, event.get('name'))
		#)
		pass
	except Exception as e:
		err('log_beatgame failed', log_id, event)
		logex(e)

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
