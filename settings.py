'''
Settings

Here are the parts:
- Calculation
- Visuals
- Saving
- Keybinds
- Constants (Please do not change!)
'''

'''Calculation'''
FLOAT_ACCURACY = 3 #This is how many digits after the decimal point things will generally round to


'''Visuals'''
INTERFACE_FPS = 60 # The interface window will be called every 1/INTERFACE_FPS seconds
TICK_MS = 1
OCCASIONAL_TICK_MS = 5000 # Recommended to keep above 1 second, as it runs processes that do not need updates every tick

SHOW_CROSSHAIR = True # Shows a crosshair for the mouse's position

hexColorToRGBA = lambda hexcolor: tuple(int(hexcolor[i:i+2], 16) for i in (1, 3, 5)) + (255,)

BACKGROUND_COLOR = "#333247" #Background color
FRAME_COLOR      = "#524f6b" #Borders and Frame color
SELECTED_COLOR   = "#bebcd5" #Selected Element color
VOID_COLOR       = "#84829b" #Void color

BACKGROUND_COLOR_RGBA = hexColorToRGBA(BACKGROUND_COLOR)
FRAME_COLOR_RGBA      = hexColorToRGBA(FRAME_COLOR     )
SELECTED_COLOR_RGBA   = hexColorToRGBA(SELECTED_COLOR  )
VOID_COLOR_RGBA       = hexColorToRGBA(VOID_COLOR      )


'''Saving'''
import os, time
PATH_SAVE_DEFAULT = os.path.join("saves")

FORMAT_TIME = lambda x: time.strftime("%I:%M:%S %p %m/%d/%Y", time.localtime(x))


'''Keybinds'''
KB_IGNORE    = ["Win_L"]                                                                                # Keys to ignore
KB_EXAMPLE   = lambda keys: (len(keys) == 2) and ("Control_L" in keys) and ("space" in keys)            # Example Keybind


'''Constants - DO NOT CHANGE!!!'''
'''Do not change these constants. Some are probably important. Some are used for testing purposes. 
   Editing certain constants will break things! You have been warned!'''
from PIL import Image, ImageFont
import numpy
from subsystems.simplefancy import *

# Version
VERSION = "v0.0.0"

# Sections
'''Region ID, Top Left, Bottom Right, Size, Keep In Relative Top Left, Keep In Relative Top Right'''
SECTIONS_DATA = {
    " ": [(   0,   0),(   0,   0),(   0,   0),(   0,   0),(   0,   0)],
    "a": [(  20,  20),(1043, 677),(1024, 658),(   0,   0),(1024, 658)],
}
SECTIONS = list(SECTIONS_DATA.keys())

# Imagery
LOADING_IMAGE = Image.open(os.path.join("resources", "loading.png")).convert("RGBA") # 1366x697, Solid, Loading Screen
LOADING_IMAGE_ARRAY = numpy.array(LOADING_IMAGE)
EMPTY_LARGE_IMAGE = Image.open(os.path.join("resources", "blank_large.png")).convert("RGBA")
EMPTY_LARGE_IMAGE_ARRAY = numpy.array(EMPTY_LARGE_IMAGE)
PLACEHOLDER_IMAGE = Image.open(os.path.join("resources", "placeholder", "placeholder.png")).convert("RGBA")    # 512x512, Solid, [black, white, grey]
PLACEHOLDER_IMAGE_ARRAY = numpy.array(PLACEHOLDER_IMAGE)
PLACEHOLDER_IMAGE_2 = Image.open(os.path.join("resources", "placeholder", "placeholder2.png")).convert("RGBA")  # 100x100, Transparent Background [black, white, grey]
PLACEHOLDER_IMAGE_2_ARRAY = numpy.array(PLACEHOLDER_IMAGE_2)
PLACEHOLDER_IMAGE_3 = Image.open(os.path.join("resources", "placeholder", "placeholder3.png")).convert("RGBA")  # 128x128, Solid Background [black, white, grey]
PLACEHOLDER_IMAGE_3_ARRAY = numpy.array(PLACEHOLDER_IMAGE_3)
PLACEHOLDER_IMAGE_4 = Image.open(os.path.join("resources", "placeholder", "placeholder4.png")).convert("RGBA")  # 16x16, Transparent Background [black, white]
PLACEHOLDER_IMAGE_4_ARRAY = numpy.array(PLACEHOLDER_IMAGE_4)
PLACEHOLDER_IMAGE_5 = Image.open(os.path.join("resources", "placeholder", "placeholder5.png")).convert("RGBA")  # 32x32, Solid Background [rainbow]
PLACEHOLDER_IMAGE_5_ARRAY = numpy.array(PLACEHOLDER_IMAGE_5)
MISSING_IMAGE_PATH = os.path.join("resources", "missing.png")
MISSING_IMAGE = Image.open(os.path.join("resources", "missing.png")).convert("RGBA")
MISSING_IMAGE_ARRAY = numpy.array(MISSING_IMAGE)
EMPTY_IMAGE_ARRAY = numpy.zeros((1, 1, 4), dtype=numpy.uint8)

# Fonts
FONT_LARGE = ImageFont.truetype(os.path.join("resources", "Comfortaa-Medium.ttf"), 24)
FONT_MEDIUM = ImageFont.truetype(os.path.join("resources", "Comfortaa-Medium.ttf"), 15)
FONT_SMALL_MEDIUM = ImageFont.truetype(os.path.join("resources", "Comfortaa-Medium.ttf"), 12)
FONT_SMALL = ImageFont.truetype(os.path.join("resources", "Comfortaa-Medium.ttf"), 10)
EDITOR_SPACING = lambda x: x*20+15

# Blank Interface Sections
'''
- Sketch Area:   `(  20,  20) to (1043, 677)` : size `(1024, 658)`
'''

FRAME_SKETCH_INSTRUCTIONS = genereateThemedBorderRectangleInstructions((1024, 658),hexColorToRGBA(FRAME_COLOR))

CURSOR_ARROW_ARRAY = getArrayImageRGBAFromPath(os.path.join("resources", "cursor_arrow.png"))
CURSOR_SELECT_ARRAY = getArrayImageRGBAFromPath(os.path.join("resources", "cursor_select.png"))

ORB_IDLE_ARRAY = getArrayImageRGBAFromPath(os.path.join("resources", "orb_idle.png"))
ORB_SELECTED_ARRAY = getArrayImageRGBAFromPath(os.path.join("resources", "orb_selected.png"))
POINT_IDLE_ARRAY = getArrayImageRGBAFromPath(os.path.join("resources", "point_idle.png"))
POINT_SELECTED_ARRAY = getArrayImageRGBAFromPath(os.path.join("resources", "point_selected.png"))

ICON_CONSOLE_ARRAY = getArrayImageRGBAFromPath(os.path.join("resources", "icon", "console.png"))