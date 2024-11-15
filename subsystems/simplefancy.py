'''This file contains functions related to fancy rendering, but does not import from setting'''

from PIL import Image
import numpy, random, colorsys
from subsystems.render import *

def getArrayImageRGBAFromPath(path):
    '''Given a path, opens the image, converts it to RGBA, and returns it as a numpy array.'''
    return numpy.array(Image.open(path).convert("RGBA"))

def getImageRGBAFromPath(path):
    '''Given a path, opens the image, converts it to RGBA, and returns the Image.'''
    return Image.open(path).convert("RGBA")

def generateColorBox(size:list|tuple = (25,25),color:list|tuple = (255,255,255,255)):
    '''Generates a box of (size) size of (color) color'''
    array = numpy.empty((size[1], size[0], 4), dtype=numpy.uint8)
    array[:, :] = color
    return arrayToImage(array)

def generateUnrestrictedColorBox(size:list|tuple = (25,25),color:list|tuple = (255,255,255,255)):
    '''Generates an array box of (size) size of (color) color without restrictions'''
    array = numpy.empty((size[1], size[0], 4))
    array[:, :] = color
    return array

def generateBorderBox(size:list|tuple = (25,25), outlineW:int = 1, color:list|tuple = (255,255,255,255)):
    '''Generates a bordered box with a transparent inside, with transparent space of (size), and an (outlineW) px thick outline of (color) color surrounding it'''
    array = numpy.zeros((size[1]+2*outlineW, size[0]+2*outlineW, 4), dtype=numpy.uint8)
    array[:outlineW, :, :] = color
    array[-outlineW:, :, :] = color
    array[:, :outlineW, :] = color
    array[:, -outlineW:, :] = color
    return arrayToImage(array)

def generateInwardsBorderBox(size:list|tuple = (25,25), outlineW:int = 1, color:list|tuple = (255,255,255,255)):
    '''Generates a inwards bordered box with a transparent inside, with transparent space of (size - outline), and an (outlineW) px thick outline of (color) color surrounding it'''
    array = numpy.zeros((size[1], size[0], 4), dtype=numpy.uint8)
    array[:outlineW, :, :] = color
    array[-outlineW:, :, :] = color
    array[:, :outlineW, :] = color
    array[:, -outlineW:, :] = color
    return arrayToImage(array)

def generatePastelDark():
    '''Randomly generates a dark pastel color'''
    color = [100]
    color.insert(random.randrange(0,len(color)), random.randrange(100,200))
    color.insert(random.randrange(0,len(color)), random.randrange(100,200))
    color.append(255)
    return color

def translatePastelLight(color):
    '''Translate a dark pastel color to a light pastel color, given the color in RGBA form'''
    colorC = color[0:3]
    colorC = list(colorsys.rgb_to_hsv(colorC[0]/255,colorC[1]/255,colorC[2]/255))
    colorC[2] = 0.9
    colorC = colorsys.hsv_to_rgb(colorC[0],colorC[1],colorC[2])
    return [round(colorC[0]*255), round(colorC[1]*255), round(colorC[2]*255), color[3]]

def genereateThemedBorderRectangleInstructions(size:list|tuple = (25,25),borderColor:list|tuple = (255,255,255,255), background:Image = None, backgroundOffset:list|tuple = (0,0)):
    instructions = []
    if background != None: instructions.append([background, backgroundOffset])
    row = generateColorBox((size[0],3), borderColor)
    col = generateColorBox((3,size[1]), borderColor)
    instructions.append([row, (0,0)])
    instructions.append([col, (0,0)])
    instructions.append([row, (0,size[1]-3)])
    instructions.append([col, (size[0]-3,0)])
    return instructions

def genereateSpecificThemedBorderRectangleInstructions(section, borderColor:list|tuple = (255,255,255,255)):
    '''Generates Instructions for a specific section's Themed Border Rectangle'''
    return None