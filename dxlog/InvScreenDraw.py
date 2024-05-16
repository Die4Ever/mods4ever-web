from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import json
import os.path

SquareSize=53
BaseXOffset=20
BaseYOffset=29
ImageScale=2

InventoryLabelCoord=[35,28]
CreditsLabelCoord=[360,28]
CreditsAmountCoord=[470,28]

InvTestString = """[{"type": "BeatGame", "ending": "2", "time": "206851", "SaveCount": "800", "deaths": "0", "maxrando": "0", "PlayerName": "Asstro", "map": "ENDGAME2", "mapname": "", "mission": "99", "TrueNorth": "0", "PlayerIsFemale": "False", "GameMode": "Normal Randomizer", "newgameplus_loops": "0", "loadout": "All Items Allowed", "NumberOfBingos": "12", "bingo-0-0": {"event": "paris_hostage_Dead", "desc": "Kill both the hostages in the catacombs", "progress": 2, "max": 2}, "bingo-0-1": {"event": "ClubEntryPaid", "desc": "Help Mercedes and Tessa", "progress": 1, "max": 1}, "bingo-0-2": {"event": "M10EnteredBakery", "desc": "Enter the bakery", "progress": 1, "max": 1}, "bingo-0-3": {"event": "TobyAtanwe_Dead", "desc": "Kill Toby Atanwe", "progress": 1, "max": 1}, "bingo-0-4": {"event": "TerroristCommander_Dead", "desc": "Kill the Terrorist Commander", "progress": 1, "max": 1}, "bingo-1-0": {"event": "Gray_ClassDead", "desc": "Kill 5 Grays", "progress": 10, "max": 5}, "bingo-1-1": {"event": "ActivateVandenbergBots", "desc": "Activate both of the bots at Vandenberg", "progress": 2, "max": 2}, "bingo-1-2": {"event": "KnowsAnnasKillphrase", "desc": "Learn both parts of Anna's Killphrase", "progress": 2, "max": 2}, "bingo-1-3": {"event": "MolePeopleSlaughtered", "desc": "Slaughter the Mole People", "progress": 1, "max": 1}, "bingo-1-4": {"event": "MoonBaseNews", "desc": "Read news about the Lunar Mining Complex", "progress": 3, "max": 1}, "bingo-2-0": {"event": "JocksToilet", "desc": "Use Jock's toilet", "progress": 1, "max": 1}, "bingo-2-1": {"event": "M02BillyDone", "desc": "Give Billy some food", "progress": 1, "max": 1}, "bingo-2-2": {"event": "Free Space", "desc": "Free Space", "progress": 1, "max": 1}, "bingo-2-3": {"event": "MJ12Commando_ClassDead", "desc": "Kill 10 MJ12 Commandos", "progress": 33, "max": 10}, "bingo-2-4": {"event": "lemerchant_Dead", "desc": "Kill Le Merchant", "progress": 1, "max": 1}, "bingo-3-0": {"event": "JoeGreene_Dead", "desc": "Kill Joe Greene", "progress": 1, "max": 1}, "bingo-3-1": {"event": "MilitaryBot_ClassDead", "desc": "Destroy 5 Military Bots", "progress": 5, "max": 5}, "bingo-3-2": {"event": "SpinShipsWheel", "desc": "Spin 3 ships wheels", "progress": 4, "max": 3}, "bingo-3-3": {"event": "AnnaNavarre_Dead", "desc": "Kill Anna Navarre", "progress": 1, "max": 1}, "bingo-3-4": {"event": "BoatEngineRoom", "desc": "Access the engine room on the boat in the Hong Kong canals", "progress": 1, "max": 1}, "bingo-4-0": {"event": "HumanStompDeath", "desc": "Stomp 3 humans to death", "progress": 4, "max": 3}, "bingo-4-1": {"event": "ManWhoWasThursday", "desc": "Read 4 parts of The Man Who Was Thursday", "progress": 6, "max": 4}, "bingo-4-2": {"event": "HotelHostagesSaved", "desc": "Save all hostages in the hotel", "progress": 1, "max": 1}, "bingo-4-3": {"event": "Chad_Dead", "desc": "Kill Chad", "progress": 1, "max": 1}, "bingo-4-4": {"event": "TongsHotTub", "desc": "Take a dip in Tracer Tong's hot tub", "progress": 1, "max": 1}, "Aug-7": {"name": "AugSpeed", "level": 3}, "Aug-3": {"name": "AugCloak", "level": 3}, "Aug-4": {"name": "AugRadarTrans", "level": 3}, "Aug-9": {"name": "AugShield", "level": 3}, "Aug-10": {"name": "AugHealing", "level": 3}, "Aug-13": {"name": "AugIFF", "level": 0}, "Aug-12": {"name": "AugLight", "level": 0}, "Aug-6": {"name": "AugMuscle", "level": 3}, "Aug-8": {"name": "AugVision", "level": 3}, "Aug-5": {"name": "AugDrone", "level": 3}, "Aug-14": {"name": "AugDatalink", "level": 0}, "Aug-11": {"name": "AugHeartLung", "level": 0},"Inv-0":{"class":"AugmentationUpgradeCannister","x":4,"y":4,"count":1,"name":"Augmentation Upgrade Canister"},"Inv-1":{"class":"WeaponStealthPistol","x":4,"y":3,"count":0,"name":"Stealth Pistol"},"Inv-2":{"class":"Multitool","x":4,"y":2,"count":1,"name":"Multitool"},"Inv-3":{"class":"WeaponFlamethrower","x":0,"y":3,"count":0,"name":"Flamethrower"},"Inv-4":{"class":"BallisticArmor","x":3,"y":2,"count":1,"name":"Ballistic Armor"},"Inv-5":{"class":"WeaponPepperGun","x":4,"y":1,"count":0,"name":"Pepper Gun"},"Inv-6":{"class":"Lockpick","x":3,"y":1,"count":1,"name":"Lockpick"},"Inv-7":{"class":"WeaponSawedOffShotgun","x":0,"y":2,"count":0,"name":"Sawed-off Shotgun"},"Inv-8":{"class":"FireExtinguisher","x":2,"y":1,"count":3,"name":"Fire Extinguisher"},"Inv-9":{"class":"WeaponLAM","x":4,"y":0,"count":2,"name":"Lightweight Attack Munitions (LAM)"},"Inv-10":{"class":"BallisticArmor","x":3,"y":0,"count":1,"name":"Ballistic Armor"},"Inv-11":{"class":"WeaponBaton","x":2,"y":0,"count":0,"name":"Baton"},"Inv-12":{"class":"WeaponAssaultShotgun","x":0,"y":0,"count":0,"name":"Assault Shotgun"},"credits":1540}]"""
DEFAULT_FONT_NAME="CourierPrimeCode.ttf"

ERROR_FONT_SIZE = 12
DEFAULT_FONT_SIZE = 18
LABEL_FONT_SIZE = 24

COUNT_TEXT_OFFSET_X=6
COUNT_TEXT_OFFSET_Y=42

class InventoryScreenDrawer:

    def getInvImage(self,InvClass):
        imageLoc = self.IconsFolder+InvClass+".png"
        if not os.path.exists(imageLoc):
            return None

        im = Image.open(imageLoc)
        im = im.convert('RGBA')

        return self.scaleImage(im,ImageScale)


    def drawInventory(self,inv):
        invClass = inv.get("class")
        x = inv.get("x",-1)
        y = inv.get("y",-1)
        count = inv.get("count",0)
        
        if (x<0 or y<0 or invClass==""):
            return

        #font = ImageFont.load_default()
        coord=self.getInventoryCoord(x,y)

        invImage=self.getInvImage(invClass)

        if(invImage!=None):
            self.image.paste(invImage,coord,invImage)
        else:
            font = ImageFont.truetype(DEFAULT_FONT_NAME, ERROR_FONT_SIZE)
            draw = ImageDraw.Draw(self.image)
            draw.text(coord,invClass,font=font)

        if (count>1):
            font = ImageFont.truetype(DEFAULT_FONT_NAME, DEFAULT_FONT_SIZE)
            draw = ImageDraw.Draw(self.image)
            coord=(coord[0]+(COUNT_TEXT_OFFSET_X*ImageScale),coord[1]+(COUNT_TEXT_OFFSET_Y * ImageScale))
            draw.text(coord,"Count:"+str(count),font=font)

    def getInventoryCoord(self,x,y):
        xCoord=BaseXOffset
        yCoord=BaseYOffset

        xCoord=xCoord+(x*SquareSize)
        yCoord=yCoord+(y*SquareSize)

        return (xCoord * ImageScale ,yCoord * ImageScale)
        

    def saveImage(self):
        self.image.save("InvScreenTest.png")
        
    def getImageInMemory(self):
        b = BytesIO()
        self.image.save(b,"PNG")
        b.seek(0)  #This is apparently needed, otherwise twitter will reject it

        return b


    def handleInvJson(self,inputJson):
        for i in range(0,50): #only 30 slots in inventory right now, but just to be safe
            invId = "Inv-"+str(i)
            if invId in inputJson:
                self.inventory.append(inputJson[invId])

        self.credits=inputJson.get("credits",0)


    def drawAllInventory(self):
        for inv in self.inventory:
            self.drawInventory(inv)


    def drawLabels(self):
        font = ImageFont.truetype(DEFAULT_FONT_NAME, LABEL_FONT_SIZE)
        draw = ImageDraw.Draw(self.image)
        draw.text(InventoryLabelCoord,"Inventory",font=font)
        draw.text(CreditsLabelCoord,"Credits",font=font)
        draw.text(CreditsAmountCoord,str(self.credits),font=font)


    def scaleImage(self,image,scale):
        image = image.resize((image.size[0]*scale,image.size[1]*scale),Image.Resampling.NEAREST)
        return image

    def getInvScreenAltText(self):
        alt="An inventory screen containing:\n"
        for inv in self.inventory:
            alt+=inv.get("name","")
            if (inv.get("count",0)>1):
                alt+=" (Count: "+str(inv.get("count"))+")"
            alt+="\n"
        return alt

    def __init__(self,jsonIn,imageDir="""InventoryImages/""",iconDir="""InventoryImages/Icons/"""):
        self.ImageFolder = imageDir
        self.IconsFolder = iconDir
        self.image = Image.open(self.ImageFolder+"InventoryScreen.png")
        self.image.convert("RGBA")
        self.image = self.scaleImage(self.image,ImageScale)
        self.inventory = []
        self.credits=0

        self.handleInvJson(jsonIn)

        self.drawAllInventory()
        self.drawLabels()

        #print(self.getInvScreenAltText())

        #self.saveImage() #Once actually merged, don't always save the image
        
#demoJson = json.loads(InvTestString)
#InvDraw = InventoryScreenDrawer(demoJson[0])
