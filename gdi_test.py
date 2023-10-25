
import random
from Suura.includes.payloads.gdi_payloads import Screen,VAR
from Suura.includes.util import gdi32
from Suura.includes.util import GetDC
dc = GetDC()
while True:
    gdi32.BitBlt(dc,random.randint(1,10),random.randint(1,20),Screen.SCREEN_X,Screen.SCREEN_X,dc,0,0,VAR.SRCCOPY)
    gdi32.BitBlt(dc,random.randint(1,10) % 10 - 20,random.randint(1,20),Screen.SCREEN_X,Screen.SCREEN_X,dc,0,0,VAR.SRCCOPY)