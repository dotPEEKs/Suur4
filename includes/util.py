import os
import sys

import wmi
import time
import socket
import locale
import signal
import struct
import ctypes
import psutil
import random
import winreg
import secrets
import hashlib
import logging
import threading
import playsound
import multiprocessing
from ctypes import wintypes as w
# add local lib
from Suura.includes.Qimg.Qimg import HMAC
from Suura.includes.Qimg.Qimg import Build
from Suura.includes.Qimg.Qimg import PBDKF2
from Suura.includes.Qimg.Qimg import AESCrypto
user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32
kernel32 = ctypes.windll.kernel32
shell32 = ctypes.windll.shell32
KEYEVENTF_SCANCODE = 0x8
KEYEVENTF_UNICODE = 0x4
KEYEVENTF_KEYUP = 0x2
SPACE = 0x39
INPUT_KEYBOARD = 1
ULONG_PTR = ctypes.c_ulong if ctypes.sizeof(ctypes.c_void_p) == 4 else ctypes.c_ulonglong
sys_ = logging.StreamHandler(sys.stdout)
logger = logging.getLogger().addHandler(sys_)
class AudioPlayer:
    class Player:
        def __init__(self,fname):
            self.fname = fname
            self.status = False
            self.loop = False
            self.toggle = False
        def play(self):
            if not self.status:
                print("SONG STARTED %s AT %s" % (self.fname,time.strftime("%H:%M %d:%m:%Y")))
                self.process = multiprocessing.Process(target=playsound.playsound,args=(self.fname,))
                self.process.daemon = True
                self.status = True
                self.process.start()
                self.status_checker()
            elif self.loop and not self.status:
                self.play()
        def stop(self):
            if self.process and self.process.is_alive() and self.toggle:
                self.toggle = False
                self.status = False
                self.process.terminate()
                print("SONG CLOSED %s AT %s" % (self.fname,time.strftime("%H:%M %d:%m:%Y")))
        def handler_of_status_checker(self):
            while self.toggle:
                if self.process and not self.process.is_alive():
                    self.process = None
                    self.status = False
                    if self.loop:
                        self.play()
                elif self.process is None and not self.loop:
                    self.toggle = False
                time.sleep(1)
        def status_checker(self):
            """
            handling for control status 
            """
            if not self.toggle:
                self.toggle = True
                self.thread = threading.Thread(target=self.handler_of_status_checker)
                self.thread.daemon = True
                self.thread.start()
        def __repr__(self) -> str:
            return "<%s name = %s is_playing = %s>" % (self.__class__.__name__,os.path.basename(self.fname),self.status)
    def __init__(self,**songs):
        self.playable_songs = {}
        for song_names,song_paths in songs.items():
            if not os.path.exists(song_paths):
                print("%s doesnt exists !!!" % (song_paths))
            elif not os.path.isfile(song_paths):
                print("%s it's dont seems like a file given parameters must be file " % (song_paths))
            elif not os.path.splitext(song_paths)[1][1:] in list(map(lambda item:item.lower(),"WAV MP3 FLAC OGG AAC M4A".split(" "))):
                print("Not supported file extension : %s" % (os.path.splitext(song_paths)[1]))
            else:
                self.playable_songs[song_names] = song_paths
        for keys,values in self.playable_songs.items():
            try:
                setattr(self,str(keys),self.Player(values))
                logging.info("%s Appended" % (values))
            except Exception as set_attr_fault:
                logging.critical("%s I cannot append this song %s because this error: %s" % (values,str(set_attr_fault)))
    def __repr__(self) -> str:
        return_string = "<%s " % (self.__class__.__name__)
        for key_,values_ in self.playable_songs.items():
            return_string += "%s" % (getattr(self,key_).__repr__())
        return_string += ">"
        return return_string
class Mouse:
    def __init__(self):
        self._mouse_movement_lock = False
    def move(self,x: int,y: int):
        if isinstance(x,int) and isinstance(y,int):
            user32.SetCursorPos(x,y)
    @property
    def get_mouse_pos(self) -> w.POINT:
        struct_ = w.POINT()
        user32.GetCursorPos(ctypes.byref(struct_))
        return struct_
    @property
    def x(self):
        return self.get_mouse_pos.x
    @property
    def y(self):
        return self.get_mouse_pos.y
    def _lock_thread(self):
        while self._mouse_movement_lock:
            self.move(100,100)
            time.sleep(0.2)
    def lock(self):
        if not self._mouse_movement_lock:
            self._mouse_movement_lock = True
            thread = threading.Thread(target=self._lock_thread)
            thread.daemon = True
            thread.start()
    def unlock(self):
        self._mouse_movement_lock = False
    def __repr__(self) -> str:
        return "<%s x = %s y = %s locked = %s>" % (self.__class__.__name__,self.x,self.y,self._mouse_movement_lock)
def list_proc_pids_from_name(proc_name: str) -> list:
    pids = []
    for process in psutil.process_iter():
        if process.name() == proc_name:
            pids.append(process.pid)
    return pids
def kill_procs_from_pids(*pids):
    for pid in pids:
        try:
            os.kill(pid,signal.SIGTERM)
        except:
            pass
def getHwnd():
    return user32.GetForegroundWindow()
def getDCHwnd():
    return user32.GetWindowDC()
def GetDC() -> int:
    return user32.GetDC(getDCHwnd())
def get_icacls_credentials() -> str:
    return r"%s\%s" % (socket.gethostname(),os.environ["USERNAME"])
def is_admin() -> bool:
    try:
        return shell32.IsUserAnAdmin()
    except:
        return False
    return True
def GetLocalLocale() -> str:
    return locale.windows_locale[kernel32.GetUserDefaultUILanguage()]

def GetWindowText(Hwnd) -> str:
    WindowTextLen = user32.GetWindowTextLengthW(Hwnd) + 1
    buffer = ctypes.create_unicode_buffer(WindowTextLen)
    user32.GetWindowTextW(Hwnd,buffer,WindowTextLen)
    if buffer.value is None:
        buffer.value = "" # set default value empty string
    return buffer.value
def GetActiveWindow() -> str:
    """
    Mevcut var olan pencere isminin bilgisini getirir
    """
    Hwnd = user32.GetForegroundWindow()
    return GetWindowText(Hwnd)
def GetActiveWindows(*,get_only_hwnds = False,get_only_window_names = False) -> dict:
    """
    Bütün açık olan pencelerin ismini getitirir
    Eğer ki sadece handle verisini almak istiyorsan
    1.Kullanım: GetActiveWindows(get_only_hwnds = True) -> Liste şeklinde hwnd değerlerini vericektir
    2.Kullanım: GetActiveWindows(get_only_names = True) -> Liste şeklinde pencere isimlerini vericektir
    3.Kullanım: GetActiveWindows() -> Sözlük şeklinde dönüş sağlayacaktır 
    { HandleWindows : Window Text }
    """
    hwnds = []
    window_credentials = {}
    def callback_func(Hwnd,LongParam):
        hwnds.append(Hwnd)
        return True
    window_enumerator = ctypes.WINFUNCTYPE(ctypes.c_bool,ctypes.c_int,ctypes.c_int)(callback_func)
    user32.EnumWindows(window_enumerator,0)
    for handle_window in hwnds:
        window_name = GetWindowText(handle_window)
        if len(window_name) > 0:
            window_credentials[handle_window] = window_name
    if get_only_hwnds:
        return list(window_credentials.keys())
    if get_only_window_names:
        return list(window_credentials.values())
    return window_credentials
def get_pid_from_window_hwnd(window_name: str,hwnd: int) -> int:
    is_window_exists = user32.FindWindowW(None,window_name)
    pid = ctypes.c_ulong()
    if is_window_exists:
        try:
            user32.GetWindowThreadProcessId(hwnd,ctypes.byref(pid))
        except:
            return 0
        return pid.value if pid.value != 0 else 0
    return 0
class SetBackground:
    def __init__(self,filename: str):
        self.dir_mode = False
        if not os.path.exists(filename) and os.path.isfile(filename):
            raise Exception("File Must be exist or file")
        elif os.path.isdir(filename):
            self.dir_mode = True
        self.fname = filename
        self.is_setted = False
        self.looped = False
        self.delay = 0.1
    def set_bg(self,fname):
        SPI_SETDESKWALLPAPER = 0x0014 # equals to 20
        try:
            user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER,0,fname,0)
            self.is_setted = not self.is_setted
        except:
            pass
    def loop_handler(self):
        while self.looped:
            if self.dir_mode:
                for path in os.listdir(self.fname):
                    time.sleep(self.delay)
                    full_p = os.path.join(self.fname,path)
                    self.set_bg(full_p)
                    time.sleep(self.delay)
            time.sleep(self.delay)
    def change_bg(self):
        if self.looped:
            thread = threading.Thread(target=self.loop_handler)
            thread.daemon = True
            thread.start()
        else:
            self.set_bg(self.fname)
    def __repr__(self) -> str:
        return "%s(file = %s is_setted_up = %s)" % (self.__class__.__name__,self.fname,self.is_setted)
def sign_data(data: bytes) -> bytes:
    random_data = secrets.token_bytes(random.randint(1,150))
    return struct.pack(">I",len(random_data))+random_data+data
def unsign_data(data: bytes) -> bytes:
    big_endian_size = 4
    try:
        pad_size = struct.unpack(">I",data[:4])[0]
        chunk = data[pad_size+big_endian_size:]
        return chunk
    except:
        return b"BAD_SIGNATURE"

def is_running_wmware():
    wmi_ = wmi.WMI().Win32_ComputerSystem()[0]
    return Build.DEFAULT_BUILD_SALT + hashlib.sha256(Build.DEFAULT_BUILD_SALT + wmi_.Manufacturer.lower().encode()).digest() in (b'V\xcftF\x12\xe0\x86\xf6\xc7\x8d\xe9Ava\xc7\x1fY,\xc3\x02f<\x00!\xff\xa9!\x86\xbf<\x1aW\x9a\x97\xe5\xe0\x1f\x8b(\xf7f\x85^[\x12\x1f\x8b\xda',
                            b'V\xcftF\x12\xe0\x86\xf6\xc7\x8d\xe9Ava\xc7\x1f\x9e\xd7y]>j\xec\x82\xdfo>\xff/\x92\xf9|v\\r\xc8\x89\x060N6\xea\xcf\xc6\x84\xd4g\xff',
                            b'V\xcftF\x12\xe0\x86\xf6\xc7\x8d\xe9Ava\xc7\x1fK\xf9\xfdo\x9c\xf6\x88\xf6\x1b\xbbi\xa4\x8e\xad_\x89:\xeb\xfac\x9c\xb3\xbb\x8e\xbd\xcd\xe4\x9f\xa9\xf5\xce\xe6')

class RegeditEdit:
    def __init__(self,data=None):
        self.tuples = data
        if len(self.tuples) <= 1:
            self.tuples+=(None,None,None,None,None)
    def init(self):
        for sub_tuples in self.tuples:
            if len(sub_tuples) == 5:
                key_path,sub_path,data_name,data_value,data_type = sub_tuples
                try:
                    key_handler = winreg.OpenKey(key_path,sub_path,0,winreg.KEY_SET_VALUE)
                    winreg.SetValueEx(key_handler,data_name,0,data_type,data_value)
                except:
                    pass
                finally:
                    winreg.CloseKey(key_handler)
ULONG_PTR = c_ulong if ctypes.sizeof(ctypes.c_void_p) == 4 else ctypes.c_ulonglong

# https://stackoverflow.com/questions/62189991/how-to-wrap-the-sendinput-function-to-python-using-ctypes
# i add pyautogui but its create so huge exe file 
class KEYBDINPUT(ctypes.Structure):
    _fields_ = [('wVk' ,w.WORD),
                ('wScan',w.WORD),
                ('dwFlags',w.DWORD),
                ('time',w.DWORD),
                ('dwExtraInfo',ULONG_PTR)]

class MOUSEINPUT(ctypes.Structure):
    _fields_ = [('dx' ,w.LONG),
                ('dy',w.LONG),
                ('mouseData',w.DWORD),
                ('dwFlags',w.DWORD),
                ('time',w.DWORD),
                ('dwExtraInfo',ULONG_PTR)]

class HARDWAREINPUT(ctypes.Structure):
    _fields_ = [('uMsg' ,w.DWORD),
                ('wParamL',w.WORD),
                ('wParamH',w.WORD)]

class DUMMYUNIONNAME(ctypes.Union):
    _fields_ = [('mi',MOUSEINPUT),
                ('ki',KEYBDINPUT),
                ('hi',HARDWAREINPUT)] 

class INPUT(ctypes.Structure):
    _anonymous_ = ['u']
    _fields_ = [('type',w.DWORD),
                ('u',DUMMYUNIONNAME)]

lib = ctypes.windll.user32
lib.SendInput.argtypes = w.UINT,ctypes.POINTER(INPUT),ctypes.c_int
lib.SendInput.restype = w.UINT

def send_special_code(code):
    i = INPUT()
    i.type = INPUT_KEYBOARD
    i.ki = KEYBDINPUT(0,code,KEYEVENTF_SCANCODE,0,0)
    lib.SendInput(1,ctypes.byref(i),ctypes.sizeof(INPUT))
    i.ki.dwFlags |= KEYEVENTF_KEYUP
    lib.SendInput(1,ctypes.byref(i),ctypes.sizeof(INPUT))

def send_char(s: str,delay=0.00099312414134):
    i = INPUT()
    i.type = INPUT_KEYBOARD
    for c in s:
        i.ki = KEYBDINPUT(0,ord(c),KEYEVENTF_UNICODE,0,0)
        lib.SendInput(1,ctypes.byref(i),ctypes.sizeof(INPUT))
        i.ki.dwFlags |= KEYEVENTF_KEYUP
        lib.SendInput(1,ctypes.byref(i),ctypes.sizeof(INPUT))
        time.sleep(delay)


def xor_encrypt(plain_text, key):
    encrypted_text = ""
    for char in plain_text:
        encrypted_text += chr(ord(char) ^ key)
    return encrypted_text

def xor_decrypt(encrypted_text, key):
    decrypted_text = ""
    for char in encrypted_text:
        decrypted_text += chr(ord(char) ^ key)
    return decrypted_text
