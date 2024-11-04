from subsystems.checks import Check
Check.check()

import tkinter as tk
from subsystems.window import Window

window = Window()
window.start()


'''
original:
avg of 1095 frames: 0.03700961282808487 seconds
new:
avg of 1095 frames: 0.0294141542965963 seconds
'''