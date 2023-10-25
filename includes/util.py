import os
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
import threading
import playsound
import multiprocessing
from ctypes import wintypes as w

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
class AudioPlayer:
    class Player:
        def __init__(self,fname):
            self.fname = fname
            self.status = False
            self.loop = False
            self.toggle = False
        def play(self):
            if not self.status:
                self.process = multiprocessing.Process(target=playsound.playsound,args=(self.fname,))
                self.process.daemon = True
                self.status = True
                self.process.start()
                self.status_checker()
            elif self.loop:
                self.play()
        def stop(self):
            if self.process and self.process.is_alive() and self.toggle:
                self.toggle = False
                self.status = False
                self.process.terminate()
        def handler_of_status_checker(self):
            while self.toggle:
                if self.process and not self.process.is_alive():
                    self.process = None
                    self.status = False
                    if self.loop:
                        self.play()
                elif self.process is None and not self.loop:
                    self.toggle = False
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
            except:
                pass
    def __repr__(self) -> str:
        return_string = "<%s " % (self.__class__.__name__)
        for key_,values_ in self.playable_songs.items():
            return_string += "%s" % (getattr(self,key_).__repr__())
        return_string += ">"
        return return_string
class Mouse:
    """
    Mouse Pozisyon bilgilerini getirmek için
    """
    # bu sınıf artık sadece mouse kordinat bilgisini getirmeyecek genel olarak mouse işlevlerini kontrol edicek
    class POINT(ctypes.Structure): # burayı düzelt ve built-in olan wintypes.POINT kullan
        _fields_ = [("pos_x",ctypes.c_int),("pos_y",ctypes.c_int)]
    def __new__(cls) -> tuple:
        pos_handler = Mouse.POINT()
        user32.GetCursorPos(ctypes.byref(pos_handler))
        return (pos_handler.pos_x,pos_handler.pos_y)
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
    return user32.GetDC(0)
def get_icacls_credentials() -> str:
    return r"%s\%s" % (socket.gethostname(),os.environ["USERNAME"])
def is_admin() -> bool:
    try:
        return shell32.IsUserAnAdmin()
    except:
        return False
    return True
def get_lang() -> str:
    return locale.windows_locale[kernel32.GetUserDefaultUILanguage()]
def list_windows():
    hwnds = []
    window_names = {}
    def callback(Hwnd,LongParam):
        hwnds.append(Hwnd)
        return True
    func = ctypes.WINFUNCTYPE(ctypes.c_bool,ctypes.c_int,ctypes.c_int)(callback)
    user32.EnumWindows(func,0)
    for handles in hwnds:
        windowlenght = user32.GetWindowTextLengthW(handles) + 1
        buffer = ctypes.create_unicode_buffer(windowlenght)
        user32.GetWindowTextW(handles,buffer,windowlenght)
        if len(buffer.value) > 0 and buffer.value != "":
            window_names[buffer.value]=handles
    return window_names
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
def GetCurrentWindowTitle() -> str:
    """
    Mevcut var olan pencere isminin bilgisini getirir
    """
    Hwnd = user32.GetForegroundWindow()
    CurrentWindowTitleLenght = user32.GetWindowTextLengthW(Hwnd)
    mem_buffer = ctypes.create_unicode_buffer(CurrentWindowTitleLenght + 1)
    user32.GetWindowTextW(Hwnd,mem_buffer,CurrentWindowTitleLenght + 1)
    if mem_buffer.value is None:
        mem_buffer.value = "" # burada eğer ki veri boş dönerse çökmemesi için yine de boş bir string verdik
    return mem_buffer.value
 
class SetBackground:
    def __init__(self,filename: str):
        if not os.path.exists(filename) and os.path.isfile(filename):
            raise Exception("File Must be exist or file")
        self.fname = filename
        self.is_setted = False
    def set_bg(self):
        try:
            user32.SystemParametersInfoW(20,0,self.fname,0)
            self.is_setted = not self.is_setted
        except:
            pass
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
    manufecturer = wmi_.Manufacturer.lower()
    if "vmware" in manufecturer or "innotek GmbH" in manufecturer:
        return True
    return False

class RegeditEdit:
    def __init__(self,data=None):
        self.tuples = data
        if len(self.tuples) == 1:
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

def send_char(s: str,delay=0.00050099312414134):
    i = INPUT()
    i.type = INPUT_KEYBOARD
    for c in s:
        i.ki = KEYBDINPUT(0,ord(c),KEYEVENTF_UNICODE,0,0)
        lib.SendInput(1,ctypes.byref(i),ctypes.sizeof(INPUT))
        i.ki.dwFlags |= KEYEVENTF_KEYUP
        lib.SendInput(1,ctypes.byref(i),ctypes.sizeof(INPUT))
        time.sleep(delay)
