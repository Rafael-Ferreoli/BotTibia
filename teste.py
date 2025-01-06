import threading

import pyautogui as pg
import keyboard
import time
import json


while True:
    keyboard.wait('h')
    print(pg.position())