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

		ret = {}
		
		if ip not in config.get('banned_ips',[]):
			events = d.get('events', [])
			if len(events) > 0:
				info('log_id: '+str(log_id)+', got events: '+repr(events))
			for event in events:
				if event['type'] == 'DEATH':
					log_death(cursor, log_id, event)
				if event["type"] == "BeatGame":
					log_beatgame(cursor, log_id, mod, version, event, d)
				if event['type'] == 'QueryLeaderboard':
					ret.update(QueryLeaderboard(cursor, event, d.get('playthrough_id')))
			tweet(config, d, events, mod, version)
		else:
			warn("IP " + ip + " is banned!")
		
		db.commit()
		if d.get('firstword'):
			ret.update(select_deaths(cursor, mod, d.get('map')))
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


def log_beatgame(cursor, log_id, mod, version, e, d):
	if VersionStringToInt(version) < VersionToInt(2, 3, 0, 1):
		return
	try:
		bingo_spots = 0
		for x in range(0,5):
			for y in range(0,5):
				bingoTag = "bingo-"+str(x)+"-"+str(y)
				square = e.get(bingoTag)
				if square and square['progress'] >= square['max'] and square['event'] != "Free Space":
					bingo_spots += 1

		name = unrealscript_sanitize(e['PlayerName'])
		
		cursor.execute(
			'INSERT INTO leaderboard SET '
			+ 'log_id=%s, name=%s,  totaltime=%s,  gametime=%s,           score=%s,   flagshash=%s,       setseed=%s,      stable_version=%s,              rando_difficulty=%s,   combat_difficulty=%s,   deaths=%s,   loads=%s,       saves=%s,       bingos=%s,           bingo_spots=%s, ending=%s,   newgameplus_loops=%s,   initial_version=%s',
			(  log_id,    name,     e['realtime'], e['timewithoutmenus'], e['score'], d.get('flagshash'), e['bSetSeed'],   VersionStringIsStable(version), e['rando_difficulty'], e['combat_difficulty'], e['deaths'], e['LoadCount'], e['SaveCount'], e['NumberOfBingos'], bingo_spots,    e['ending'], e['newgameplus_loops'], e['initial_version'])
		)
	except Exception as ex:
		err('log_beatgame failed', log_id, e)
		logex(ex)


def QueryLeaderboard(cursor, event, playthrough_id):
	cursor.execute("SELECT "
		+ "name, totaltime as time, score, leaderboard.flagshash, setseed, seed, UNIX_TIMESTAMP()-UNIX_TIMESTAMP(created) as age, playthrough_id "
		+ "FROM leaderboard JOIN logs ON(leaderboard.log_id=logs.id) "
		+ "WHERE initial_version >= %s AND age < 31622400 "# max age of 366 days
		+ " ORDER BY score DESC",
		(VersionToInt(2,3,0,0),))

	placement = 1
	users = set()
	leaderboard = []
	newplacement = 0
	for (d) in cursor:
		name = unrealscript_sanitize(d['name'])
		if event.get('PlayerName') == name and playthrough_id == d['playthrough_id']:
			newplacement = len(leaderboard)
		elif name in users:
			continue
		place = placement
		if name in users:
			place = '--'
		else:
			placement += 1
		arr = [ name, d['score'], d['time'], d['seed'], d['flagshash'], d['setseed'], place, PlaythroughIdToHex(d['playthrough_id']) ]
		leaderboard.append(arr)
		users.add(name)
	
	# TODO: split the leaderboard to show your position
	ret = {}
	for i in range(min(15,len(leaderboard))):
		ret['leaderboard-'+str(i)] = leaderboard[i]
	return ret


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
