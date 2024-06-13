import ctypes
import os
from core.utils.msgbox import *

advapi32 = ctypes.WinDLL('advapi32')
kernel32 = ctypes.WinDLL('kernel32')
ntdll = ctypes.windll.ntdll

class LUID(ctypes.Structure):
    _fields_ = [("LowPart", ctypes.c_ulong), ("HighPart", ctypes.c_long)]

class LUID_AND_ATTRIBUTES(ctypes.Structure):
    _fields_ = [("Luid", LUID), ("Attributes", ctypes.c_ulong)]

class TOKEN_PRIVILEGES(ctypes.Structure):
    _fields_ = [("PrivilegeCount", ctypes.c_ulong), ("Privileges", LUID_AND_ATTRIBUTES * 1)]


LookupPrivilegeValue = advapi32.LookupPrivilegeValueW
LookupPrivilegeValue.argtypes = (ctypes.c_void_p, ctypes.c_wchar_p, ctypes.POINTER(LUID))
AdjustTokenPrivileges = advapi32.AdjustTokenPrivileges
AdjustTokenPrivileges.argtypes = (ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(TOKEN_PRIVILEGES), ctypes.c_ulong, ctypes.POINTER(TOKEN_PRIVILEGES), ctypes.POINTER(ctypes.c_ulong))
OpenProcessToken = advapi32.OpenProcessToken
OpenProcessToken.argtypes = (ctypes.c_void_p, ctypes.c_ulong, ctypes.POINTER(ctypes.c_void_p))


SE_PRIVILEGE_ENABLED = 0x00000002
TOKEN_QUERY = 0x0008
TOKEN_ADJUST_PRIVILEGES = 0x0020


def SetPrivilege(privilege_name, enable=True):

    process_handle = kernel32.GetCurrentProcess()


    token_handle = ctypes.c_void_p()
    OpenProcessToken(process_handle, TOKEN_ADJUST_PRIVILEGES | TOKEN_QUERY, ctypes.byref(token_handle))


    luid = LUID()
    LookupPrivilegeValue(None, privilege_name, ctypes.byref(luid))


    new_privileges = TOKEN_PRIVILEGES()
    new_privileges.PrivilegeCount = 1
    new_privileges.Privileges[0].Luid = luid
    if enable:
        new_privileges.Privileges[0].Attributes = SE_PRIVILEGE_ENABLED
    else:
        new_privileges.Privileges[0].Attributes = 0


    AdjustTokenPrivileges(token_handle, False, ctypes.byref(new_privileges), 0, None, None)


    if ctypes.windll.kernel32.GetLastError() != 0:
        print(f"Hata: {ctypes.windll.kernel32.GetLastError()}")
    else:
        print("Ayrıcalık başarıyla ayarlandı.")


def set_as_critic():
    privilege_name = "SeDebugPrivilege"
    SetPrivilege(privilege_name, enable=True)  # Ayrıcalığı etkinleştirme
    ntdll.RtlSetProcessIsCritical(1,0,0)