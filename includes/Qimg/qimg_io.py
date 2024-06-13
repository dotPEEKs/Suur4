import os
import io
from enum import Enum
from .qimg_errno import *
class SEEK:
    SEEK_SET = 0 
    SEEK_CUR = 1
    SEEK_END = 2
class IO(Traceback):
    """
    Supporting to I/O process to Qimg module it's not reading directly or writing firstly controlling is dir or file if it's file after the type control is it can readable or writable shortly handling file R/W functions to securely
    """
    def __new__(cls,file,mode):
        cls.__fd_mode = "w"
        if not os.path.exists(file):
            return ERRNO.ERRNO_NON_EXISTING_FILE
        elif not os.path.isfile(file):
            return ERRNO.ERRNO_BAD_FILE_TYPE
        else:
            try:
                cls.fd = open(file,mode)
            except ValueError:
                return ERRNO.ERRNO_BAD_FMODE
            except PermissionError:
                return ERRNO.ERRNO_BAD_PERMISSION
            except: # UNDEFINED EXCEPTIONS
                return ERRNO.ERRNO_UNDEFINED_ERROR
            return super(IO,cls).__new__(cls)
    def __init__(self,file,mode):
        self.file = file
        self.mode = mode
        self.r_size = 0
        self.w_size = 0
        self.read_counter = 0 # for seeking 
    def __repr__(self) -> str:
        string = "<%s filename = %s mode = %s " % (self.__class__.__name__,self.file,self.mode)
        string += "type = %s " % ('writable' if self.writable() else 'readable')
        string += "%s = %s " % ('writed' if self.writable() else 'readed',self.w_size if self.writable() else self.r_size)
        string += "file_size = %s " % (os.path.getsize(self.file))
        string += "is_closed = %s >" % (self.is_fd_closed())
        return string

    @staticmethod
    def create_file(filename: str) -> ERRNO or bool:
        try:
            with open(filename,"w"):
                pass
        except PermissionError as perm_error:
            return (ERRNO.ERRNO_BAD_PERMISSION,perm_error)
        return True

    def write(self,content: bytes or str,flush = False) -> ERRNO or bool:
        """
        if content writed succesfully will return True else ERRNO
        if you wanna dont wait writed data at ram you can use flush = True
        """
        if not self.writable():
            return ERRNO.ERRNO_NON_WRITABLE_FILE
        try:
            self.fd.write(content)
            if flush:
                self.fd.flush()
            self.w_size += len(content)
        except TypeError as write_fault:
            return (ERRNO.ERRNO_NON_ALLOWED_CONTENT_TYPE,str(write_fault))
        return True

    def simple_read(self,chunk=None):
        where_i_am = self.fd.tell()
        if where_i_am == os.path.getsize(self.file):
            self.fd.seek(0,SEEK.SEEK_SET)
        try:
            content = self.fd.read(chunk)
            self.r_size += len(content)
            return content
        except QimgException as read_fault:
            return (ERRNO.ERRNO_CANNOT_READ,str(read_fault))

    def read_streamize(self,chunk=None):
        rsize = 0
        cursize = os.path.getsize(self.file)
        while rsize < cursize:
            content = self.simple_read(chunk)
            if not isinstance(content,Enum):
                rsize += len(content)
            else:
                yield content # we generated errno and break the loop
                break
            yield content
    def close(self):
        if self.fd.closed:
            self.fd.close()
            return True
        return False
    def writable(self) -> bool:
        try:
            return self.fd.writable()
        except:
            return False
    def readable(self) -> bool:
        try:
            return self.fd.readable()
        except:
            return False
    def is_fd_closed(self) -> bool:
        return self.fd.closed