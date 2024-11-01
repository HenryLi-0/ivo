from subsystems.render import placeOver
from settings import *
import time
from PIL import Image, ImageTk


total = 0
for i in range(100):
    temp1 = LOADING_IMAGE_ARRAY.copy()
    temp2 = LOADING_IMAGE_ARRAY.copy()
    start = time.time()
    placeOver(temp1, temp2, (0,0))
    end = time.time()
    total += (end-start)
print(f"placeOver avg: {total/100}")


total = 0
for i in range(100):
    temp1 = LOADING_IMAGE.copy()
    temp2 = LOADING_IMAGE.copy()
    start = time.time()
    res = Image.alpha_composite(temp1, temp2)
    end = time.time()
    total += (end-start)
print(f"pillow avg: {total/100}")
