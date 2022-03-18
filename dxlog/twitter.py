import requests
import tweepy
import time
from better_profanity import profanity
from dxlog.base import *

def load_profanity_filter():
	profanity.load_censor_words(whitelist_words=['thug', 'hooker', 'junkie', 'god', 'hell'])

def tweet(config, playthrough_data, events, mod, version):
	if len(events) == 0:
		return
	if config["twit_bearer_token"]=="" or config["twit_consumer_key"]=="" or config["twit_consumer_secret"]=="" or config["twit_access_token"]=="" or config["twit_access_token_secret"]=="":
		return
	
	twitApi = tweepy.Client( bearer_token=config["twit_bearer_token"], 
								consumer_key=config["twit_consumer_key"], 
								consumer_secret=config["twit_consumer_secret"], 
								access_token=config["twit_access_token"], 
								access_token_secret=config["twit_access_token_secret"], 
								return_type = requests.Response,
								wait_on_rate_limit=True)
	load_profanity_filter()	
	for event in events:
		msg = gen_event_msg(event, playthrough_data, mod, version)
		if msg!=None:
			send_tweet(twitApi,msg)


def damage_string(dmgtype):
	if dmgtype=="shot":
		return "was murdered"
	elif dmgtype=="teargas":
		return "was tear gassed to death"
	elif dmgtype=="poisongas":
		return "was poison gassed to death"
	elif dmgtype=="radiation":
		return "was radiated to death"
	elif dmgtype=="halongas":
		return "was gassed to death"
	elif dmgtype=="poisoneffect" or dmgtype=="poison":
		return "was poisoned to death"
	elif dmgtype=="sabot" or dmgtype=="autoshot":
		return "was filled with holes"
	elif dmgtype=="burned" or dmgtype=="flamed":
		return "was burned to death"
	elif dmgtype=="drowned":
		return "drowned"
	elif dmgtype=="emp" or dmgtype=="shocked":
		return "was shocked to death"
	elif dmgtype=="exploded":
		return "was blown to bits"
	elif dmgtype=="fell":
		return "was splattered all over the floor"
	else:
		if dmgtype:
			err('unknown dmgtype: '+dmgtype)
		return 'was killed'


def location_to_string(location):
	location = location_split.split(location)
	x = round(float(location[0]), 3)
	y = round(float(location[1]), 3)
	z = round(float(location[2]), 3)
	return str(x)+', '+str(y)+', '+str(z)


def censor_name(name):
	name = profanity.censor(name)
	if name.count('*') >= len(name)*0.7:
		name = 'Inappropriate Name'
	return name

def gen_death_msg(isPlayer, event, location):
	victim = ''
	if 'victim' in event:
		victim = event['victim']
	else:# player is deprecated
		victim = event.get('player')

	safeVictimName = censor_name(victim)
	killer = event.get('killer')
	dmgtype = event.get('dmgtype')
	msg = safeVictimName+" "+damage_string(dmgtype.lower())
	
	if (killer==victim):
		msg+=" by themselves"
	elif killer:
		msg+=' by '+censor_name(killer)
	
	if 'mapname' in event:
		msg += ' in '+event['mapname'] + ' (Mission: ' + str(event['mission']).zfill(2) + ')'
	else:
		msg+=" in "+event['map']
	
	if location:
		msg+="\n\nPosition: " + location_to_string(location)
	else:
		msg+='\n'
	return msg


def twitter_sanitize(val):
	if not val:
		return ''
	return str(val).replace('#', '').replace('@', '')

def gametime_to_string(time):
	time = int(float(time) / 10)
	return str(datetime.timedelta(seconds=time))


mod_names = { 'DeusEx': '', 'GMDXRandomizer': 'GMDX', 'RevRandomizer': 'Revision', 'HXRandomizer': 'HX', 'VMDRandomizer': 'VanillaMadder' }
flag_to_character_names = {
	'TerroristCommander_Dead': 'Terrorist Commander',
	'TiffanySavage_Dead': 'Tiffany Savage',
	'PaulDenton_Dead': 'Paul Denton'
}

def gen_event_msg(event,d,mod,version):
	msg = None
	
	info("Generating message for event: "+str(event))
	
	if "type" not in event:
		err("Event has no type field")
		return None

	for k in event:
		event[k] = twitter_sanitize(event[k])
	seed = twitter_sanitize(d.get('seed'))
	flagshash = twitter_sanitize(d.get('flagshash'))
	mod = twitter_sanitize(mod)
	version = twitter_sanitize(version)
	
	# player died
	if event['type']=='DEATH':
		msg = gen_death_msg(True, event, event['location'])
	
	# important character died, only works for vanilla with injects/shims
	# Check against the character list to see if they deserve a tweet
	elif event['type']=='PawnDeath':
		if event['victimBindName']+"_Dead" in flag_to_character_names:
			msg = gen_death_msg(False, event, event['location'])
		else:
			info('PawnDeath unknown name: '+event['victimBindName'])

	# flag for character's death, we assume the player killed them, location is None or player's location?
	elif event['type']=='Flag' and event['flag'] in flag_to_character_names:
		event['victim'] = flag_to_character_names[event['flag']]
		event['killer'] = event['PlayerName']
		#immediate = event['immediate'] # we might need this, maybe to ignore the location?
		msg = gen_death_msg(False, event, event.get('location'))
	
	elif event["type"]=="BeatGame":
		ending = int(event["ending"])
		if   ending==1:
			msg = event["PlayerName"]+" destroyed Area 51, beginning a new dark age\n"
		elif ending==2:
			msg = event["PlayerName"]+" merged with Helios to create a benevolent cybernetic dictatorship\n"
		elif ending==3:
			msg = event["PlayerName"]+" killed Bob Page and joined the Illuminati to rule the world unopposed\n"
		elif ending==4:
			msg = event["PlayerName"]+" decided this whole conspiracy thing was boring and decided to have a dance party instead\n"
		else:
			#unknown ending
			err("Unknown ending value "+str(event["ending"]))
			return None
		msg+= "\nTime: "+gametime_to_string(event["time"])
		if 'loadout' in event and event['loadout'] != 'All Items Allowed':
			msg+= '\nLoadout: '+event['loadout']
		if 'deaths' in event:
			msg+= '\nDeaths: '+str(event['deaths'])+', Save count: '+str(event['SaveCount'])

	elif event['type']=='Trigger' and event['tag']=='MadeBasket':
		msg = 'Sign '+event['instigator']+' up for the Knicks!!!! (Mission: ' + str(event['mission']).zfill(2) + ')\n'

	elif event['type']=='Flag' and event['flag']=='BathroomBarks_Played':
		msg = 'By the way, '+event['PlayerName']+', stay out of the ladies restroom. That kind of activity embarasses the agency more than it does you.\n'
	elif event['type']=='Flag' and event['flag']=='ManBathroomBarks_Played':
		msg = 'By the way, '+event['PlayerName']+', stay out of the men\'s restroom. That kind of activity embarasses the agency more than it does you.\n'
	elif event['type']=='Flag' and event['flag']=='GotHelicopterInfo':
		msg = '\"Oh my god! '+event['PlayerName']+'! A bomb!\"\nJock found and disarmed the bomb planted in his helicopter by the fake mechanic.\n'
	elif event['type']=='Flag' and event['flag']=='JoshFed':
		msg = event['PlayerName']+' gave some food to Josh the homeless kid in Battery Park in exchange for some info about the soda machine\n'
	elif event['type']=='Flag' and event['flag']=='M02BillyDone':
		msg = event['PlayerName']+' gave some food to Billy the homeless kid in Castle Clinton for some info about the NSF tunnels\n'
	elif event['type']=='Flag' and event['flag']=='FordSchickRescued':
		msg = event['PlayerName']+' successfully rescued Ford Schick from the MJ12 base in the New York sewers\n'
	elif event['type']=='Flag' and event['flag']=='M10EnteredBakery':
		msg = event['PlayerName']+' went looking for a nice baguette in the Paris bakery\n'
	elif event['type']=='Flag' and event['flag']=='AlleyCopSeesPlayer_Played':
		msg = event['PlayerName']+' got caught doing a bit of breaking and entering in Paris\n'
	elif event['type']=='Flag' and event['flag']=='FreshWaterOpened':
		msg = event['PlayerName']+' opened up a fresh water supply for the people living in Brooklyn Bridge Station\n'
	elif event['type']=='Flag' and event['flag']=='assassinapartment':
		msg = event['PlayerName']+' decided to pay a visit to the local assassin\n'
	elif event['type']=='Flag' and event['flag']=='GaveRentonGun':
		msg = event['PlayerName']+' gave a weapon to Gilbert Renton so he could defend his hotel\n'
	elif event['type']=='Flag' and event['flag']=='MiguelHack_Played':
		msg = event['PlayerName']+' helped Miguel escape the MJ12 facility under UNATCO HQ\n'
	elif event['type']=='Flag':
		info('Flag event, unknown flag name: '+event['flag'])
    
	else:
		err("Unrecognized event type: "+str(event["type"]))
		return None
		
	
	if seed:
		msg += '\nSeed: '+str(seed)
		if flagshash:
			msg += ', flagshash: '+str(flagshash)
	
	msg+= "\n#DeusEx #Randomizer"
	if mod and mod_names.get(mod):
		msg += ' #' + mod_names.get(mod)
	if version:
		msg += ' ' + version
	msg = profanity.censor(msg)
		
	return msg

def send_tweet(api,msg):
	info("Tweeting '"+msg+"'")
	tweet = msg

	if len(tweet)>280:
		diff = len(tweet)-280
		tweet = msg[:-diff-3]+"..."
	try:
		response = api.create_tweet(text=tweet)
	except Exception as e:
		err("Encountered an issue when attempting to tweet: "+str(e)+" "+str(e.args))

