import time
import ctypes
import random
from ctypes import wintypes
from Suura.includes.gdi_util import Screen
from Suura.includes.gdi_util import Variable #variable
from Suura.includes.gdi_util import Color
from Suura.includes.util import GetDC,getHwnd
from Suura.includes.gdi_util import PAINTSTRUCTURE,RECT
class GAMMAPIXEL:
    def __init__(self):
        self.stage_limits = (1,15)
        self.stage = 1
        self.hdc = GetDC()
    def increase_stage(self):
        if self.stage < self.stage_limits[1]:
            self.stage = self.stage + 1
    def decrease_stage(self):
        if self.stage > 1:
            self.stage = self.stage - 1
    def draw(self):
        for _ in range(1,self.stage):
            current_color = Color.ColorWhite
            random_x_pos = random.randint(1,Screen.SCREEN_X)
            random_y_pos = random.randint(1,Screen.SCREEN_Y)
            if random.randint(0,4) % 2 == 0:
                current_color = Color.ColorWhite
            ctypes.windll.gdi32.SetPixel(self.hdc,random_x_pos-1,random_y_pos+1,current_color)
            ctypes.windll.gdi32.SetPixel(self.hdc,random_x_pos+2,random_y_pos-2,current_color)
            ctypes.windll.gdi32.SetPixel(self.hdc,random_x_pos+3,random_y_pos-3,current_color)
            ctypes.windll.gdi32.SetPixel(self.hdc,random_x_pos+4,random_y_pos+4,current_color)
            ctypes.windll.gdi32.SetPixel(self.hdc,random_x_pos-1,random_y_pos+1,current_color)
            ctypes.windll.gdi32.SetPixel(self.hdc,random_x_pos+2,random_y_pos-2,current_color)
            ctypes.windll.gdi32.SetPixel(self.hdc,random_x_pos+3,random_y_pos-3,current_color)
            ctypes.windll.gdi32.SetPixel(self.hdc,random_x_pos+4,random_y_pos+4,current_color)
            ctypes.windll.gdi32.SetPixel(self.hdc,random_x_pos-1,random_y_pos+1,current_color)
            ctypes.windll.gdi32.SetPixel(self.hdc,random_x_pos+2,random_y_pos-2,current_color)
            ctypes.windll.gdi32.SetPixel(self.hdc,random_x_pos+3,random_y_pos-3,current_color)
            ctypes.windll.gdi32.SetPixel(self.hdc,random_x_pos+4,random_y_pos+4,current_color)
            time.sleep(0.5)
    def setstage_maximum(self):
        if self.stage < self.stage_limits[1]:
            self.stage = self.stage_limits[1]
    def setstage_minimum(self):
        if self.stage > self.stage_limits[0]:
            self.stage = self.stage_limits[0]
    def start(self):
        while True:
            self.draw()
            time.sleep(1)