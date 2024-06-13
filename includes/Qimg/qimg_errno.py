# Definations ERRNO for QIMG module
import time

import warnings
from enum import Enum

#__all__ = ["ERRNO","TranslateErrNoToMsg"]
from .qimg_exceptions import QimgException
class ERRNO(Enum):
    # IO UTILS ERRNO 
    ERRNO_BAD_FILE_TYPE = 0X1
    ERRNO_BAD_FMODE = 0X2
    ERRNO_BAD_PERMISSION = 0X3
    ERRNO_BAD_SEEK = 0X4
    ERRNO_NON_READABLE_FILE = 0X5
    ERRNO_NON_WRITABLE_FILE = 0X6
    ERRNO_NON_EXISTING_FILE = 0X7
    ERRNO_NON_ALLOWED_CONTENT_TYPE = 0x8
    ERRNO_CANNOT_READ = 0X9
    ERRNO_UNDEFINED_ERROR = 0X500 # for except blocks and debugging
def TranslateErrNoToMsg(msg: int) -> str:
    errs = {
        ERRNO.ERRNO_BAD_FILE_TYPE:"Verdiğiniz bir parametrenin dosya olmadığına işarettir Örn:Klasör gibi vb.",
        ERRNO.ERRNO_BAD_FMODE:"Desteklenmeyen okuma/yazma modu ",
        ERRNO.ERRNO_BAD_PERMISSION:"İlgili dosyanın yazma veya okuma izninin olmaması",
        ERRNO.ERRNO_BAD_SEEK:"Desteklenmeyen seek numarası ya da ilgili modun verilen seek numarasını desteklememesi",
        ERRNO.ERRNO_NON_READABLE_FILE:"Okunamayan dosya",
        ERRNO.ERRNO_NON_WRITABLE_FILE:"Yazılamayan dosya",
        ERRNO.ERRNO_NON_EXISTING_FILE:"Mevcut olmayan dosya",
        ERRNO.ERRNO_NON_ALLOWED_CONTENT_TYPE:"İzin verilmeyen ya da desteklenmeyen girdi tipi ya da ilgili modun girdi tipini desteklememesi",
        ERRNO.ERRNO_CANNOT_READ:"Okuma işleminde oluşan bir hata",
        ERRNO.ERRNO_UNDEFINED_ERROR:"Programın çökmemesi için ve desteklenmeyen hata tipi"
    }
    return errs.get(msg)
class Traceback:
    def __init__(self,errno = None,exception = None):
        self.errno = errno or ERRNO.ERRNO_UNDEFINED_ERROR
        self.exception = exception or "There is no exception specified"
        self.translated_msg = TranslateErrNoToMsg(errno) or "UNDEFINED ERROR"
    def __repr__(self) -> str:
        return "%s -> %s" % (self.errno,self.translated_msg)
