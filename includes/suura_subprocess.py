import os
import subprocess
class ProcessType:
    @staticmethod
    def open_hide_process(args: str) -> bool:
        process_startup_info = subprocess.STARTUPINFO()
        process_startup_info.dwFlags = subprocess.HIGH_PRIORITY_CLASS
        process_startup_info.wShowWindow |= subprocess.SW_HIDE
        try:
            proces = subprocess.Popen(args,startupinfo=process_startup_info,creationflags=subprocess.CREATE_NO_WINDOW)
        except Exception:
            return False
        return proces
    @staticmethod
    def open_process(args: str) -> bool:
        """
        if command executed succesfully it will return subprocess class otherwise return false
        """
        try:
            proc = subprocess.Popen(args)
        except:
            return False
        return proc
    @staticmethod
    def system(command: str):
        try:
            os.system(command)
        except Exception as e:
            return False
        return True
class Process:
    def __init__(self):
        self._command = "cmd.exe"
        self._parameter = ""
        self._process_type = ProcessType.open_process
    @property
    def command(self) -> str:
        return self._command
    @command.setter
    def command(self,value: str):
        if isinstance(value,str):
            self._command = value
    @property
    def parameter(self):
        return self._parameter
    @parameter.setter
    def parameter(self,pvalue: str) -> str:
        if isinstance(pvalue,str):
            self._parameter = pvalue
    @property
    def process_type(self):
        return self._process_type
    @process_type.setter
    def process_type(self,ptype_value: type) -> type:
        if ptype_value.__class__.__name__ == "function":
            self._process_type = ptype_value
    def exec(self) -> bool:
        return self._process_type(self.command + " " + self.parameter)
