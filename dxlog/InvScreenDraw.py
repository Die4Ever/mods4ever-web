from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import json
import os.path
from dxlog.base import *
from typeguard import typechecked

SquareSize=53
BaseXOffset=20
BaseYOffset=29
ImageScale=2

InventoryLabelCoord=[35,28]
CreditsLabelCoord=[360,28]
CreditsAmountCoord=[470,28]

DEFAULT_FONT_NAME="CourierPrimeCode.ttf"

ERROR_FONT_SIZE = 12
DEFAULT_FONT_SIZE = 18
LABEL_FONT_SIZE = 24

COUNT_TEXT_OFFSET_X=6
COUNT_TEXT_OFFSET_Y=42

@typechecked
class InventoryScreenDrawer:

    def getInvImage(self,InvClass:str):
        imageLoc = self.IconsFolder+InvClass+".png"
        if not os.path.exists(imageLoc):
            return None

        im = Image.open(imageLoc)
        im = im.convert('RGBA')

        return self.scaleImage(im,ImageScale)


    def drawInventory(self,inv:dict):
        invClass: str = inv.get("class")
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
                inv: dict = inputJson[invId]
                self.inventory.append(inv)

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
        self.inventory: list[dict] = []
        self.credits=0

        self.handleInvJson(jsonIn)

        self.drawAllInventory()
        self.drawLabels()