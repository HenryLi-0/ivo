'''This file contains classes all about the visual objects the user sees'''

import numpy, random, math
from subsystems.render import placeOver
from subsystems.fancy import *
from subsystems.point import *
from settings import *

'''Hitboxes'''

class CircularPositionalBox:
    '''Just remembers where the object is supposed to be on screen, given the mouse position and updates when the mouse is in a specific ciruclar range'''
    def __init__(self, r:int = 10, ix = 0, iy = 0):
        '''Circular detection box will be centered!'''
        self.r, self.ix, self.iy = r, ix, iy
    def process(self, interact, rmx, rmy):
        '''Should be called whenever the position wants to question its position'''
        if interact: self.ix, self.iy = rmx, rmy
    def getInteract(self, rmx, rmy): 
        '''Returns whether or not the mouse is in range of interaction'''
        return math.sqrt((rmx-self.ix)**2 + (rmy-self.iy)**2) <= self.r
    def getPosition(self): return (self.ix, self.iy)
    def getX(self): return self.ix
    def getY(self): return self.iy
    def getR(self): return self.r
    def setPosition(self, position: tuple|list): self.ix, self.iy = position
    def setX(self, nx): self.ix = nx
    def setY(self, ny): self.iy = ny
    def setR(self, nr): self.r = nr

class RectangularPositionalBox:
    '''Just remembers where the object is supposed to be on screen, given the mouse position and updates when the mouse is in a specific bounding box'''
    def __init__(self, bbox:tuple|list = (10,10), ix = 0, iy = 0):
        '''Bounding box will NOT be centered!'''
        self.bbox, self.ix, self.iy = bbox, ix, iy
    def process(self, interact, rmx, rmy):
        '''Should be called whenever the position wants to question its position'''
        if interact: self.ix, self.iy = rmx, rmy
    def getInteract(self, rmx, rmy):
        '''Returns whether or not the mouse is in the bounding box of interaction'''
        return (self.ix < rmx) and (rmx < (self.ix+self.bbox[0])) and (self.iy < rmy) and (rmy < (self.iy+self.bbox[1]))
    def getPosition(self): return (self.ix, self.iy)
    def getX(self): return self.ix
    def getY(self): return self.iy
    def getBBOX(self): return self.bbox
    def setPosition(self, position: tuple|list): self.ix, self.iy = position
    def setX(self, nx): self.ix = nx
    def setY(self, ny): self.iy = ny
    def setBBOX(self, nbbox): self.bbox = nbbox

class FixedRegionPositionalBox:
    '''Just remembers where the object is supposed to be on screen, given the mouse position and updates when the mouse is in a specific region. Not movable by interaction.'''
    def __init__(self, pointA:tuple|list = (0,0), pointB:tuple|list = (10,10)):
        '''Point A and Point B are two opposite corners of a region!'''
        self.pointA = (min(pointA[0], pointB[0]), min(pointA[1], pointB[1]))
        self.pointB = (max(pointA[0], pointB[0]), max(pointA[1], pointB[1]))
    def process(self, interact, rmx, rmy):
        '''Should be called whenever the position wants to question its position'''
        pass
    def getInteract(self, rmx, rmy):
        '''Returns whether or not the mouse is in the region of interaction'''
        return (self.pointA[0] < rmx) and (rmx < self.pointB[0]) and (self.pointA[1] < rmy) and (rmy < self.pointB[1])
    def getPosition(self): return self.pointA
    def getX(self): return self.pointA[0]
    def getY(self): return self.pointA[1]
    def getRegion(self): return (self.pointA, self.pointB)
    def setPosition(self, position: tuple|list): 
        self.pointB = subtractP(self.pointB, subtractP(self.pointA, position))
        self.pointA = position
    def setRegion(self, pointA, pointB):
        self.pointA = (min(pointA[0], pointB[0]), min(pointA[1], pointB[1]))
        self.pointB = (max(pointA[0], pointB[0]), max(pointA[1], pointB[1]))

'''Visual Objects'''

from settings import ORB_IDLE_ARRAY, ORB_SELECTED_ARRAY

class OrbVisualObject:
    '''A movable point.'''
    def __init__(self, name, pos:tuple|list = (random.randrange(0,903), random.randrange(0,507))):
        self.type = "orb"
        self.name = name
        self.positionO = CircularPositionalBox(50)
        self.positionO.setPosition(pos)
    def tick(self, img, active):
        placeOver(img, ORB_SELECTED_ARRAY if active else ORB_IDLE_ARRAY, self.positionO.getPosition(), True)
        placeOver(img, displayText(self.name, "s"), self.positionO.getPosition(), True)
    def updatePos(self, rmx, rmy):
        self.positionO.setPosition((rmx, rmy))
    def keepInFrame(self, minX, minY, maxX, maxY):
        pos = self.positionO.getPosition()
        if pos[0] < minX or maxX < pos[0] or pos[1] < minY or maxY < pos[1]:
            self.positionO.setPosition((max(minX,min(pos[0],maxX)), max(minY,min(pos[1],maxY))))
    def getInteractable(self, rmx, rmy):
        return self.positionO.getInteract(rmx, rmy)

class ButtonVisualObject:
    '''A button.'''
    def __init__(self, name, pos:tuple|list, img:numpy.ndarray, img2:numpy.ndarray):
        self.type = "button"
        self.name = name
        self.img = img
        self.img2 = img2
        self.positionO = RectangularPositionalBox((img.shape[1],img.shape[0]), pos[0], pos[1])
    def tick(self, img, active):
        placeOver(img, self.img2 if active else self.img, self.positionO.getPosition(), False)
    def updatePos(self, rmx, rmy):
        pass
    def keepInFrame(self, minX, minY, maxX, maxY):
        pos = self.positionO.getPosition()
        if pos[0] < minX or maxX < pos[0] or pos[1] < minY or maxY < pos[1]:
            self.positionO.setPosition((max(minX,min(pos[0],maxX)), max(minY,min(pos[1],maxY))))
    def getInteractable(self,rmx,rmy):
        return self.positionO.getInteract(rmx, rmy)

class EditableTextBoxVisualObject:
    '''An editable text box.'''
    def __init__(self, name, pos:tuple|list, startTxt= "", intOnly = False):
        self.type = "textbox"
        self.name = name
        self.txt = str(startTxt)
        self.txtImg = displayText(self.txt, "m")
        self.intOnly = intOnly
        self.positionO = RectangularPositionalBox((max(self.txtImg.shape[1],10),max(self.txtImg.shape[0],23)), pos[0], pos[1])
        self.underlineIdle = generateColorBox((self.positionO.getBBOX()[0],3), FRAME_COLOR_RGBA)
        self.underlineActive = generateColorBox((self.positionO.getBBOX()[0],3), SELECTED_COLOR_RGBA)
    def tick(self, img, active):
        temp = generateColorBox(addP(self.positionO.getBBOX(), (0,3)), FRAME_COLOR_RGBA if active else BACKGROUND_COLOR_RGBA)
        placeOver(temp, self.underlineActive if active else self.underlineIdle, (0, self.positionO.getBBOX()[1]))
        placeOver(img, temp, self.positionO.getPosition())
        placeOver(img, self.txtImg, self.positionO.getPosition(), False)
    def updateText(self, txt):
        if self.txt!=str(txt):
            self.txt = str(txt)
            if self.intOnly:
                if txt == "" or len(str(txt)) == 0:
                    self.txt = "0"
                else:
                    temp = list(str(txt))
                    for item in temp:
                        if item not in "0123456789":
                            while item in temp: temp.remove(item)
                        self.txt = "".join(temp)
            self.txtImg = displayText(self.txt, "m")
            self.positionO.setBBOX((max(self.txtImg.shape[1]+3,10),max(self.txtImg.shape[0],23)))
            self.underlineIdle = generateColorBox((self.positionO.getBBOX()[0],3), FRAME_COLOR_RGBA)
            self.underlineActive = generateColorBox((self.positionO.getBBOX()[0],3), SELECTED_COLOR_RGBA)
    def updatePos(self, rmx, rmy):
        pass
    def keepInFrame(self, minX, minY, maxX, maxY):
        pos = self.positionO.getPosition()
        if pos[0] < minX or maxX < pos[0] or pos[1] < minY or maxY < pos[1]:
            self.positionO.setPosition((max(minX,min(pos[0],maxX)), max(minY,min(pos[1],maxY))))
    def getInteractable(self,rmx,rmy):
        return self.positionO.getInteract(rmx, rmy)
    
class DummyVisualObject:
    '''I sit around doing nothing and can store data. A little better that one group member in randomly assigned class projects. That person didn't deserve that 100, did they now? (joke)'''
    def __init__(self, name, pos:tuple|list, data = None):
        self.type = "dummy"
        self.name = name
        self.positionO = RectangularPositionalBox((0,0), pos[0], pos[1])
        self.data = data
    def tick(self, c, active):
        pass
    def updatePos(self, rmx, rmy):
        pass
    def keepInFrame(self, maxX, maxY):
        pass
    def getInteractable(self,rmx,rmy):
        return False

class IconVisualObject:
    '''An icon, basically a fancy button.'''
    # generateIcon(img, active = False, size = (29,29), color = "")
    def __init__(self, name, pos:tuple|list, icon:numpy.ndarray, size:tuple|list = (29,29)):
        self.type = "icon"
        self.name = name
        self.img = generateIcon(icon, False, size)
        self.img2 = generateIcon(icon, True, size)
        self.positionO = RectangularPositionalBox((self.img.shape[1],self.img.shape[0]), pos[0], pos[1])
    def tick(self, img, active):
        placeOver(img, self.img2 if active else self.img, self.positionO.getPosition(), False)
        if active: placeOver(img, displayText(self.name, "s", (0,0,0,200)), self.positionO.getPosition(), False)
    def updatePos(self, rmx, rmy):
        pass
    def keepInFrame(self, minX, minY, maxX, maxY):
        pos = self.positionO.getPosition()
        if pos[0] < minX or maxX < pos[0] or pos[1] < minY or maxY < pos[1]:
            self.positionO.setPosition((max(minX,min(pos[0],maxX)), max(minY,min(pos[1],maxY))))
    def getInteractable(self,rmx,rmy):
        return self.positionO.getInteract(rmx, rmy)
    
class ToggleVisualObject:
    '''A toggle, basically a fancy button/icon, but this time with two faces, on and off that switch on rising detection of clicks!'''
    # generateIcon(img, active = False, size = (29,29), color = "")
    def __init__(self, name, pos:tuple|list, iconOn:numpy.ndarray, iconOff:numpy.ndarray, size:tuple|list = (29,29), runOn = lambda: 0, runOff = lambda: 0):
        self.type = "icon"
        self.name = name
        self.img = generateIcon(iconOn, False, size)
        self.img2 = generateIcon(iconOff, False, size)
        self.positionO = RectangularPositionalBox((self.img.shape[1],self.img.shape[0]), pos[0], pos[1])
        self.active = 0
        self.state = False
        self.runOn = runOn
        self.runOff = runOff
    def tick(self, img, active):
        if active:
            self.active +=1
        else:
            self.active = 0
        if self.active == 1:
            self.state = not(self.state)
            if self.state == True: self.runOn()
            if self.state == False: self.runOff()
        placeOver(img, self.img2 if self.state else self.img, self.positionO.getPosition(), False)
        if active: placeOver(img, displayText(self.name, "s", (0,0,0,200)), self.positionO.getPosition(), False)
    def setToggle(self, runOn, runOff):
        self.runOn = runOn
        self.runOff = runOff
    def updatePos(self, rmx, rmy):
        pass
    def keepInFrame(self, minX, minY, maxX, maxY):
        pos = self.positionO.getPosition()
        if pos[0] < minX or maxX < pos[0] or pos[1] < minY or maxY < pos[1]:
            self.positionO.setPosition((max(minX,min(pos[0],maxX)), max(minY,min(pos[1],maxY))))
    def getInteractable(self,rmx,rmy):
        return self.positionO.getInteract(rmx, rmy)

class HorizontalSliderVisualObject:
    '''A slider!!! No way!!! (horizontal)'''
    def __init__(self, name, pos:tuple|list=(random.randrange(0,20), random.randrange(0,20)), length = random.randrange(50,100), sliderRange = [1,100]):
        self.type = "slider"
        self.name = name
        self.originalPos = pos
        self.length = length
        self.positionO = CircularPositionalBox(15)
        self.positionO.setPosition(addP(pos, (10,10)))
        self.displayScalar = sliderRange[1]-sliderRange[0]
        self.sliderRange = sliderRange
        self.bar = generateColorBox((length, 20), (0,0,0,0))
        placeOver(self.bar, generateColorBox((length, 2), hexColorToRGBA(FRAME_COLOR)), (0,9))
        placeOver(self.bar, generateColorBox((3, 20), hexColorToRGBA(FRAME_COLOR)), (0,0))
        placeOver(self.bar, generateColorBox((3, 20), hexColorToRGBA(FRAME_COLOR)), (length-3,0))
        self.updatePos(-9999999, 0)
    def tick(self, img, active):
        placeOver(img, self.bar, self.originalPos)
        placeOver(img, POINT_SELECTED_ARRAY if active else POINT_IDLE_ARRAY, self.positionO.getPosition(), True)
        if active: 
            placeOver(img, displayText(str(round((self.positionO.getX()-self.originalPos[0])/self.length*self.displayScalar+self.sliderRange[0])), "s", (0,0,0,150), (255,255,255,255)), addP(self.positionO.getPosition(), (0,25)), True)
    def getData(self):
        return round((self.positionO.getX()-self.originalPos[0])/self.length*self.displayScalar+self.sliderRange[0])
    def setData(self, extent):
        self.updatePos(self.originalPos[0] + (extent-self.sliderRange[0])/self.displayScalar*self.length, 0)
    def updatePos(self, rmx, rmy):
        self.positionO.setX(max(self.originalPos[0], min(rmx, self.originalPos[0] + self.length)))
    def keepInFrame(self, minX, minY, maxX, maxY):
        pos = self.positionO.getPosition()
        if pos[0] < minX or maxX < pos[0] or pos[1] < minY or maxY < pos[1]:
            self.positionO.setPosition((round(max(minX,min(pos[0],maxX))), round(max(minY,min(pos[1],maxY)))))
    def getInteractable(self, rmx, rmy):
        return self.positionO.getInteract(rmx, rmy)
    
class VerticalSliderVisualObject:
    '''A slider!!! No way!!! (vertical)'''
    def __init__(self, name, pos:tuple|list=(random.randrange(0,20), random.randrange(0,20)), length = random.randrange(50,100), sliderRange = [1,100]):
        self.type = "slider"
        self.name = name
        self.originalPos = pos
        self.length = length
        self.positionO = CircularPositionalBox(15)
        self.positionO.setPosition(addP(pos, (10,10)))
        self.displayScalar = sliderRange[1]-sliderRange[0]
        self.sliderRange = sliderRange
        self.bar = generateColorBox((20, length), (0,0,0,0))
        placeOver(self.bar, generateColorBox((2, length), hexColorToRGBA(FRAME_COLOR)), (9,0))
        placeOver(self.bar, generateColorBox((20, 3), hexColorToRGBA(FRAME_COLOR)), (0,0))
        placeOver(self.bar, generateColorBox((20, 3), hexColorToRGBA(FRAME_COLOR)), (0, length-3))
        self.updatePos(0, -9999999)
    def tick(self, img, active):
        placeOver(img, self.bar, self.originalPos)
        placeOver(img, POINT_SELECTED_ARRAY if active else POINT_IDLE_ARRAY, self.positionO.getPosition(), True)
        if active: 
            placeOver(img, displayText(str(round((self.positionO.getY()-self.originalPos[1])/self.length*self.displayScalar+self.sliderRange[0])), "s", (0,0,0,150), (255,255,255,255)), addP(self.positionO.getPosition(), (0,25)), True)
    def getData(self):
        return round((self.positionO.getY()-self.originalPos[1])/self.length*self.displayScalar+self.sliderRange[0])
    def setData(self, extent):
        self.updatePos(0, self.originalPos[1] + (extent-self.sliderRange[0])/self.displayScalar*self.length)
    def updatePos(self, rmx, rmy):
        self.positionO.setY(max(self.originalPos[1], min(rmy, self.originalPos[1] + self.length)))
    def keepInFrame(self, minX, minY, maxX, maxY):
        pos = self.positionO.getPosition()
        if pos[0] < minX or maxX < pos[0] or pos[1] < minY or maxY < pos[1]:
            self.positionO.setPosition((round(max(minX,min(pos[0],maxX))), round(max(minY,min(pos[1],maxY)))))
    def getInteractable(self, rmx, rmy):
        return self.positionO.getInteract(rmx, rmy)
    
class CheckboxVisualObject:
    '''A checkbox, basically a simple toggle.'''
    def __init__(self, name, pos:tuple|list, size:tuple|list = (29,29), state = False):
        self.type = "checkbox"
        self.name = name
        self.img = generateIcon(generateColorBox(size, (255,0,0,255)), False, size)
        self.img2 = generateIcon(generateColorBox(size, (0,255,0,255)), False, size)
        self.positionO = RectangularPositionalBox((self.img.shape[1],self.img.shape[0]), pos[0], pos[1])
        self.active = 0
        self.state = state
    def tick(self, img, active):
        if active: self.active +=1
        else: self.active = 0
        if self.active == 1: self.state = not(self.state)
        placeOver(img, self.img2 if self.state else self.img, self.positionO.getPosition(), False)
    def updatePos(self, rmx, rmy):
        pass
    def keepInFrame(self, minX, minY, maxX, maxY):
        pos = self.positionO.getPosition()
        if pos[0] < minX or maxX < pos[0] or pos[1] < minY or maxY < pos[1]:
            self.positionO.setPosition((max(minX,min(pos[0],maxX)), max(minY,min(pos[1],maxY))))
    def getInteractable(self,rmx,rmy):
        return self.positionO.getInteract(rmx, rmy)
    
class TextButtonPushVisualObject:
    '''A button, but it has text! and it resets itself after some ticks!'''
    def __init__(self, name, text:numpy.ndarray, pos:tuple|list, time = 60):
        self.type = "button"
        self.name = name
        temp = displayText(str(text), "m")
        self.img = generateIcon(temp, False, (temp.shape[1],temp.shape[0]))
        self.img2 = generateIcon(temp, True, (temp.shape[1],temp.shape[0]))
        self.positionO = RectangularPositionalBox((self.img.shape[1],self.img.shape[0]), pos[0], pos[1])
        self.lastPressed = 9999999
        self.state = False
        self.time = time
    def tick(self, img, active):
        if active: self.lastPressed = 0
        else: self.lastPressed += 1
        self.state = (self.time > self.lastPressed)
        placeOver(img, self.img2 if self.state else self.img, self.positionO.getPosition(), False)
    def updatePos(self, rmx, rmy):
        pass
    def keepInFrame(self, minX, minY, maxX, maxY):
        pos = self.positionO.getPosition()
        if pos[0] < minX or maxX < pos[0] or pos[1] < minY or maxY < pos[1]:
            self.positionO.setPosition((max(minX,min(pos[0],maxX)), max(minY,min(pos[1],maxY))))
    def getInteractable(self,rmx,rmy):
        return self.positionO.getInteract(rmx, rmy)