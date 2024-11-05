from settings import *
import time, math
from PIL import Image, ImageTk
from subsystems.render import *

n = 100

BACKGROUND = setSizeSize(PLACEHOLDER_IMAGE, (1024,1024))
BACKGROUND_ARRAY = imageToArray(BACKGROUND)
TRANSPARENT = setSizeSize(setTransparency(PLACEHOLDER_IMAGE_5,50), (1024,1024))
TRANSPARENT_ARRAY = imageToArray(TRANSPARENT)

TEST_POSITIONS = [(round(random.random()*1024)-512,round(random.random()*1024)-512) for i in range(n)]

def placeOver(img1:numpy.ndarray, img2:numpy.ndarray, position:list|tuple, center = False):
    '''Modifies image 1 (background) as an array of image 2 (overlay) placed on top of image 1 (background), given as numpy arrays'''
    if center: position = (round(position[0]-img2.shape[1]*0.5),round(position[1]-img2.shape[0]*0.5))
    img1H, img1W = img1.shape[:2] 
    img2H, img2W = img2.shape[:2]

    if position[1]>img1H or -position[1]>img2H: return False
    if position[0]>img1W or -position[0]>img2W: return False
    
    startX = math.floor(max(position[0], 0))
    startY = math.floor(max(position[1], 0))
    endX = math.floor(min(position[0]+img2W, img1W))
    endY = math.floor(min(position[1]+img2H, img1H))

    img2 = img2[round(max(-position[1], 0)):round((max(-position[1], 0)+(endY-startY))), round(max(-position[0], 0)):round((max(-position[0], 0)+(endX-startX)))]

    alpha_overlay = img2[:, :, 3] / 255.0
    overlayRGB = img2[:, :, :3]
    backgroundRGB = img1[startY:endY, startX:endX, :3]
    alpha_background = img1[startY:endY, startX:endX, 3] / 255.0

    if numpy.any(img2[:, :, 3] < 0):
        alpha_background = img1[startY:endY, startX:endX, 3].astype(numpy.float64)
        alpha_background += img2[:, :, 3].astype(numpy.float64)
        alpha_background[alpha_background < 0] = 0
        alpha_background[alpha_background > 255] = 255
        img1[startY:endY, startX:endX, 3] = alpha_background.astype(numpy.uint8)
    else:
        combined_alpha = alpha_overlay + alpha_background * (1 - alpha_overlay)
        blendedRGB = (overlayRGB*alpha_overlay[:, :, None]+backgroundRGB*(1-alpha_overlay[:, :, None])).astype(numpy.uint8)    
        img1[startY:endY, startX:endX, :3] = blendedRGB
        img1[startY:endY, startX:endX, 3] = (combined_alpha * 255).astype(numpy.uint8)
    
    return True

total = 0
for location in TEST_POSITIONS:
    temp1 = BACKGROUND_ARRAY.copy()
    temp2 = TRANSPARENT_ARRAY.copy()
    start = time.time()
    placeOver(temp1, temp2, location)
    end = time.time()
    total += (end-start)
print(f"placeOver avg: {total/n}")



def neoPlaceOver(img1: Image, img2: Image, position:list|tuple, center = False):
    '''Modifies image 1 (background) as an array of image 2 (overlay) placed on top of image 1 (background), given as PIL images'''
    if center: X, Y = (position[0] - math.floor(img2.width/2), position[1] - math.floor(img2.height/2))
    else: X, Y = position
    if (X < img1.width) and (Y < img1.height) and (X + img2.width > 0) and (Y + img2.height > 0):
        if (X < 0) or (Y < 0) or (X + img2.width > img1.width) or (Y + img2.height > img1.height):
            SX = math.floor(max(X, 0))
            SY = math.floor(max(Y, 0))
            crop = img2.crop((
                max(-X, 0),
                max(-Y, 0),
                max(-X, 0) + (math.floor(min(X + img2.width, img1.width)) - SX),
                max(-Y, 0) + (math.floor(min(Y + img2.height, img1.height)) - SY)
            ))
            img1.paste(crop, (SX, SY), crop)
        else:
            img1.paste(img2, (X, Y), img2)
    return True

total = 0
for location in TEST_POSITIONS:
    temp1 = BACKGROUND.copy()
    temp2 = TRANSPARENT.copy()
    start = time.time()
    neoPlaceOver(temp1, temp2, location)
    end = time.time()
    total += (end-start)
print(f"neoPlaceOver avg: {total/n}")


# from subsystems.render import rotateDeg
# temp1 = BACKGROUND.copy()
# # temp2 = TRANSPARENT.copy()
# temp2 = rotateDeg(TRANSPARENT.copy(), 45)

# print(temp2.width, temp2.height)

# neoPlaceOver(temp1, temp2, (100,50), True)
# temp1.show()