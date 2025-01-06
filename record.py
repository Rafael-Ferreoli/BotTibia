import pyautogui as pg
from pynput.keyboard import Listener
from pynput import keyboard
import json
import os

from constants import FOLDER_NAME


def create_folder():
    if not os.path.isdir(FOLDER_NAME):
        os.mkdir(FOLDER_NAME)



class Rec:
    def __init__(self):
        create_folder()
        self.count = 0
        self.coordinates = []

    def photo(self):
        x, y = pg.position()
        photo = pg.screenshot(region=(x-4, y-4, 10, 10))
        path = f'{FOLDER_NAME}/flag_{self.count}.png'
        photo.save(path)
        self.count = self.count + 1
        infos = {
            "path": path,
            "down_hole": 0,
            "up_hole": 0,
            "wait": 10
        }
        self.coordinates.append(infos)

    def down_hole(self):
        last_coordinates = self.coordinates[-1]
        last_coordinates['down_hole'] = 1

    def up_hole(self):
        last_coordinates = self.coordinates[-1]
        last_coordinates['up_hole'] = 1


    def key_code(self,key):
        if key == keyboard.Key.esc:
            with open(f'{FOLDER_NAME}/infos.json','w') as file:
                file.write(json.dumps(self.coordinates))
            return False
        if key == keyboard.Key.insert:
            self.photo()
        if key == keyboard.Key.page_down:
            self.down_hole()
        if key == keyboard.Key.page_up:
            self.up_hole()

    def start(self):
        with Listener(on_press=self.key_code) as listener:
            listener.join()

record = Rec()
record.start()
