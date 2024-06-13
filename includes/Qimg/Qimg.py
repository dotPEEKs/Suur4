import os
import binascii as zlib
import time
import hmac
import random
import string
import struct
import base64
import secrets
import warnings
import hashlib
from datetime import datetime # you can use time.mktime 
from .qimg_exceptions import (
    ShortKeyLenghtWarning,
    QimgWarning
)
from Crypto.Cipher import AES
from .qimg_io import (IO,Enum)
from .qimg_errno import TranslateErrNoToMsg
doc = """
NOTE:
1 - Do Not pack your important datas with this tool

2 - I'am not own responsible any data lost or data damages

3 - When packing process finished tool must be generated two file first:.Qkey( real key ) second:.Qslt(Salt file of key ) if you lost this these files you cannot decrypt packed file,so you must be dont lost this file this is your own responsibilities

4 - Every packing process key changing (even if it's the same file) 

5 - Every responsibility is your own not ME
"""
generate_string = lambda:"".join(random.sample(string.ascii_letters,6))
DEBUG_SHOW_WARNING_MSG = False
if DEBUG_SHOW_WARNING_MSG:
    warnings.warn(doc,QimgWarning,stacklevel=2)

class QimgVar:
    # bunlar ise sabit ve her derlemede farklılık göstermeyen değişkenlerdir
    DEFAULT_QIMG_FILE_HEADER = b"Qimg" + b"\xd07" + b"\xd08"
    DEFAULT_QIMG_SALT_FILE_HEADER = b"Qsalt" + b"\xd09" + b"\xd010"
    DEFAULT_QIMG_KEY_FILE_HEADER = b"Qkey" + b"\xd011" + b"\xd012"
    DEFAULT_QIMG_METADATA_SIZE = 221
    DEFAULT_QIMG_FILE_HEADER_SIZE = 321
    DEFAULT_MTIME_EOF_HMAC_HASH_SIZE = -64

class Build:
    # burada değişken veriler var ve bu veriler her buildde her derlemede farklılık içerir bunlar sadece şimdilik test amaçlı sabittir
    DEFAULT_HMAC_KEY_OF_HEADER = b'\xe6\x05\xc5\x9c\xd8,1\xc3\xe6PO\xd7\x17\x9c|\x0c'
    DEFAULT_HMAC_KEY_OF_EOF_MTIMESTAMP = b'\xdfr\x94Q\xd6\x8b\xc3\x96\xfe\x830\ncS\x94\xa9'
    DEFAULT_BUILD_SALT = b'V\xcftF\x12\xe0\x86\xf6\xc7\x8d\xe9Ava\xc7\x1f'
    DEFAULT_BUILD_SECRET_MAGIC_FIELD_LENGTH = random.randint(1,128)
    DEFAULT_READ_CHUNKS = 16800 # 16.8 kb
    DEFAULT_PAD_SIZE = random.randint(1024,2048)
    DEFAULT_PBDKF2_KEY_ITER = random.randint(1500000,2000000)
    DEFAULT_HMAC_KEY_VI_CHECK = b"\rc\xe1AB+\xfe[>S\xe5|\x84\xb0\x9a\xc4\x15\xf2\x91\x90\x14\xa7%\xc1\x14\x868\x8e\xe3x\xa5\x81"

class HMAC:
    """
    veri bütünlüğünü kontrol etmek için kullanılan sınıf.Bununla verilerin bütünlüğü kontrol edilir
    """
    def __new__(cls,key: bytes,msg: bytes) -> bytes:
        hmac_ = hmac.new(key,msg,hashlib.sha512)
        return hmac_.digest()

class PBDKF2:
    """
    PBDKF2 AES için güvenli anahtar türetmek için kullanılır
    """
    def __init__(self,key=b"\x0d"):
        if len(key) < 128:
            warnings.warn("Short key lenght key must be big than 128 your key length: %s" % (len(key)),ShortKeyLenghtWarning,2)
            key = secrets.token_bytes(256)
        self.key = hashlib.pbkdf2_hmac('sha256',key,Build.DEFAULT_BUILD_SALT,Build.DEFAULT_PBDKF2_KEY_ITER)
class AESCrypto:
    """
    Sadece prototip şuan ek olarak güncelleme alacak
    """
    def __init__(self,key: bytes,iv):
        self.key = key
        self.iv = iv
    def encrypt(self,data: bytes) -> bytes:
        aes = AES.new(self.key,AES.MODE_GCM,self.iv)
        try:
            return aes.encrypt(data)
        except:
            return b""
    def decrypt(self,data: bytes):
        aes = AES.new(self.key,AES.MODE_GCM,self.iv)
        try:
            return aes.decrypt(data)
        except:
            return b""

class Keygen:
    def __init__(self):
        self._key = PBDKF2()
        self._salt = secrets.token_bytes(16) # 
        self._pad_size = random.randint(1881,1938)
        self.headers = {
            "QKEY_SOF_HEADER":b"****START OF SECRET KEY QIMG PACKER****\n", #EOF -> END OF FILE SOF START OF FILE
            "QKEY_EOF_HEADER":b"START OF SECRET KEY QIMG PACKER****\n"
        }
        self._total = struct.pack("<Q",self._pad_size) + secrets.token_bytes(self._pad_size) + b""
    @staticmethod
    def obfuscate_key(data: bytes,n: int,c: int):
        start_byte = ord(data[0])
        n_byte_char = chr(start_byte + n)
        c_byte_char = chr(start_byte + ord(n_byte_char))
        return (
            start_byte,
            n_byte_char,
            c_byte_char
        )
class QimgFileHeader:
    """
    Dosyanın başlığını damgalamak için kullanılan sınıftır 

    """
    def __init__(self):
        self.current_timestamp = secrets.token_bytes(4) + struct.pack(">I",int(time.time()))
        self.metadata = b"This File Packed Via Qimg tool do not any change this file or data of file otherwise this be malformed and cannot unpackable you must be have .Qkey and .Qslt files only they are(but correct one) decrypt me"
        self.key = secrets.token_bytes(16)
        self.iv = secrets.token_bytes(16)
        self.use_real_timestamp = True
    @property
    def header(self) -> bytes:
        if not self.use_real_timestamp:
            self.current_timestamp = secrets.token_bytes(4) + struct.pack(">I",int(datetime(random.randint(1970,1986),3,3,3,3,3,3).timestamp()))
        total = QimgVar.DEFAULT_QIMG_FILE_HEADER + self.current_timestamp  + self.meta_data + self.key + self.iv
        total = total + HMAC(Build.DEFAULT_HMAC_KEY_OF_HEADER,total)
        total = total + struct.pack(">I",zlib.crc32(total))
        return total
    @property
    def meta_data(self):
        return self.metadata
    @meta_data.setter
    def meta_data(self,value: bytes):
        if isinstance(value,bytes) and len(value) < QimgVar.DEFAULT_QIMG_METADATA_SIZE:
            pad_size = QimgVar.DEFAULT_QIMG_METADATA_SIZE - len(value)
            value = b"\x00" * pad_size + value if len(value) != QimgVar.DEFAULT_QIMG_METADATA_SIZE else value
            self.metadata = value
    @classmethod
    def header_stamp_to_fd(cls,fd,metadata = None):
        stamper = cls()
        stamper.meta_data = metadata if not metadata is None else None
        fd.write(stamper.header)
        fd.flush()
class QimgFileHeaderAnalyser:
    def __init__(self,data: bytes):
        self.data = data if len(data) == QimgVar.DEFAULT_QIMG_FILE_HEADER_SIZE else data[:QimgVar.DEFAULT_QIMG_FILE_HEADER_SIZE]
    def analyse(self) -> bool:
        if len(self.data) < QimgVar.DEFAULT_QIMG_FILE_HEADER_SIZE:
            return -5 # burayı değiştir 
        elif HMAC(Build.DEFAULT_HMAC_KEY_OF_HEADER,self.data[:40]) != self.data[-64:] and zlib.crc32(self.data[:len(self.data)-4]) != struct.unpack(">I",self.data[-4:])[0]:
            return -4 # burayı da değiştir 
        else:
            timestamp = self.data[len(QimgVar.DEFAULT_QIMG_FILE_HEADER) + 4:len(QimgVar.DEFAULT_QIMG_FILE_HEADER) + 4 * 2]
            metadata = self.data[self.data.index(timestamp) + len(timestamp):QimgVar.DEFAULT_QIMG_METADATA_SIZE]
            return {
                "timestamp":time.ctime(struct.unpack(">I",timestamp)[0]),
                "metadata":metadata
            }
class FileAnalyser:
    def __init__(self,file: str):
        self.timestamp = HMAC(Build.DEFAULT_HMAC_KEY_OF_EOF_MTIMESTAMP,struct.pack(">I",int(os.path.getmtime(file))))
        self.fd = open(file,"rb")
    def get_mtime(self):
        self.fd.seek(QimgVar.DEFAULT_MTIME_EOF_HMAC_HASH_SIZE,os.SEEK_END)
        mtime = self.fd.read()
        self.fd.seek(0,os.SEEK_SET)
        return mtime
    @property
    def is_matching(self):
        return self.get_mtime() == self.timestamp

class Qimg:
    def __init__(self,target=None):
        self.keygen = Keygen()
        self.fd = open("test_out.Qimg","ab+")
    def pack(self):
        QimgFileHeader.header_stamp_to_fd(self.fd)
        for _ in range(1,150):
            self.fd.write(secrets.token_bytes(15))
        self.fd.write(HMAC(Build.DEFAULT_HMAC_KEY_OF_EOF_MTIMESTAMP,struct.pack(">I",int(time.time()))))
        self.fd.close()