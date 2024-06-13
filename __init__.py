import pathlib
import os
DEBUG_NOT_VMWARE = True
def get_assets_data(*args) -> str:
    """
    it's only use while in exe file
    """
    return os.path.join(os.path.expandvars("%LocalAppData%"),*args)
def to_nt_path(path: str) -> str:
    return path.replace("/","\\")
def get_path(*args) -> str:
    global DEBUG_NOT_VMWARE
    path = r"C:\Windows\system32\suura"
    if DEBUG_NOT_VMWARE:
        path = os.path.expandvars("%LocalAppData%")
    """
    standart usage after set-up process
    """
    return os.path.join(path,*args)
def lib_path(*args):
    return os.path.join(os.path.dirname(__file__),*args)
def get_exe_assets(*args):
    return os.path.join(os.path.dirname(pathlib.Path(os.path.dirname(__file__)).resolve()),*args)
def get_dir_path():
    return os.path.dirname(__file__)