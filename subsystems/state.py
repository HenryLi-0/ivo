'''This file is used for transfering information from interface tick and image rendering processes'''
from subsystems.visuals import *

class State:
    def __init__(self):
        self.mx = 0
        self.my = 0
        self.prevmx = 0
        self.prevmy = 0
        self.mPressed = False
        self.mRising = False
        self.fps = 0
        self.ticks = 0
        self.deltaTicks = 1
        '''Interactable Visual Objects'''
        '''
        Code:
        a - example A
        b - example B
        '''
        self.ivos = {
            -999 : [" ", DummyVisualObject("dummy", (0,0))], # used for not interacting with anything
            -998 : [" ", DummyVisualObject("dummy", (0,0))], # used for text boxes
            -997 : [" ", DummyVisualObject("dummy", (0,0))], # used by keybinds
            -996 : [" ", DummyVisualObject("dummy", (0,0))], # used by scrolling

            # Example Usage
            -99 : ["a", OrbVisualObject("example", (145,165))],
            -98 : ["a", ButtonVisualObject("Example Button", (200,150), PLACEHOLDER_IMAGE_5_ARRAY, PLACEHOLDER_IMAGE_3_ARRAY)],
            -97 : ["a", EditableTextBoxVisualObject("Example Textbox", (20,150), "Textbox", False)],
            -96 : ["a", IconVisualObject("Example Icon", (20,195), ICON_CONSOLE_ARRAY, (33,33))],
            -95 : ["a", ToggleVisualObject("Example Toggle", (20,245), ICON_CONSOLE_ARRAY, ICON_CONSOLE_ARRAY, (33,33), lambda: print("on"), lambda: print("off"))],
            -94 : ["a", HorizontalSliderVisualObject("Example Horizontal Slider", (50,300), 100, [0,100])],
            -93 : ["a", VerticalSliderVisualObject("Example Vertical Slider", (20,330), 100, [0,100])],
            -92 : ["a", CheckboxVisualObject("Example Checkbox", (80,360), (33,33), True)],
            -91 : ["a", TextButtonPushVisualObject("Example Text Button", "Some Button", (20,475))],
        }
        '''Control'''
        self.interacting = -999
        self.previousInteracting = -999
        self.mouseScroll = 0 
        self.consoleAlerts = []
        self.keybindLastUpdate = time.time()
        '''Sliders'''
        self.sliders = []
        self.slidersData = []

    def createIVO(self):
        self.ivos[self.c.c()]