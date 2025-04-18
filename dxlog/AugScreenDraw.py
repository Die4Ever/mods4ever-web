from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import json
import os.path
from dxlog.base import *

BoxSize=(208,208)
InactiveAugColor=(255,255,30)
ActiveAugColor=(30,255,30)

CranialCoord=(286,179)
EyesCoord=(907,179)
ArmsCoord=(134,482)
SubDermalCoord=[(134,818),(134,1054)]
LegsCoord=(1046,1314)
TorsoCoord=[(1046,506),(1046,742),(1046,978)]
DefaultCoord=[(135,1390),(345,1390),(558,1390)]

SkillSpacing=25
CranialSkillLevel=(410,400)
EyeSkillLevel=(1030,400)
ArmSkillLevel=(255,705)
LegsSkillLevel=(1172,1535)
SubdermalSkillLevel=[(255,1040),(255,1275)]
TorsoSkillLevel=[(1172,728),(1172,965),(1172,1200)]
DefaultSkillLevel=[(256,1612),(470,1612),(685,1612)]

DEFAULT_FONT_NAME="CourierPrimeCode.ttf"
DEFAULT_FONT_SIZE = 28

class AugScreenDrawer:
    def getSkillPoint(self, base,level):
        return (base[0]+(SkillSpacing*level),base[1])

    def getAugImage(self,augName):
        if augName=="AugSkullGun":
            augName = "AugDatalink"
        elif augName=="AugTracking":
            augName = "AugTarget"
        imageLoc = self.ImageFolder+augName+".png"
        if not os.path.exists(imageLoc):
            return None

        im = Image.open(imageLoc)

        return im

    def getAugCoord(self,location,index):
        if location=="Cranial":
            return CranialCoord
        elif location=="Eyes":
            return EyesCoord
        elif location=="Arms":
            return ArmsCoord
        elif location=="Legs":
            return LegsCoord
        elif location=="Subdermal":
            return SubDermalCoord[index]
        elif location=="Torso":
            return TorsoCoord[index]
        elif location=="Default":
            return DefaultCoord[index]

        print("Didn't recognize location "+location)
        return (0,0)

    def getAugSkillCoord(self,location,index):
        if location=="Cranial":
            return CranialSkillLevel
        elif location=="Eyes":
            return EyeSkillLevel
        elif location=="Arms":
            return ArmSkillLevel
        elif location=="Legs":
            return LegsSkillLevel
        elif location=="Subdermal":
            return SubdermalSkillLevel[index]
        elif location=="Torso":
            return TorsoSkillLevel[index]
        elif location=="Default":
            return DefaultSkillLevel[index]

        print("Didn't recognize location "+location)
        return (0,0)

    #The aug images are white on black, with white being full opaque
    #The given color will tint the image to the specified color
    def makeAugImageTransparent(self,image,color):
        image = image.convert("RGBA")
        data = image.getdata()

        newData = []
        for pixel in data:
            newData.append((color[0],color[1],color[2],pixel[0]))
        image.putdata(newData)
        return image

    def setSkillLevel(self,location,skillLevel,index=0,color=(255,255,255,255)):
        for i in range(0,skillLevel):
            ImageDraw.floodfill(self.image,self.getSkillPoint(self.getAugSkillCoord(location,index),i),color)

    def drawAug(self,augName,location,skillLevel,index=0):
        if (index==-1):
            return
        
        augImage = self.getAugImage(augName)
        if (augImage != None):
            augImage = augImage.crop((0,0,52,52))
            resample = Image.Resampling.NEAREST
            augImage = augImage.resize(BoxSize, resample)
            augImage = self.makeAugImageTransparent(augImage,InactiveAugColor)
            coord = self.getAugCoord(location,index)
            self.image.paste(augImage,coord,augImage)
        else:
            #If we don't have the image, write the aug name for easy debug
            font = ImageFont.truetype(DEFAULT_FONT_NAME, DEFAULT_FONT_SIZE)
            draw = ImageDraw.Draw(self.image)
            coords = self.getAugCoord(location, index)
            coords = (coords[0] + 5, coords[1] + 90)
            draw.text(coords, self.getAugName(augName), font=font)
            
            
        self.setSkillLevel(location,skillLevel+1,index)

    def saveImage(self):
        self.image=self.image.convert('RGB')
        self.image.save("AugScreenTest.jpg")
        
    def getImageInMemory(self):
        b = BytesIO()
        self.image=self.image.convert('RGB')
        self.image.save(b,"JPEG")
        b.seek(0)  #This is apparently needed, otherwise twitter will reject it

        return b

    def handleAugJson(self,inputJson):
        for i in range(3,15):
            augId = "Aug-"+str(i)
            if augId in inputJson:
                self.augs[i]=inputJson[augId]
    def getLocationAndIndexFromHotkey(self,hotKey):
        #Deus Ex hotkeys map to different positions
        if hotKey==3:
            return ("Subdermal",0)
        elif hotKey==4:
            return ("Subdermal",1)
        elif hotKey==5:
            return ("Cranial",0)
        elif hotKey==6:
            return ("Arms",0)
        elif hotKey==7:
            return ("Legs",0)
        elif hotKey==8:
            return ("Eyes",0)
        elif hotKey==9:
            return ("Torso",0)
        elif hotKey==10:
            return ("Torso",1)
        elif hotKey==11:
            return ("Torso",2)
        elif hotKey==12:
            return ("Default",1) #Light
        elif hotKey==13:
            return ("Default",0) #IFF
        elif hotKey==14:
            return ("Default",2) #Datalink
        else:
            return ("Unknown",-1)

    def drawAllAugs(self):
        info("Aug list: "+str(self.augs))
        for hotKey in self.augs.keys():
            locIndex = self.getLocationAndIndexFromHotkey(hotKey)
            self.drawAug(self.augs[hotKey]["name"],locIndex[0],self.augs[hotKey]["level"],locIndex[1])

    def getAugName(self,className):
        augs=dict()
        augs["AugAqualung"]="Aqualung"
        augs["AugBallistic"]="Ballistic Protection"
        augs["AugCloak"]="Cloak"
        augs["AugCombat"]="Combat Strength"
        augs["AugDatalink"]="Infolink"
        augs["AugDefense"]="Aggressive Defense System"
        augs["AugDrone"]="Spy Drone"
        augs["AugEnviro"]="Environmental Resistance"
        augs["AugEMP"]="EMP Shield"
        augs["AugHealing"]="Regeneration"
        augs["AugHeartLung"]="Synthetic Heart"
        augs["AugIFF"]="IFF"
        augs["AugLight"]="Light"
        augs["AugMuscle"]="Microfibral Muscle"
        augs["AugPower"]="Power Recirculator"
        augs["AugRadarTrans"]="Radar Transparency"
        augs["AugShield"]="Energy Shield"
        augs["AugSpeed"]="Speed Enhancement"
        augs["AugStealth"]="Run Silent"
        augs["AugTarget"]="Targeting"
        augs["AugVision"]="Vision Enhancement"
        augs["AugNinja"]="Ninja"
        augs["AugSkullGun"]="Skull Gun"
        augs["AugTracking"]="Tracking"
        augs["AugInfraVision"]="Infravision"
        augs["AugMotionSensor"]="Motion Sensor"
        augs["AugVisionShort"]="Short-Range Vision Enhancement"
        augs["AugOnlySpeed"]="Running Enhancement"
        augs["AugJump"]="Jump Enhancement"

        if className not in augs:
            return profanity.censor(className) #Just in case
        else:
            return augs[className]

    def getAugScreenAltText(self):
        alt=""
        for hotkey in self.augs.keys():
            if(hotkey<=12):
                alt+="F"+str(hotkey)+" - "+self.getAugName(self.augs[hotkey]["name"])+" (Level "+str(self.augs[hotkey]["level"]+1)+")\n"
        return profanity.censor(alt)
        

    def __init__(self, jsonIn, imageDir="AugDrawImages/", isFemale=False):
        self.ImageFolder = imageDir
        if isFemale=="True":
            baseImage = "AugScreenFemale.png"
        else:
            baseImage = "AugScreenMale.png"
        self.image = Image.open(self.ImageFolder+baseImage)
        self.augs = {}
        self.handleAugJson(jsonIn)
        self.drawAllAugs()

