from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import json
import os.path
from dxlog.base import *

BoxSize=(208,208)
InactiveAugColor=(255,255,30)
ActiveAugColor=(30,255,30)

AugLevelColor=(255,255,255,255)
GMDXAugLevelColor=(255,0,0,255)
MaxAugLevelColor=(113,113,113,255)
GMDXMaxAugLevelColor=(32,32,32,255)

CranialCoord=(286,179)
CranialCoordGMDX=(394,166)
EyesCoord=(907,179)
ArmsCoord=(134,482)
ArmsCoordGMDX=[(134,198),(134,434)]
SubDermalCoord=[(134,818),(134,1054)]
LegsCoord=(1046,1314)
TorsoCoord=[(1046,506),(1046,742),(1046,978)]
DefaultCoord=[(135,1390),(345,1390),(558,1390)]

SkillSpacing=25
CranialSkillLevel=(410,400)
CranialSkillLevelGMDX=(520,390)
EyeSkillLevel=(1030,400)
ArmSkillLevel=(255,705)
ArmSkillLevelGMDX=[(260,420),(260,655)]
LegsSkillLevel=(1172,1535)
SubdermalSkillLevel=[(255,1040),(255,1275)]
TorsoSkillLevel=[(1172,728),(1172,965),(1172,1200)]
DefaultSkillLevel=[(256,1612),(470,1612),(685,1612)]

DEFAULT_FONT_NAME="CourierPrimeCode.ttf"
DEFAULT_FONT_SIZE = 28

class AugScreenDrawer:
    def getSkillPoint(self, base,level):
        return (base[0]+(SkillSpacing*level),base[1])
    
    def remapAugImage(self,augName):

        #Shifter/Biomod
        if augName=="AugSkullGun":
            augName = "AugDatalink"
        elif augName=="AugTracking":
            augName = "AugTarget"
        
        #GMDX
        elif augName=="AugBallisticPassive":
            augName = "AugBallistic"
        elif augName =="AugIcarus":
            augName = "AugEMP"
        elif augName =="AugCombatStrength": #note original aug is AugCombat
            augName = "AugCombatStrengthGMDX"

        #VMD
        #These mech augs are theoretically not for player use right now
        elif augName=="AugMechCloak":
            augName = "AugCloak"
        elif augName=="AugMechCombat":
            augName = "AugCombat"
        elif augName=="AugMechDermal":
            augName = "AugBallistic"
        elif augName=="AugMechEMP":
            augName = "AugEMP"
        elif augName=="AugMechEnergy":
            augName = "AugBallistic" #???
        elif augName=="AugMechEnviro":
            augName = "AugEnviro"
        elif augName=="AugMechMuscle":
            augName = "AugMuscle"
        elif augName=="AugMechSpeed":
            augName = "AugSpeed"
        elif augName=="AugMechStealth":
            augName = "AugStealth"
        elif augName=="AugMechTarget":
            augName = "AugTarget"
        elif augName=="AugMechVision":
            augName = "AugVision"

        return augName

    def getAugImage(self,augName):
        augName = self.remapAugImage(augName);
        imageLoc = self.ImageFolder+augName+".png"
        if not os.path.exists(imageLoc):
            return None

        im = Image.open(imageLoc)

        return im

    def getAugCoord(self,location,index):
        gmdx = ("gmdx" in self.mod.lower())
        if location=="Cranial":
            if (not gmdx):
                return CranialCoord
            else:
                return CranialCoordGMDX
        elif location=="Eyes":
            return EyesCoord
        elif location=="Arms":
            if (not gmdx):
                return ArmsCoord
            else:
                return ArmsCoordGMDX[index]
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
        gmdx = ("gmdx" in self.mod.lower())

        if location=="Cranial":
            if (not gmdx):
                return CranialSkillLevel
            else:
                return CranialSkillLevelGMDX
        elif location=="Eyes":
            return EyeSkillLevel
        elif location=="Arms":
            if (not gmdx):
                return ArmSkillLevel
            else:
                return ArmSkillLevelGMDX[index]
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
        data = image.get_flattened_data()

        newData = []
        for pixel in data:
            newData.append((color[0],color[1],color[2],pixel[0]))
        image.putdata(newData)
        return image

    def setSkillLevel(self,location,skillLevel,skillMax,index=0):
        #print("Setting aug in "+location+" with level "+str(skillLevel)+" and max "+str(skillMax))
        augColor = None
        maxColor = None
        if ("gmdx" in self.mod.lower()):
            augColor = GMDXAugLevelColor
            maxColor = GMDXMaxAugLevelColor
        else:
            augColor = AugLevelColor
            maxColor = MaxAugLevelColor
        
        for i in range(0,skillLevel):
            ImageDraw.floodfill(self.image,self.getSkillPoint(self.getAugSkillCoord(location,index),i),augColor)

        if (skillMax >= 4):
            return

        for i in range(skillMax,4):
            ImageDraw.floodfill(self.image,self.getSkillPoint(self.getAugSkillCoord(location,index),i),maxColor)

    def drawAugLocOverlay(self,location):
        if (location=="Default"):
            return
        
        genderDir="Male/"
        if (self.isFemale):
            genderDir="Female/"

        overlayImageLoc = self.ImageFolder+"LocOverlay/"+genderDir+location+".png"

        try:
            im = Image.open(overlayImageLoc)
        except:
            return
        
        loc=(0,0)
        if location=="Cranial":
            loc=(626,202)
        elif location=="Eyes":
            loc=(702,274)
        elif location=="Arms":
            loc=(478,462)
        elif location=="Legs":
            loc=(718,910)
        elif location=="Subdermal":
            loc=(394,662)
        elif location=="Torso":
            loc=(686,454)
        else:
            print("Didn't recognize location "+location)
            return

        self.image.paste(im,loc,im)

    def drawAug(self,augName,location,skillLevel,skillMax,index=0):
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
            
            
        self.setSkillLevel(location,skillLevel+1,skillMax+1,index)

        self.drawAugLocOverlay(location)

    def saveImage(self):
        self.image=self.image.convert('RGB')
        self.image.save("AugScreenTest.jpg")
        
    def getImageInMemory(self):
        b = BytesIO()
        self.image=self.image.convert('RGB')
        self.image.save(b,"JPEG")
        b.seek(0)  #This is apparently needed, otherwise twitter will reject it

        return b
    
    def InitAugSlotTable(self):
        slots = dict()
        for i in range(0,6+1):
            slots[i]=dict()
            for j in range(0,3):
                slots[i][j]=None

        return slots

    def handleAugJson(self,inputJson):
        augSlotPopulate = self.InitAugSlotTable()
        augNum = 0


        for i in range(3,15):
            augId = "Aug-"+str(i)
            if augId in inputJson:
                self.augs[augNum]=inputJson[augId]
                if "max" not in self.augs[augNum]:
                    self.augs[augNum]["max"] = self.DefaultAugMax(self.augs[augNum]["name"])
                if "key" not in self.augs[augNum]:
                    #If hotkey isn't in the json, we're probably sending it as the index
                    self.augs[augNum]["key"]=i
                if "loc" not in self.augs[augNum]:
                    self.augs[augNum]["loc"]=self.getLocationFromHotkey(self.augs[augNum]["key"])

                self.augs[augNum]["slot"]=self.getSlotFromHotkey(self.augs[augNum]["key"])

                loc = self.augs[augNum]["loc"]
                slot = self.augs[augNum]["slot"]
                name = self.augs[augNum]["name"]

                if (loc >= 0 and slot >= 0):
                    augSlotPopulate[loc][slot] = name

                augNum = augNum+1

        for i in range(0,10):
            augId = "PAug-"+str(i)
            if augId in inputJson:
                self.augs[augNum]=inputJson[augId]
                if "max" not in self.augs[augNum]:
                    self.augs[augNum]["max"] = self.DefaultAugMax(self.augs[augNum]["name"])
                if "loc" not in self.augs[augNum]:
                    self.augs[augNum]["loc"]=999

                self.augs[augNum]["key"]=-1
                self.augs[augNum]["slot"]=self.findAvailableAugSlot(augSlotPopulate,self.augs[augNum]["loc"])
                augSlotPopulate[self.augs[augNum]["loc"]][self.augs[augNum]["slot"]]=self.augs[augNum]["name"]

                augNum = augNum+1


    #Aug max levels to use if not present in the message (ie. versions before we started including it)
    def DefaultAugMax(self,augName):
        #Remember that this is from 0-3, not 1-4
        if (augName=="AugIFF"):
            return 0
        elif (augName=="AugDatalink"):
            return 0
        elif (augName=="AugLight"):
            return 1

        return 3

    def findAvailableAugSlot(self,popList,loc):
        for i in range(0,3):
            if popList[loc][i]==None:
                return i
        return -1

    def getLocationAndIndexFromHotkey(self,hotKey):
        #Deus Ex hotkeys map to different positions
        loc = self.getLocationName(self.GetLocationFromHotkey(hotKey))
        idx = self.getSlotFromHotkey(hotKey)

        return (loc,idx)
    
    def getSlotFromHotkey(self,hotKey):
        idx=0
        if hotKey==3:
            idx=0
        elif hotKey==4:
            idx=1
        elif hotKey==5:
            idx=0
        elif hotKey==6:
            idx=0
        elif hotKey==7:
            idx=0
        elif hotKey==8:
            idx=0
        elif hotKey==9:
            idx=0
        elif hotKey==10:
            idx=1
        elif hotKey==11:
            idx=2
        elif hotKey==12:
            idx=1 #Light
        elif hotKey==13:
            idx=0 #IFF
        elif hotKey==14:
            idx=2 #Datalink
        else:
            idx=-1
        
        return idx

        
    def getLocationFromHotkey(self,hotKey):
        if hotKey==3:
            return 5
        elif hotKey==4:
            return 5
        elif hotKey==5:
            return 0
        elif hotKey==6:
            return 3
        elif hotKey==7:
            return 4
        elif hotKey==8:
            return 1
        elif hotKey==9:
            return 2
        elif hotKey==10:
            return 2
        elif hotKey==11:
            return 2
        elif hotKey==12:
            return 6 #Light
        elif hotKey==13:
            return 6 #IFF
        elif hotKey==14:
            return 6 #Datalink
        else:
            return -1 #Unknown

        
    def getLocationName(self,loc):
        locName = ""
        idx = 0

        if (loc==0):
            locName = "Cranial"
        elif (loc==1):
            locName = "Eyes"
        elif (loc==2):
            locName = "Torso"
        elif (loc==3):
            locName = "Arms"
        elif (loc==4):
            locName = "Legs"
        elif (loc==5):
            locName = "Subdermal"
        elif (loc==6):
            locName = "Default"
        else:
            locName = "Unknown"

        return locName


    def drawAllAugs(self):
        for idx in self.augs.keys():
            loc = self.augs[idx]["loc"]
            locName = self.getLocationName(loc)
            slot = self.augs[idx]["slot"]
            
            self.drawAug(self.augs[idx]["name"],locName,self.augs[idx]["level"],self.augs[idx]["max"],slot)

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

        #GMDX
        augs["AugBallisticPassive"]="BPN-021"
        augs["AugIcarus"]="EMSP"
        augs["AugCombatStrength"]="Combat Strength (Active)"
        augs["AugEnergyTransfer"]="Energy Transference"

        #VMD
        augs["AugMechCloak"]="Glass-Shield Cloaking System"
        augs["AugMechCombat"]="Cybernetic Arm Prosthesis"
        augs["AugMechDermal"]="Dermal Armor"
        augs["AugMechEMP"]="EMP Shielding"
        augs["AugMechEnergy"]="Dermal Tempering"
        augs["AugMechEnviro"]="Implanted Rebreather"
        augs["AugMechMuscle"]="Heavy Cybernetic Arms"
        augs["AugMechSpeed"]="Sprint Enhancement"
        augs["AugMechStealth"]="Stealth Enhancement"
        augs["AugMechTarget"]="Aim Stabilizer"
        augs["AugMechVision"]="Smart Vision"

        if className not in augs:
            return profanity.censor(className) #Just in case
        else:
            return augs[className]

    def getAugScreenAltText(self):
        alt=""
        for idx in self.augs.keys():
            hotkey = self.augs[idx]["key"]
            if (hotkey > 0 and hotkey<=12):
                alt+="F"+str(hotkey)+" - "+self.getAugName(self.augs[idx]["name"])+" (Level "+str(self.augs[idx]["level"]+1)+")\n"
            else:
                alt+="Passive: " + self.getAugName(self.augs[idx]["name"])+" (Level "+str(self.augs[idx]["level"]+1)+")\n"

        #info("Aug Alt Text: "+alt)
        return profanity.censor(alt)
        

    def findBaseImage(self):
        if ("gmdx" in self.mod.lower()):
            if self.isFemale: #AE only
                baseImage = "AugScreenMaleGMDX.png" #TODO change to female GMDX image
            else:
                baseImage = "AugScreenMaleGMDX.png"
        else:
            if self.isFemale:
                baseImage = "AugScreenFemale.png"
            else:
                baseImage = "AugScreenMale.png"

        return baseImage

    def __init__(self, jsonIn, mod="", imageDir="AugDrawImages/", isFemale=False):
        self.ImageFolder = imageDir

        self.isFemale= (isFemale=="True")

        self.mod = mod

        baseImage = self.findBaseImage()

        self.image = Image.open(self.ImageFolder+baseImage)
        self.augs = {}
        self.handleAugJson(jsonIn)
        self.drawAllAugs()

