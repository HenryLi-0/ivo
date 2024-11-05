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

    def tick(self,mx,my,mPressed,fps,keyQueue,mouseScroll):
        '''Entire Screen: `(0,0) to (1365,697)`: size `(1366,698)`'''
        self.s.tick(mx,my,mPressed,fps,keyQueue,mouseScroll)

        interacting = self.s.interacting

        '''Keyboard'''
        for key in keyQueue: 
            if not key in self.s.previousKeyQueue:
                if key in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789":
                    self.s.stringKeyQueue+=key
                else:
                    if key=="space":    self.s.stringKeyQueue+=" "
                    if key=="slash":    self.s.stringKeyQueue+="/"
                    if key=="asterisk": self.s.stringKeyQueue+="*"
                    if key=="equal":    self.s.stringKeyQueue+="="
                    if key=="at":       self.s.stringKeyQueue+="@"
                    if key=="minus":    self.s.stringKeyQueue+="-"
                    if key=="colon":    self.s.stringKeyQueue+=":"
                    if key=="BackSpace":
                        if len(self.s.stringKeyQueue) > 0:
                            self.s.stringKeyQueue=self.s.stringKeyQueue[0:-1]
                    if key=="Return" or key=="Control_L":
                        interacting = -998
                        break
        self.s.previousKeyQueue = keyQueue.copy()

        keybind = None
        if (interacting == -999 or interacting == -997) and (time.time() - self.s.keybindLastUpdate > 0.2):
            if KB_EXAMPLE(keyQueue):
                '''EXAMPLE KEYBIND: CTRL + SPACE'''
                print("example keybind")
                keybind = "example"

        if self.s.currentKeybind[1] != keybind and keybind != None:
            keybind = [True, keybind]
        else:
            keybind = [False, keybind]
        self.s.currentKeybind = keybind

        '''Mouse Scroll'''
        self.s.mouseScroll = mouseScroll
        if abs(self.s.mouseScroll) > 0:
            if interacting == -999: interacting = -996
            if interacting == -996:
                print("scrolling!")
        else:
            if interacting == -996: interacting = -999
        pass

        '''Interacting With...'''
        self.s.previousInteracting = interacting
        previousInteracting = self.s.previousInteracting
        if not(self.s.mPressed):
            interacting = -999
        if interacting == -999 and self.s.mPressed and self.s.mRising:
            processed = False
            for id in self.s.ivos:
                for section in SECTIONS:
                    if self.s.ivos[id][0] == section:
                        if self.s.ivos[id][1].getInteractable(self.s.mx - SECTIONS_DATA[section][0][0], self.s.my - SECTIONS_DATA[section][0][1]):
                            interacting = id
                            processed = True
                            break
                if processed: break
        if interacting != -999:
            section = self.s.ivos[interacting][0]
            self.s.ivos[interacting][1].updatePos(self.s.mx - SECTIONS_DATA[section][0][0], self.s.my - SECTIONS_DATA[section][0][1])
            self.s.ivos[interacting][1].keepInFrame(SECTIONS_DATA[section][3][0],SECTIONS_DATA[section][3][1],SECTIONS_DATA[section][4][0],SECTIONS_DATA[section][4][1])
        if (self.s.mPressed) and (previousInteracting == -999) and (interacting != -999) and (self.s.ivos[interacting][1].type  == "textbox"): 
            self.s.stringKeyQueue = self.s.ivos[interacting][1].txt
        if (interacting != -999) and (self.s.ivos[interacting][1].type  == "textbox"):
            self.s.ivos[interacting][1].updateText(self.s.stringKeyQueue)
        if (previousInteracting != -999) and (previousInteracting != -998):
            if (self.s.ivos[previousInteracting][1].type  == "textbox"):
                if not(interacting == -998):
                    interacting = previousInteracting
                    self.s.ivos[interacting][1].updateText(self.s.stringKeyQueue)
                else:
                    self.s.ivos[previousInteracting][1].updateText(self.s.stringKeyQueue)

        self.s.interacting = interacting
        self.s.previousInteracting = previousInteracting

        '''Schedule Section Updates'''
        if not(self.s.interacting in SYS_IVOS):
            self.s.scheduleSectionUpdate(self.s.ivos[self.s.interacting][0])
        
        self.s.scheduleSectionUpdate("b")

        if SHOW_CROSSHAIR:
            for section in SECTIONS:
                if self.s.mouseInSection(section) or self.s.mouseWasInSection(section):
                    self.s.scheduleSectionUpdate(section)

    def processNone(self, im):
        return im

    def processExampleA(self, im):
        return SectionExampleA.render(self.s, im)
    
    def processExampleB(self, im):
        return SectionExampleB.render(self.s, im)

    def saveState(self):
        pass

    def close(self):
        pass
