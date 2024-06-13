import ctypes
from ctypes import wintypes
user32 = ctypes.windll.user32
from Suura.includes.util import getHwnd,GetDC
class Screen:
    SCREEN_X = user32.GetSystemMetrics(0) # it's defining X position
    SCREEN_Y = user32.GetSystemMetrics(1) # it's defining Y position

class Variable:
    SRCCOPY = 0X00CC0020
    SRCAND = 0X008800C6

class Color:
    ColorRed    = 	    0X9F
    ColorWhite  =       0XFFFFFF
    ColorYellow =       0XDB
    ColorBlueViolet = 	0X8A
    ColorGrey   = 	    0X808080

class RECT(ctypes.Structure):
    _fields_ = [
        ("left",ctypes.c_long),
        ("right",ctypes.c_long),
        ("top",ctypes.c_long),
        ("bottom",ctypes.c_long)
    ]

class PAINTSTRUCTURE(ctypes.Structure):
    _fields_ = [
        ("HDC",wintypes.HDC),
        ("fErase",ctypes.c_bool),
        ("rcPaint",RECT),
        ("fRestore",ctypes.c_bool),
        ("fIncUpdate",ctypes.c_bool),
        ("rgbReserved",ctypes.c_byte)
    ]