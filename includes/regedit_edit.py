import winreg
class RegeditEdit:
    def __init__(self,data=None):
        self.tuples = data
    def init(self):
        for sub_tuples in self.tuples:
            if len(sub_tuples) == 5:
                key_path,sub_path,data_name,data_value,data_type = sub_tuples
                try:
                    key_handler = winreg.OpenKey(key_path,sub_path,0,winreg.KEY_SET_VALUE)
                    winreg.SetValueEx(key_handler,data_name,0,data_type,data_value)
                except:
                    pass
