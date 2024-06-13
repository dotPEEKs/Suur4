import threading

import pynput.keyboard

class Log:
    def __init__(self,max_log_size = 30):
        self.log = ""
        self.max_log_size = max_log_size
    def add(self,char: str):
        if len(self.log) > self.max_log_size:
            self.log = ""
        try:
            self.log = self.log + char
        except:
            pass
    def __add__(self, char):
        self.add(char)
    def is_keyword_matching_end_keyword(self,string):
        return self.log[-len(string):] == string
class KeySniffer:
    def __init__(self):
        self.log = Log()
    def start_listener(self):
        with pynput.keyboard.Listener(on_press=self.on_press) as l:
            l.join()
            self.listener = l
    def stop(self):
        if hasattr(self,"listener"):
            self.listener.stop()
    def on_press(self,key):
        if isinstance(key,pynput.keyboard.KeyCode):
            self.log+key.char
    def start(self):
        self.thread = threading.Thread(target=self.start_listener)
        self.thread.daemon = True
        self.thread.start()
    def is_user_accepted(self,accept_string) -> bool:
        return self.log.is_keyword_matching_end_keyword(accept_string)