'''This file is all about managing what the user sees'''

from settings import *
from PIL import ImageTk, Image
from tkinter import filedialog
import time, random, ast
from subsystems.render import *
from subsystems.fancy import *
from subsystems.simplefancy import *
from subsystems.visuals import *
from subsystems.counter import Counter
from subsystems.point import *
from subsystems.bay import *
from subsystems.state import *

from subsystems.section.exampleA import SectionExampleA
from subsystems.section.exampleB import SectionExampleB

class Interface:
    def __init__(self):
        self.s = State()
        self.previousKeyQueue = []

    def tick(self,mx,my,mPressed,fps,keyQueue,mouseScroll):
        '''Entire Screen: `(0,0) to (1365,697)`: size `(1366,698)`'''
        self.s.tick(mx,my,mPressed,fps,keyQueue,mouseScroll)

        '''Interacting With...'''
        self.s.previousInteracting = self.s.interacting
        if not(self.s.mPressed):
            self.s.interacting = -999
        if self.s.interacting == -999 and self.s.mPressed and self.s.mRising:
            processed = False
            for id in self.s.ivos:
                for section in SECTIONS:
                    if self.s.ivos[id][0] == section:
                        if self.s.ivos[id][1].getInteractable(self.s.mx - SECTIONS_DATA[section][0][0], self.s.my - SECTIONS_DATA[section][0][1]):
                            self.s.interacting = id
                            processed = True
                            break
                if processed: break
        if self.s.interacting != -999:
            section = self.s.ivos[self.s.interacting][0]
            self.s.ivos[self.s.interacting][1].updatePos(self.s.mx - SECTIONS_DATA[section][0][0], self.s.my - SECTIONS_DATA[section][0][1])
            self.s.ivos[self.s.interacting][1].keepInFrame(SECTIONS_DATA[section][3][0],SECTIONS_DATA[section][3][1],SECTIONS_DATA[section][4][0],SECTIONS_DATA[section][4][1])
        if (self.s.mPressed) and (self.s.previousInteracting == -999) and (self.s.interacting != -999) and (self.s.ivos[self.s.interacting][1].type  == "textbox"): 
            self.s.stringKeyQueue = self.s.ivos[self.s.interacting][1].txt
        if (self.s.interacting != -999) and (self.s.ivos[self.s.interacting][1].type  == "textbox"):
            self.s.ivos[self.s.interacting][1].updateText(self.s.stringKeyQueue)
        if (self.s.previousInteracting != -999) and (self.s.previousInteracting != -998):
            if (self.s.ivos[self.s.previousInteracting][1].type  == "textbox"):
                if not(self.s.interacting == -998):
                    self.s.interacting = self.s.previousInteracting
                    self.s.ivos[self.s.interacting][1].updateText(self.s.stringKeyQueue)
                else:
                    self.s.ivos[self.s.previousInteracting][1].updateText(self.s.stringKeyQueue)

    def processExampleA(self, im):
        return SectionExampleA.render(self.s, im)
    
    def processExampleB(self, im):
        return SectionExampleB.render(self.s, im)

    def saveState(self):
        pass

    def close(self):
        pass
