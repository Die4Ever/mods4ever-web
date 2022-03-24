import requests
import tweepy
import time
from better_profanity import profanity
from dxlog.base import *

def load_profanity_filter():
	profanity.load_censor_words(whitelist_words=['thug', 'hooker', 'junkie', 'god', 'hell', 'urinal'])

#Add "prevent_tweet":true to the config.json to prevent actually sending tweets
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
			if "prevent_tweet" in config and config["prevent_tweet"]==True:
				info("Would have tweeted:\n"+msg)
			else:
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
	elif dmgtype=='stomped':
		return 'asked to be stepped on'
	elif dmgtype=='stunned':
		return 'was stunned'
	elif dmgtype=='knockedout':
		return 'was knocked out'
	elif dmgtype=='suicided':
		return 'was killed'
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
	if not name:
		return ''
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

	if not isPlayer and 'PlayerName' in event and event['PlayerName'] != killer:
		safePlayerName = censor_name(event['PlayerName'])
		msg += " under "+safePlayerName+"'s watch"
	
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


def BeatGameMsg(event):
	ending = int(event["ending"])
	player = censor_name(event['PlayerName'])
	if   ending==1:
		msg = player+" destroyed Area 51, beginning a new dark age\n"
	elif ending==2:
		msg = player+" merged with Helios to create a benevolent cybernetic dictatorship\n"
	elif ending==3:
		msg = player+" killed Bob Page and joined the Illuminati to rule the world unopposed\n"
	elif ending==4:
		msg = player+" decided this whole conspiracy thing was boring and decided to have a dance party instead\n"
	else:
		#unknown ending
		err("Unknown ending value "+str(event["ending"]))
		return None
	msg+= "\nTime: "+gametime_to_string(event["time"])
	if event.get('loadout') and event['loadout'] != 'All Items Allowed':
		msg+= '\nLoadout: '+event['loadout']
	if event.get('GameMode') and event['GameMode'] != 'Original Story':
		msg+= '\nGame Mode: '+event['GameMode']
	if 'deaths' in event:
		msg+= '\nDeaths: '+str(event['deaths'])+', Save count: '+str(event['SaveCount'])
	return msg


def FlagEventMsg(event):
	flag = event.get('flag')
	player = censor_name(event['PlayerName'])
	if flag=='BathroomBarks_Played':
		return 'By the way, '+player+', stay out of the ladies restroom. That kind of activity embarasses the agency more than it does you.\n'
	elif flag=='ManBathroomBarks_Played':
		return 'By the way, '+player+', stay out of the men\'s restroom. That kind of activity embarasses the agency more than it does you.\n'
	elif flag=='GotHelicopterInfo':
		return '\"Oh my god! '+player+'! A bomb!\"\nJock found and disarmed the bomb planted in his helicopter by the fake mechanic.\n'
	elif flag=='JoshFed':
		return player+' gave some food to Josh the homeless kid in Battery Park in exchange for some info about the soda machine\n'
	elif flag=='M02BillyDone':
		return player+' gave some food to Billy the homeless kid in Castle Clinton for some info about the NSF tunnels\n'
	elif flag=='FordSchickRescued':
		return player+' successfully rescued Ford Schick from the MJ12 base in the New York sewers\n'
	elif flag=='NiceTerrorist_Dead':
		return 'Jesus Christ, '+player+'. Didn\'t you hear Paul? He ordered the militia to stand down.\n'
	elif flag=='M10EnteredBakery':
		return player+' went looking for a nice baguette in the Paris bakery\n'
	elif flag=='AlleyCopSeesPlayer_Played':
		return player+' got caught doing a bit of breaking and entering in Paris\n'
	elif flag=='FreshWaterOpened':
		return player+' opened up a fresh water supply for the people living in Brooklyn Bridge Station\n'
	elif flag=='assassinapartment':
		return player+' decided to pay a visit to the local assassin\n'
	elif flag=='GaveRentonGun':
		return player+' gave a weapon to Gilbert Renton so he could defend his hotel\n'
	elif flag=='DXREvents_LeftOnBoat':
		return player+" was afraid of flying and took the boat back to UNATCO HQ\n"
	elif flag=='AlleyBumRescued':
		return player+" rescued the bum who was being mugged on the basketball court\n"
	elif flag=='FoundScientistBody':
		return player+" dove into the collapsed Canal road in search of treasure\n"
	elif flag=='ClubMercedesConvo1_Done':
		return player+" kindly paid to get Mercedes and Tessa into the Lucky Money club\n"
	elif flag=='M08WarnedSmuggler':
		return player+" warned Smuggler of the impending UNATCO raid\n"
	elif flag=='ShipPowerCut':
		return player+" shut off the electricity on the lower decks of the Superfreighter\n"
	elif flag=='CamilleConvosDone':
		return player+" decided to spend some time with Camille the cage dancer at La Porte De L\'Enfer\n"
	elif flag=='MeetAI4_Played':
		return player+" spent some time listening to the musings of Morpheus, the Echelon prototype\n"
	elif flag=='DL_Flooded_Played':
		return player+" visited the flooded southern wing of the ocean lab\n"
	elif flag=='JockSecondStory':
		return player+" helped Jock get a nice buzz before he goes on duty\n"
	elif flag=='M07ChenSecondGive_Played':
		return player+" had a nice night out with the boys at the Lucky Money\n"
	elif flag=='DeBeersDead':
		return player+" decided to save a bit of electricity by deactivating Lucius DeBeers' life support\n"
	else:
		info('Flag event, unknown flag name: '+flag)
	return None

def TriggerEventMsg(event):
	tag = event.get('tag')
	
	if tag=='MadeBasket':
		return 'Sign '+event['instigator']+' up for the Knicks!!!! (Mission: ' + str(event['mission']).zfill(2) + ')\n'
	elif tag=='nsfwander':
		return event['PlayerName']+' helped Miguel escape the MJ12 facility under UNATCO HQ\n'
	else:
		info('Trigger event, unknown tag name: '+tag)
		

	return None

def ExtinguishFireMsg(event):
	extinguisher = event.get('extinguisher')
	msg = event['PlayerName']+" was on fire but "
	if   extinguisher=='clean toilet':
		msg+="managed to splash water from a toilet to put it out\n"
	elif extinguisher=='filthy toilet':
		msg+="managed to splash water from an absolutely filthy toilet to put it out\n"
	elif extinguisher=='clean urinal':
		msg+="somehow managed to splash water from a urinal to put it out\n"
	elif extinguisher=='filthy urinal':
		msg+="somehow managed to splash water from a disgusting urinal to put it out\n"
	elif extinguisher=='shower':
		msg+="took a nice shower to put it out\n"
	else:
		return None
		
	#mapname should always be there, but just in case...
	if 'mapname' in event:
		msg += '\n\n'+event['mapname'] + ' (Mission: ' + str(event['mission']).zfill(2) + ')'
	else:
		msg+="\n\nMap: "+event['map']

	msg+="\nPosition: " + location_to_string(event['location'])
	
	return msg



mod_names = { 'DeusEx': '', 'GMDXRandomizer': 'GMDX', 'RevRandomizer': 'Revision', 'HXRandomizer': 'HX', 'VMDRandomizer': 'VanillaMadder' }
flag_to_character_names = {
	'TerroristCommander_Dead': 'Terrorist Commander',
	'TiffanySavage_Dead': 'Tiffany Savage',
	'PaulDenton_Dead': 'Paul Denton',
	'JordanShea_Dead': 'Jordan Shea',
	'SandraRenton_Dead': 'Sandra Renton',
	'GilbertRenton_Dead': 'Gilbert Renton',
	'AnnaNavarre_Dead': 'Anna Navarre',
	'GuntherHermann_Dead': 'Gunther Hermann',
	'JoJoFine_Dead': 'JoJo Fine',
	'TobyAtanwe_Dead': 'Toby Atanwe',
	'Antoine_Dead': 'Antoine',
	'Chad_Dead': 'Chad',
	'hostage_Dead': 'Juveau',
	'hostage_female_Dead': 'Anna',
	'Hela_Dead': 'Hela',
	'Renault_Dead': 'Renault',
	'Labrat_Bum_Dead': 'Labrat Bum',
	'DXRNPCs1_Dead': 'The Merchant',
	'lemerchant_Dead': 'Le Merchant',
	'Harold_Dead': 'Harold',
	'Josh_Dead': 'Josh',
	'Billy_Dead': 'Billy',
	'MarketKid_Dead': 'Louis Pan',
	'aimee_Dead': 'Aimee',
	'WaltonSimons_Dead': 'Walton Simons',
	'JoeGreene_Dead': 'Joe Greene'
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
			return None

	# flag for character's death, we assume the player killed them, location is None or player's location?
	elif event['type']=='Flag' and event['flag'] in flag_to_character_names:
		event['victim'] = flag_to_character_names[event['flag']]
		event['killer'] = event['PlayerName']
		#immediate = event['immediate'] # we might need this, maybe to ignore the location?
		msg = gen_death_msg(False, event, event.get('location'))
	
	elif event["type"]=="BeatGame":
		msg = BeatGameMsg(event)
		if not msg:
			return None

	elif event['type']=='Trigger':
		msg = TriggerEventMsg(event)
		if not msg:
			return None

	elif event['type']=='Flag':
		msg = FlagEventMsg(event)
		if not msg:
			return None
	
	elif event['type']=='SavedPaul':
		msg = event['PlayerName']+' saved Paul\'s life during the raid!\n'
		if 'PaulHealth' in event:
			msg += 'Paul had ' + str(int(event['PaulHealth'])) + '% health remaining\n'
			
	elif event['type']=='ExtinguishFire':
		msg = ExtinguishFireMsg(event)
		if not msg:
			return None
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

