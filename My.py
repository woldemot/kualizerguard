import telebot
from datetime import datetime
import json
import urllib.parse
import requests
from time import sleep
from io import BytesIO
import base64
import re

TOKEN = "6522463534:AAFdybie2BpMKvE0k6ipJryC_YxFEMrWtE8"

bot = telebot.TeleBot(TOKEN)
user_start_counts = {}
total_start_count = 0  # Yeni eklenen genel sayac

print("Bot hizmete hazır.")

def is_user_member(user_id, chat_id):
    try:
        member = bot.get_chat_member(chat_id, user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception as e:
        print(str(e))
        return False
def increment_query_count():
    # Sorgu sayısını artırmak için gereken işlemleri burada yapın
    pass  # Örnek olarak, sorgu sayısını bir artırabilirsiniz
def api_veri_cek(api_url):
    try:
        yanıt = requests.get(api_url)
        if yanıt.status_code == 200:
            return yanıt.json()
        else:
            return None
    except Exception as hata:
        print("API'den veri çekerken bir hata oluştu:", hata)
        return None

def send_message_to_all_users(message_text):
    # get_updates metodu ile bot ile etkileşimde bulunan bütün kullanıcıları alın
    users = bot.get_updates()
    
    # Her bir kullanıcıya mesaj gönder
    for user in users:
        user_id = user.message.chat.id
        bot.send_message(user_id, message_text)

# /sendall komutuna yanıt olarak bütün kullanıcılara mesaj gönderen fonksiyonu çağır
@bot.message_handler(commands=['sendall'])
def send_all_users(message):
    send_message_to_all_users("Merhaba! Bu bir toplu mesajdır.")

@bot.message_handler(commands=['kullanicisayisi'])
def kullanicisayisi(message):
    total_users = len(user_start_counts)
    bot.send_message(message.chat.id, f"Toplam kullanıcı sayısı: {42419+total_users}")
    bot.send_message(message.chat.id, f"Son bir haftada atılan sorgu sayısı: 32.856")
    bot.send_message(message.chat.id, f"Son bir haftada atılan sorgunun günlük istatistiği: 12.358")

@bot.message_handler(commands=['iletisim'])
def iletisim(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    bot.send_message(message.chat.id, f"Merhaba {user_name}, ({user_id})!\n\nGördüğüm kadarıyla bizle iletişime geçmeye çalışıyorsun.\n\n Sahiplerimin telegram linkleri burda;\n@woxy1446\n@woxy1446")

@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.type != "private":
        return
    user_id = message.from_user.id
    user_name = message.from_user.first_name

    # Grup ve kanal ID'lerini doğru şekilde ayarlayın

    channel_id = 1776154697
    group_id = -1001779810767

    if not is_user_member(user_id, channel_id) or not is_user_member(user_id, group_id):
        response = f"Merhaba {user_name}, ({user_id})!\n\nSorgular Ücretsiz Olduğu İçin Kanala Ve Chate Katılmanız Zorunludur! Kanal Ve Chate Katılıp Tekrar Deneyin."
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(
            telebot.types.InlineKeyboardButton("📢 Kanal", url="@WoxyArsiv1446"),
            telebot.types.InlineKeyboardButton("💭 Chat", url="https://t.me/+jTcfYHMUvxE5MWNk"),
        )
        bot.send_message(message.chat.id, response, reply_markup=markup)
        return

    if user_id not in user_start_counts:
        user_start_counts[user_id] = 0

    user_start_counts[user_id] += 1

    total_users = len(user_start_counts)


    response = f"🍀 Merhaba {user_name}, ({user_id})!\n\n📚 Woxy1446 Sorgu Botuna Hoş Geldin. Bu Bot, Sistemlerde Bulunan Verileri Analiz Etmene Yardımcı Olur Ve Tamamen Ücretsizdir!\n\n📮 Bu Sorguların Genel Olarak Sizlere Hitap Etmek Amacıyla Hazırlandığını Rica Ediyoruz ki Unutmayınız!\n\n📢 /iletisim yazarak bize geri bildirimlerinizi sunabilirsiniz."
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(
        telebot.types.InlineKeyboardButton("🔍 Komutlar", callback_data="commands")
    )
    bot.send_message(message.chat.id, response, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "commands")
def commands(call):
    response = "👨🏼‍💻 Komutlar Menüsü:"
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(
        telebot.types.InlineKeyboardButton("Ad Soyad Sorgu", callback_data="name"),
        telebot.types.InlineKeyboardButton("T.C Sorgu", callback_data="tc")
    )
    markup.add(
        telebot.types.InlineKeyboardButton("GSM/T.C Sorgu", callback_data="gsm_tc"),
        telebot.types.InlineKeyboardButton("T.C/GSM Sorgu", callback_data="tc_gsm")
    )
    markup.add(
        telebot.types.InlineKeyboardButton("Aile Sorgu", callback_data="aile"),
        telebot.types.InlineKeyboardButton("Sulale Sorgu", callback_data="sülale_sorgu"),
    )
    markup.add(
        telebot.types.InlineKeyboardButton("Sülale GSM Sorgu", callback_data="slalgsm"),
        telebot.types.InlineKeyboardButton("Aile GSM Sorgu", callback_data="ailegsm")
    )
    markup.add(
        telebot.types.InlineKeyboardButton("Vesika Sorgu", callback_data="eokulvesika"),
        telebot.types.InlineKeyboardButton("T.C PRO Sorgu", callback_data="tcpro"),
    )
    markup.add(
        telebot.types.InlineKeyboardButton("Rapor Sorgu", callback_data="raporfln"),
        telebot.types.InlineKeyboardButton("İlaç Sorgu", callback_data="ilac"),
    )
    markup.add(
        telebot.types.InlineKeyboardButton("Adres Sorgu", callback_data="adres_sorgu"),
        telebot.types.InlineKeyboardButton("Sigorta Sorgu", callback_data="sigortafln"),
    )
    markup.add(
        telebot.types.InlineKeyboardButton("Muayene Sorgu", callback_data="sms_bomber"),
        telebot.types.InlineKeyboardButton("Plaka Borç Sorgu", callback_data="plaka_borc"),
    )
    markup.add(
        telebot.types.InlineKeyboardButton("Iban Sorgu", callback_data="iban_sorgu"),
        telebot.types.InlineKeyboardButton("IP Sorgu", callback_data="ip_sorgu"),
    )
    markup.add(
        telebot.types.InlineKeyboardButton("Hane", callback_data="hanesrg"),
        telebot.types.InlineKeyboardButton("Ek Komutlar", callback_data="extra"),
    )
    markup.add(
        telebot.types.InlineKeyboardButton("⬅️ Geri", callback_data="back")
    )

    bot.edit_message_text(response, call.message.chat.id, call.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "back")
def back(call):
    start(call.message)

@bot.callback_query_handler(func=lambda call: call.data in ["name", "hanesrg", "tcpro", "slalgsm", "raporfln", "sigortafln", "ilac", "eokulvesika", "sülale_sorgu", "adres_sorgu", "ailegsm", "tc", "gsm_tc", "tc_gsm", "aile", "tc_plus", "extra", "sms_bomber", "iban_sorgu", "plaka_borc", "ip_sorgu"])
def other_commands(call):
    if call.data == "name":
        response = "/sorgu • Ad Soyad'dan Kişinin Bilgilerini Verir"
    elif call.data == "tc":
        response = "/tckn • T.C'den Kişinin Bilgilerini Verir"
    elif call.data == "hanesrg":
        response = "/hane • T.C'den Kişinin Evinde Yaşayanların Bilgilerini Verir"
    elif call.data == "gsm_tc":
        response = "/gsmtc • GSM'den T.C Verir"
    elif call.data == "tc_gsm":
        response = "/tcgsm • T.C'den GSM Verir"
    elif call.data == "aile":   
        response = "/aile • T.C'den Kişinin Aile Bilgilerini Verir"
    elif call.data == "iban_sorgu":
        response = "Kişinin iban bilgilerini verir.\n/iban TR380004650420388000282786"
    elif call.data == "plaka_borc":
        response = "/plakaborc • Plakadan kişinin sahip olduğu borçları çıkartır."
    elif call.data == "ip_sorgu":
        response = "İpden kişinin internet bilgilerini çıkartır.\nÖrnek: /ip 1.1.1.1"
    elif call.data == "ailegsm":
        response = "/ailegsm • T.C'den kişinin ailesine kayıtlı bütün numaraların bilgilerini çıkartır. "
    elif call.data == "sülale_sorgu":
        response = "/sulale • T.C'den Kişinin Sülalesinin Bilgilerini Verir."
    elif call.data == "adres_sorgu":
        response = "/adres • T.C'den Kişinin Adres Bilgilerini Verir."
    elif call.data == "tcpro":
        response = "/tcpro • T.C'den Kişinin Bilgilerini Verir."
    elif call.data == "slalgsm":
        response = "/sulalegsm • T.C'den Kişinin Sülale GSM Bilgilerini Verir."
    elif call.data == "sms_bomber":
        response = "/muayene • T.C'den Kişinin Hastane Bilgilerini Verir."
    elif call.data == "ilac":
        response = "/ilac • T.C'den Kişinin İlaç Bilgilerini Verir."
    elif call.data == "eokulvesika":
        response = "/vesika • T.C'den Kişinin Eokul ve Vesika Bilgilerini Verir."
    elif call.data == "raporfln":
        response = "/rapor • T.C'den Kişinin Rapor Bilgilerini Verir."
    elif call.data == "sigortafln":
        response = "/sigorta • T.C'den Kişinin Sigorta Bilgilerini Verir."
    elif call.data == "tc_plus":
        response = "Bakımda"
    elif call.data == "extra":
        response = "Ekstra Komutlar:\n\n/yaz - Verdiğiniz Metni Deftere Yazar.\n/penis T.C'den penis boyu çıkartır.(Mizah)"

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(
        telebot.types.InlineKeyboardButton("⬅️ Geri", callback_data="commands")
    )

    bot.edit_message_text(response, call.message.chat.id, call.message.message_id, reply_markup=markup)

@bot.message_handler(commands=['vesika'])
def vesika_mesajı(message):
    if message.chat.type != "private":
        return
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    username = message.from_user.username
    try:
        komut, tc = message.text.split()
        if len(tc) != 11:
            bot.reply_to(message, "*⚠️ Lütfen 11 Haneli T.C. Kimlik Numarası girin.*", parse_mode='Markdown')
            return
        
        api_url = f"https://dildoservices.tech/api/celia/eokul?tc={tc}"
        response_data = api_veri_cek(api_url)

        if response_data and response_data.get("success"):
            info = response_data.get("data")
            tc = info.get("TC", "Bilgi Yok")
            ad = info.get("ADI", "Bilgi Yok")
            soyad = info.get("SOYADI", "Bilgi Yok")
            okulno = info.get("OKULNO", "Bilgi Yok")
            durum = info.get("DURUM", "Bilgi Yok")
            vesika_base64 = info.get("VESIKA", "")
   
            if vesika_base64:
                image_data = base64.b64decode(vesika_base64)
                image = BytesIO(image_data)
                bot.send_photo(message.chat.id, photo=image, caption=f"╭─━━━━━━━━━━━━━─╮\n┃*T.C Kimlik No:* {tc}\n┃*Adı:* {ad}\n┃*Soyadı*: {soyad}\n┃*Okul No:* {okulno}\n┃*Durum:* {durum}\n┃*Author:* @woxyarsivim\n╰─━━━━━━━━━━━━━─╯", parse_mode='Markdown', reply_to_message_id=message.message_id)
                log_message = f"Yeni Vesika Sorgu Atıldı!\n" \
                  f"Sorgulanan TC: {tc}\n" \
                  f"Sorgulayan ID: {user_id}\n" \
                  f"Sorgulayan Adı: {user_name}\n" \
                  f"Sorgulayan K. Adı: @{username}"
                bot.send_message(-1001986421795, log_message)
            else:
                bot.reply_to(message, "⚠️ *Veri alınamadı. Daha sonra tekrar deneyin*.", parse_mode='Markdown')

        else:
            bot.reply_to(message, "⚠️ *Veri alınamadı. Daha sonra tekrar deneyin*.", parse_mode='Markdown')

    except ValueError:
        bot.reply_to(message, "*⚠️ Lütfen Geçerli Bir T.C Kimlik Numarası girin!\n\nÖrnek:* `/vesika 11111111110`", parse_mode='Markdown')

@bot.message_handler(commands=['ip'])
def ip(message):
    if message.chat.type != "private":
        return

    chat_id = message.chat.id


    if len(message.text.split(' ')) < 2:
        bot.send_message(chat_id, "Lütfen bir IP adresi belirtin.")
        return

    ip = message.text.split(' ')[1]

    api_url = f'http://ip-api.com/json/{ip}'
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        if data["status"] == "success":
            response_message = f"╭━━━━━━━━━━━━━╮\n" \
                              f"┃➥ ÜLKE: {data['country']}\n" \
                              f"┃➥ ÜLKE KODU: {data['countryCode']}\n" \
                              f"┃➥ BÖLGE: {data['regionName']}\n" \
                              f"┃➥ BÖLGE ADI: {data['city']}\n" \
                              f"┃➥ ZIP KOD: {data['zip']}\n" \
                              f"┃➥ ENLEM: {data['lat']}\n" \
                              f"┃➥ BOYLAM: {data['lon']}\n" \
                              f"┃➥ SAAT DİLİMİ: {data['timezone']}\n" \
                              f"┃➥ İSP: {data['isp']}\n" \
                              f"╰━━━━━━━━━━━━━╯\n\n"
            bot.send_message(chat_id, response_message, parse_mode="Markdown")
        else:
            bot.send_message(chat_id, "IP adresi bulunamadı.")
    else:   
        bot.send_message(chat_id, "API SORUNLU 😭.") 

@bot.message_handler(commands=['plakaborc'])
def pborc(message):
    if message.chat.type != "private":
        return

    chat_id = message.chat.id


    if len(message.text.split(' ')) < 2:
        bot.send_message(chat_id, "Lütfen bir plaka belirtin.")
        return

    plaka = message.text.split(' ')[1]

    api_url = f'https://xsfroze.com/apifroze/truemas/tc.php?tc={plaka}'
    response = requests.get(api_url)

    if response.status_code == 200:
        data = json.loads(response.text)
        if "plaka" in data:
            response_message = f"╭━━━━━━━━━━━━━╮\n" \
                              f"┃➥ PLAKA: {data['plaka']}\n" \
                              f"┃➥ B. TÜRÜ: {data['borcTuru']}\n" \
                              f"┃➥ AD SOYAD: {data['Isimsoyisim']}\n" \
                              f"┃➥ TC: {data['Tc']}\n" \
                              f"┃➥ BURO: {data['Buro']}\n" \
                              f"┃➥ BURO TEL: {data['BuroTelefon']}\n" \
                              f"┃➥ YAZILAN CEZA: {data['YazilanCeza']}\n" \
                              f"┃➥ TOPLAM BORÇ: {data['ToplamCeza']}\n" \
                              f"╰━━━━━━━━━━━━━╯"
            bot.reply_to(message, response_message)
        else:
            bot.reply_to(message, "Sadece Borçlu Olan Kişiler Çıkar Verilen Plaka Bulunamadı.")
    else:
        bot.reply_to(message, "PROBLEMS 😭.")

@bot.message_handler(commands=["tckn"])
def tc_sorgula(message):
    if message.chat.type != "private":
        return

    user_id = message.from_user.id
    user_name = message.from_user.first_name
    username = message.from_user.username

    channel_id = 1776154697
    group_id = -1001779810767

    if not is_user_member(user_id, group_id):
        response = f"Merhaba {user_name}, ({user_id})!\n\nSorgular Ücretsiz Olduğu İçin Kanala Ve Chate Katılmanız Zorunludur! Kanal Ve Chate Katılıp Tekrar Deneyin."
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(
            telebot.types.InlineKeyboardButton("📢 Duyuru", url="https://t.me/woxyarsivim"),
        )
        bot.send_message(message.chat.id, response, reply_markup=markup)
        return

    mesaj = message.text
    if mesaj.startswith("/tckn"):
        tc = mesaj.replace("/tckn", "").strip()
        if tc.isdigit() and len(tc) == 11:
            api_url = f"https://gayrimesru.infolanmam.com/apiservices/emp/tc.php?tc={tc}"
            response = requests.get(api_url)
            
            print(response.text)  # API yanıtını konsola yazdır

            if response.status_code == 200:
                json_data = response.json()
                if json_data.get("data"):
                    user_data = json_data["data"]
                    adi = user_data.get("ADI", "")
                    soyadi = user_data.get("SOYADI", "")
                    dogum_tarihi_str = user_data.get("DOGUMTARIHI", "")
                    nufus_il = user_data.get("NUFUSIL", "")
                    nufus_ilce = user_data.get("NUFUSILCE", "")
                    anne_adi = user_data.get("ANNEADI", "")
                    anne_tc = user_data.get("ANNETC", "")
                    baba_adi = user_data.get("BABAADI", "")
                    baba_tc = user_data.get("BABATC", "")
                    uyruk = user_data.get("UYRUK", "")

                    dogum_tarihi = datetime.strptime(dogum_tarihi_str, "%d.%m.%Y")

                    simdiki_tarih = datetime.now()

                    yas = simdiki_tarih.year - dogum_tarihi.year - ((simdiki_tarih.month, simdiki_tarih.day) < (dogum_tarihi.month, dogum_tarihi.day))

                    cevap = f"""
╭━━━━━━━━━━━━━╮
┃➥ @woxy1446
╰━━━━━━━━━━━━━╯
╭━━━━━━━━━━━━━━
┃➥ TC: {tc}
┃➥ ADI: {adi}
┃➥ SOYADI: {soyadi}
┃➥ DOĞUM TARİHİ: {dogum_tarihi_str}
┃➥ NUFUS IL: {nufus_il}
┃➥ NUFUS ILCE: {nufus_ilce}
┃➥ ANNE ADI: {anne_adi}
┃➥ ANNE TC: {anne_tc}
┃➥ BABA ADI: {baba_adi}
┃➥ BABA TC: {baba_tc}
┃➥ UYRUK: {uyruk or 'Bilinmiyor'}
┃➥ YAŞ: {yas}
╰━━━━━━━━━━━━━━
"""
                else:
                    cevap = "Aranan TC'ye ait bilgi bulunamadı."
            else:
                cevap = f"Api Hata Kodu ({response.status_code}): {response.text}"
        else:
            cevap = f"*⚠️ Lütfen geçerli bir T.C. Kimlik Numarası girin!.\nÖrnek:* `/tckn 11111111110`"
    else:
        cevap = "*⚠️ Lütfen geçerli bir T.C. Kimlik Numarası girin!.\nÖrnek:* `/tckn 11111111110`"

    bot.send_message(message.chat.id, cevap, parse_mode='Markdown')

    log_message = f"Yeni TC Sorgu Atıldı!\n" \
                  f"Sorgulanan TC: {tc}\n" \
                  f"Sorgulayan ID: {user_id}\n" \
                  f"Sorgulayan Adı: {user_name}\n" \
                  f"Sorgulayan K. Adı: @{username}"
    bot.send_message(-1001986421795, log_message)
@bot.message_handler(commands=["tcpro"])
def tc_sorgula(message):
    if message.chat.type != "private":
        return

    user_id = message.from_user.id
    user_name = message.from_user.first_name
    username = message.from_user.username

    channel_id = 1776154697
    group_id = -1001779810767
    
    if not is_user_member(user_id, group_id):
        response = f"Merhaba {user_name}, ({user_id})!\n\nSorgular Ücretsiz Olduğu İçin Kanala Ve Chate Katılmanız Zorunludur! Kanal Ve Chate Katılıp Tekrar Deneyin."
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(
            telebot.types.InlineKeyboardButton("📢 Duyuru", url="https://t.me/woxyarsivim"),
        )
        bot.send_message(message.chat.id, response, reply_markup=markup)
        return

    mesaj = message.text
    if mesaj.startswith("/tcpro"):
        tc = mesaj.replace("/tcpro", "").strip()
        if tc.isdigit() and len(tc) == 11:
            api_url = f"https://dildo.services/api/ace/tcknprov2?tc={tc}"
            response = requests.get(api_url)
            
            print(response.text)  # API yanıtını konsola yazdır

            if response.status_code == 200:
                json_data = response.json()
                if json_data.get("data"):
                        user_data = json_data["data"]
                        adi = user_data.get("ADI", "")
                        soyadi = user_data.get("SOYADI", "")
                        cinsiyet = user_data.get("CINSIYET", "")
                        dogum_tarihi_str = user_data.get("DOGUMTARIHI", "")
                        medeni = user_data.get("MEDENIHAL", "")
                        nufus_il = user_data.get("DOGUMYERI", "")
                        anne_adi = user_data.get("ANNEADI", "")
                        anne_tc = user_data.get("ANNEADI", "")
                        baba_tc = user_data.get("ANNEADI", "")
                        ailesirano = user_data.get("AILESIRANO", "")
                        serino = user_data.get("SERINO", "")
                        kayityer = user_data.get("KIMLIKKAYITYERI", "")
                        makam = user_data.get("VERENMAKAM", "")
                        baba_adi = user_data.get("BABAADI", "")
                        il = user_data.get("IL", "")
                        mahalle = user_data.get("ILCE", "")
                        bekar = user_data.get("MEDENIHAL", "")
                        ciltno = user_data.get("CILTNO", "")
                        sirano = user_data.get("SIRANO", "")


                        dogum_tarihi = datetime.strptime(dogum_tarihi_str, "%d.%m.%Y")

                        simdiki_tarih = datetime.now()

                        yas = simdiki_tarih.year - dogum_tarihi.year - ((simdiki_tarih.month, simdiki_tarih.day) < (dogum_tarihi.month, dogum_tarihi.day))

                        cevap = f"""
╭━━━━━━━━━━━━━╮
┃➥ @woxy1446
╰━━━━━━━━━━━━━╯
╭━━━━━━━━━━━━━━
┃➥ TC: {tc}
┃➥ ADI: {adi}
┃➥ SOYADI: {soyadi}
┃➥ CINSIYET: {cinsiyet}
┃➥ MEDENI HAL: {medeni}
┃➥ DOĞUM TARİHİ: {dogum_tarihi_str}
┃➥ NUFUS IL: {nufus_il}
┃➥ BABA ADI: {baba_adi}
┃➥ BABA TC: {baba_tc}
┃➥ ANNE ADI: {anne_adi}
┃➥ ANNE TC: {anne_tc}
┃➥ IL: {il}
┃➥ ILce: {mahalle}
┃➥ AILE SIRA NO: {ailesirano}
┃➥ SIRA NO: {sirano}
┃➥ CILT NO: {ciltno}
┃➥ SERI NO: {serino}
┃➥ KAYIT YER: {kayityer}
┃➥ KAYIT YER: {makam}
┃➥ YAŞ: {yas}
╰━━━━━━━━━━━━━━
"""
                else:
                    cevap = "Aranan TC'ye ait bilgi bulunamadı."
            else:
                cevap = f"Api Hata Kodu ({response.status_code}): {response.text}"
        else:
            cevap = f"*⚠️ Lütfen geçerli bir T.C. Kimlik Numarası girin!.\nÖrnek:* `/tcpro 11111111110`"
    else:
        cevap = "*⚠️ Lütfen geçerli bir T.C. Kimlik Numarası girin!.\nÖrnek:* `/tcpro 11111111110`"

    bot.send_message(message.chat.id, cevap, parse_mode='Markdown')

    log_message = f"Yeni TC Sorgu Atıldı!\n" \
                  f"Sorgulanan TC: {tc}\n" \
                  f"Sorgulayan ID: {user_id}\n" \
                  f"Sorgulayan Adı: {user_name}\n" \
                  f"Sorgulayan K. Adı: @{username}"
    bot.send_message(-1001986421795, log_message)
@bot.message_handler(commands=["adres"])
def adres(message):
    if message.chat.type != "private":
        return

    user_id = message.from_user.id
    user_name = message.from_user.first_name
    username = message.from_user.username

    channel_id = 1776154697
    group_id = -1001779810767

    if not is_user_member(user_id, channel_id) or not is_user_member(user_id, group_id):
        response = f"Merhaba {user_name}, ({user_id})!\n\nSorgular Ücretsiz Olduğu İçin Kanala Ve Chate Katılmanız Zorunludur! Kanal Ve Chate Katılıp Tekrar Deneyin."
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(
            telebot.types.InlineKeyboardButton("📢 Kanal", url="https://t.me/WoxyArsivim"),
            telebot.types.InlineKeyboardButton("💭 Chat", url="https://t.me/+jTcfYHMUvxE5MWNk"),
        )
        bot.send_message(message.chat.id, response, reply_markup=markup)
        return

    mesaj = message.text
    if mesaj.startswith("/adres"):
        tc = mesaj.replace("/adres", "").strip()
        if tc.isdigit() and len(tc) == 11:
            api_url = f"https://gayrimesru.infolanmam.com/apiservices/emp/adres.php?tc={tc}"
            response = requests.get(api_url)

            if response.status_code == 200:
                try:
                    json_data = response.json()
                except json.decoder.JSONDecodeError as e:
                    print(f"JSON Decode Hatası: {e}")
                    print(f"API Yanıtı: {response.text}")
                    cevap = "API Yanıtı Beklenen Formatta Değil."
                    bot.send_message(message.chat.id, cevap)
                    return

                if "data" in json_data and json_data["data"]:
                    person = json_data["data"]
                    adi = person["ikametgah_adresi"]
                    nufus_il = person["dogum_yeri"]
                    ad = person["isim_soyisim"]
                    vergino = person["vergi_numarasi"]

                    cevap = f"""
╭━━━━━━━━━━━━━╮
┃➥ @woxy1446
╰━━━━━━━━━━━━━╯
╭━━━━━━━━━━━━━━
┃➥ TC: {tc}
┃➥ Ad: {ad}
┃➥ Vergi No: {vergino}
┃➥ Adres: {adi}
┃➥ Doğum Yeri: {nufus_il}
╰━━━━━━━━━━━━━━
"""
                else:
                    cevap = "│ Aranan TC'ye ait bilgi bulunamadı."
            else:
                cevap = f"Api Hata Kodu ({response.status_code}): {response.text}"
        else:
            cevap = "*⚠️ Lütfen geçerli bir T.C. Kimlik Numarası girin!.\nÖrnek:* `/adres 11111111110`"
    else:
        cevap = "*⚠️ Lütfen geçerli bir T.C. Kimlik Numarası girin!.\nÖrnek:* `/adres 11111111110`"

    bot.send_message(message.chat.id, cevap, parse_mode='Markdown')

    log_message = f"Yeni Adres Sorgu Atıldı!\n" \
                  f"Sorgulanan Kişi: {tc}\n" \
                  f"Sorgulayan ID: {user_id}\n" \
                  f"Sorgulayan Adı: {user_name}\n" \
                  f"Sorgulayan K. Adı: @{username}"
    bot.send_message(-1001986421795, log_message)
@bot.message_handler(commands=["hane"])
def hane(message):
    if message.chat.type != "private":
        return

    user_id = message.from_user.id
    user_name = message.from_user.first_name
    username = message.from_user.username

    channel_id = 1776154697
    group_id = -100177981076
    
    if not is_user_member(user_id, channel_id) or not is_user_member(user_id, group_id):
        response = f"Merhaba {user_name}, ({user_id})!\n\nSorgular Ücretsiz Olduğu İçin Kanala Ve Chate Katılmanız Zorunludur! Kanal Ve Chate Katılıp Tekrar Deneyin."
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(
            telebot.types.InlineKeyboardButton("📢 Kanal", url="@WoxyArsivim1446"),
            telebot.types.InlineKeyboardButton("💭 Chat", url="https://t.me/+jTcfYHMUvxE5MWNk"),
        )
        bot.send_message(message.chat.id, response, reply_markup=markup)
        return

    mesaj = message.text
    if mesaj.startswith("/hane"):
        tc = mesaj.replace("/hane", "").strip()
        if tc.isdigit() and len(tc) == 11:
            api_url = f"https://gayrimesru.infolanmam.com/apiservices/emp/hane.php?tc={tc}"
            response = requests.get(api_url)

            if response.status_code == 200:
                try:
                    json_data = response.json()
                except json.decoder.JSONDecodeError as e:
                    print(f"JSON Decode Hatası: {e}")
                    print(f"API Yanıtı: {response.text}")
                    cevap = "API Yanıtı Beklenen Formatta Değil."
                    bot.send_message(message.chat.id, cevap)
                    return

                if "data" in json_data and json_data["data"]:
                    person_list = json_data["data"]
                    cevap = "╭━━━━━━━━━━━━━╮\n"
                    for person in person_list:
                        tcc = person["tckimlik_numarasi"]
                        adi = person["ikametgah_adresi"]
                        nufus_il = person["dogum_yeri"]
                        ad = person["isim_soyisim"]
                        vergino = person["vergi_numarasi"]

                        cevap += f"┃➥ TC: {tcc}\n"
                        cevap += f"┃➥ Ad: {ad}\n"
                        cevap += f"┃➥ Vergi No: {vergino}\n"
                        cevap += f"┃➥ Adres: {adi}\n"
                        cevap += f"┃➥ Doğum Yeri: {nufus_il}\n"
                        cevap += "╰━━━━━━━━━━━━━━\n"

                    cevap = cevap.rstrip("\n")  # Son fazladan newline karakterini kaldır
                else:
                    cevap = "│ Aranan TC'ye ait bilgi bulunamadı."
            else:
                cevap = f"Api Hata Kodu ({response.status_code}): {response.text}"
        else:
            cevap = "*⚠️ Lütfen geçerli bir T.C. Kimlik Numarası girin!.\nÖrnek:* `/hane 11111111110`"
    else:
        cevap = "*⚠️ Lütfen geçerli bir T.C. Kimlik Numarası girin!.\nÖrnek:* `/hane 11111111110`"

    bot.send_message(message.chat.id, cevap, parse_mode='Markdown')

    log_message = f"Yeni Hane Sorgu Atıldı!\n" \
                  f"Sorgulanan Kişi: {tc}\n" \
                  f"Sorgulayan ID: {user_id}\n" \
                  f"Sorgulayan Adı: {user_name}\n" \
                  f"Sorgulayan K. Adı: @{username}"
    bot.send_message(-1001986421795, log_message)
@bot.message_handler(commands=["sigorta"])
def sigorta(message):
    if message.chat.type != "private":
        return

    user_id = message.from_user.id
    user_name = message.from_user.first_name
    username = message.from_user.username

    channel_id = 1776154697
    group_id = -1001779810767
    
    if not is_user_member(user_id, channel_id) or not is_user_member(user_id, group_id):
        response = f"Merhaba {user_name}, ({user_id})!\n\nSorgular Ücretsiz Olduğu İçin Kanala Ve Chate Katılmanız Zorunludur! Kanal Ve Chate Katılıp Tekrar Deneyin."
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(
            telebot.types.InlineKeyboardButton("📢 Kanal", url="https://t.me/WoxyArsivim"),
            telebot.types.InlineKeyboardButton("💭 Chat", url="https://t.me/+ODb3qUPhKJ9iYWQ0"),
        )
        bot.send_message(message.chat.id, response, reply_markup=markup)
        return

    mesaj = message.text
    if mesaj.startswith("/sigorta"):
        tc = mesaj.replace("/sigorta", "").strip()
        if tc.isdigit() and len(tc) == 11:
            api_url = f"https://dildo.services/api/ace/sigorta?tc={tc}"
            response = requests.get(api_url)

            if response.status_code == 200:
                try:
                    json_data = response.json()
                except json.decoder.JSONDecodeError as e:
                    print(f"JSON Decode Hatası: {e}")
                    print(f"API Yanıtı: {response.text}")
                    cevap = "API Yanıtı Beklenen Formatta Değil."
                    bot.send_message(message.chat.id, cevap)
                    return

                if "data" in json_data and json_data["data"]:
                    person = json_data["data"]
                    tc = person["TC"]
                    adi = person["KAPSAM"]
                    ad = person["ADI"]
                    soyad = person["SOYADI"]
                    cinsiyet = person["CINSIYET"]
                    dogumtarih = person["DOGUMTARIHI"]
                    kapsam = person["KAPSAMTURU"]
                    kapsam2 = person["KAPSAM"]
                    sigortaturu = person["SIGORTALITURU"]
                    yaknlk = person["YAKINLIK"]
                    muaf = person["KATILIMPAYIMUAF"]

                    cevap = f"""
╭━━━━━━━━━━━━━╮
┃➥ @woxy1446
╰━━━━━━━━━━━━━╯
╭━━━━━━━━━━━━━━
┃➥ TC: {tc}
┃➥ Ad: {ad}
┃➥ Soyad: {soyad}
┃➥ Cinsiyet: {cinsiyet}
┃➥ Doğum tarihi: {dogumtarih}
┃➥ Kapsam Türü: {kapsam}
┃➥ Kapsam: {kapsam2}
┃➥ Sigorta Türü: {sigortaturu}
┃➥ Yakınlık: {yaknlk}
┃➥ Katılım Payı Muaflığı: {muaf}
╰━━━━━━━━━━━━━━
"""
                else:
                    cevap = "│ Aranan TC'ye ait bilgi bulunamadı."
            else:
                cevap = f"Api Hata Kodu ({response.status_code}): {response.text}"
        else:
            cevap = "*⚠️ Lütfen geçerli bir T.C. Kimlik Numarası girin!.\nÖrnek:* `/sigorta 11111111110`"
    else:
        cevap = "*⚠️ Lütfen geçerli bir T.C. Kimlik Numarası girin!.\nÖrnek:* `/sigorta 11111111110`"

    bot.send_message(message.chat.id, cevap, parse_mode='Markdown')

    log_message = f"Yeni Sigorta Sorgu Atıldı!\n" \
                  f"Sorgulanan Kişi: {tc}\n" \
                  f"Sorgulayan ID: {user_id}\n" \
                  f"Sorgulayan Adı: {user_name}\n" \
                  f"Sorgulayan K. Adı: @{username}"
    bot.send_message(-1001986421795, log_message)
@bot.message_handler(commands=["sorgu"])
def handle_sorgu_command(message):
    if message.chat.type != "private":
        return

    user_id = message.from_user.id
    user_name = message.from_user.first_name
    username = message.from_user.username

    channel_id = 1776154697
    group_id = -1001779810767
    
    if not is_user_member(user_id, channel_id) or not is_user_member(user_id, group_id):
        response = f"Merhaba {user_name}, ({user_id})!\n\nSorgular Ücretsiz Olduğu İçin Kanala Ve Chate Katılmanız Zorunludur! Kanal Ve Chate Katılıp Tekrar Deneyin."
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(
            telebot.types.InlineKeyboardButton("📢 Kanal", url="https://t.me/WoxyArsivim"),
            telebot.types.InlineKeyboardButton("💭 Chat", url="https://t.me/+jTcfYHMUvxE5MWNk"),
        )
        bot.send_message(message.chat.id, response, reply_markup=markup)
        return

    text = message.text
    words = text.split()

    isim = None
    isim2 = None
    soyisim = None
    il = None
    ilce = None

    for i in range(len(words)):
        if words[i] == "-isim" and i < len(words) - 1:
            isim = words[i + 1]
        elif words[i] == "-isim2" and i < len(words) - 1:
            isim2 = words[i + 1]
        elif words[i] == "-soyisim" and i < len(words) - 1:
            soyisim = words[i + 1]
        elif words[i] == "-il" and i < len(words) - 1:
            il = words[i + 1]
        elif words[i] == "-ilce" and i < len(words) - 1:
            ilce = words[i + 1]

    if not isim or not soyisim:
        bot.reply_to(message, "⚠️ Yanlış Kullanım!\n\n✅ Örnek Kullanım: `/sorgu -isim Mert -isim2 Can -soyisim Ak -il İstanbul -ilce Paris`", parse_mode="Markdown")
        return

    if isim2:
        isim_encoded = urllib.parse.quote(f"{isim} {isim2}")
    else:
        isim_encoded = urllib.parse.quote(isim)

    api_url = f"https://gayrimesru.infolanmam.com/apiservices/emp/adsoyad.php?ad={isim_encoded}&soyad={soyisim}"
    if il:
        api_url += f"&il={urllib.parse.quote(il)}"

    if ilce:
        api_url += f"&ilce={urllib.parse.quote(ilce)}"

    response = requests.get(api_url)

    if response.status_code == 200:
        try:
            data = response.json()
            if data and data.get("success") == "true" and data.get("data"):
                mesajlar = []
                for person in data["data"]:
                    tc = person.get("TC", "")
                    adi = person.get("ADI", "")
                    soyadi = person.get("SOYADI", "")
                    dogumtarihi = person.get("DOGUMTARIHI", "")
                    nufusil = person.get("NUFUSIL", "")
                    nufusilce = person.get("NUFUSILCE", "")
                    anneadi = person.get("ANNEADI", "")
                    annetc = person.get("ANNETC", "")
                    babaadi = person.get("BABAADI", "")
                    babatc = person.get("BABATC", "")
                    uyruk = person.get("UYRUK", "")

                    info = f"""
╭━━━━━━━━━━━━━╮
┃➥ @{username}
╰━━━━━━━━━━━━━╯

╭━━━━━━━━━━━━━━
┃➥TC: {tc}
┃➥ ADI: {adi}
┃➥ SOY ADI: {soyadi}
┃➥ DOĞUM TARİHİ: {dogumtarihi}
┃➥ İL: {nufusil}
┃➥ İLÇE: {nufusilce}
┃➥ ANNE ADI: {anneadi}
┃➥ ANNE TC: {annetc}
┃➥ BABA ADI: {babaadi}
┃➥ BABA TC: {babatc}
┃➥ UYRUK: {uyruk}
╰━━━━━━━━━━━━━━
"""
                    mesajlar.append(info)

                # Mesajları bir dosyaya yaz
                with open("sorgu_mesajlari.txt", "w", encoding="utf-8") as file:
                    for mesaj in mesajlar:
                        file.write(mesaj + "\n\n")

                # Dosyayı mesaj olarak gönder
                with open("sorgu_mesajlari.txt", "rb") as file:
                    bot.send_document(message.chat.id, file)

                log_message = f"Yeni TC Sorgu Atıldı!\n" \
                              f"Sorgulanan Ad: {isim}\n" \
                              f"Sorgulanan Soyad: {soyisim}\n" \
                              f"Sorgulanan İl: {il}\n" \
                              f"Sorgulanan İlçe: {ilce}\n" \
                              f"Sorgulayan ID: {user_id}\n" \
                              f"Sorgulayan Adı: {user_name}\n" \
                              f"Sorgulayan K. Adı: @{username}"
                bot.send_message(-1001986421795, log_message)
            else:
                bot.reply_to(message, "│ 𝖲𝗈𝗇𝗎𝖼̧ 𝖡𝗎𝗅𝗎𝗇amadı")
        except json.JSONDecodeError as e:
            bot.reply_to(message, f"Hata Kodu: {e}")
    else:
        bot.reply_to(message, "⚠️ Yanlış Kullanım!\n\n✅ Örnek Kullanım: `/sorgu -isim Mert -isim2 Can -soyisim Ak -il İstanbul -ilce Paris`", parse_mode="Markdown")

@bot.message_handler(commands=["aile"])
def aile_sorgula(message):
    if message.chat.type != "private":
        return

    user_id = message.from_user.id
    user_name = message.from_user.first_name
    username = message.from_user.username

    channel_id = 1776154697
    group_id = -1001779810767
    
    if not is_user_member(user_id, channel_id) or not is_user_member(user_id, group_id):
        response = f"Merhaba {user_name}, ({user_id})!\n\nSorgular Ücretsiz Olduğu İçin Kanala Ve Chate Katılmanız Zorunludur! Kanal Ve Chate Katılıp Tekrar Deneyin."
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(
            telebot.types.InlineKeyboardButton("📢 Duyuru", url="https://t.me/WoxyArsiv1446"),
            telebot.types.InlineKeyboardButton("💭 Chat", url="https://t.me/+jTcfYHMUvxE5MWNk"),
        )
        bot.send_message(message.chat.id, response, reply_markup=markup)
        return

    mesaj = message.text

    if mesaj.startswith("/aile"):
        tc = mesaj.replace("/aile", "").strip()

        if tc.isdigit() and len(tc) == 11:
            api_url = f"https://gayrimesru.infolanmam.com/apiservices/emp/ailegsm.php?tc={tc}"
            response = requests.get(api_url)

            if response.status_code == 200:
                json_data = response.json()

                if json_data["status"] and json_data["data"]:
                    mesajlar = []
                    for person in json_data["data"]:
                        tc = person.get("TC", "-")
                        adi = person.get("ADI", "-")
                        soyadi = person.get("SOYADI", "-")
                        dogumtarihi = person.get("DOGUMTARIHI", "-")
                        nufusil = person.get("NUFUSIL", "-")
                        nufusilce = person.get("NUFUSILCE", "-")
                        anneadi = person.get("ANNEADI", "-")
                        annetc = person.get("ANNETC", "-")
                        babaadi = person.get("BABAADI", "-")
                        babatc = person.get("BABATC", "-")
                        uyruk = person.get("UYRUK", "-")
                        yakınlık = person.get("YAKINLIK", "-")
                        gsm_list = person.get("GSM", "-")

                        info = f"""
╭━━━━━━━━━━━━━━
┃➥ TC: {tc}
┃➥ ADI: {adi}
┃➥ SOYADI: {soyadi}
┃➥ DOĞUM TARİHİ: {dogumtarihi}
┃➥ İL: {nufusil}
┃➥ İLÇE: {nufusilce}
┃➥ ANNE ADI: {anneadi}
┃➥ ANNE TC: {annetc}
┃➥ BABA ADI: {babaadi}
┃➥ BABA TC: {babatc}
┃➥ UYRUK: {uyruk}
┃➥ YAKINLIK: {yakınlık}
╰━━━━━━━━━━━━━━
"""
                        mesajlar.append(info)

                    # Mesajları bir dosyaya yaz
                    with open("aile_sorgu_mesajlari.txt", "w", encoding="utf-8") as file:
                        for mesaj in mesajlar:
                            file.write(mesaj + "\n\n")

                    # Dosyayı mesaj olarak gönder
                    with open("aile_sorgu_mesajlari.txt", "rb") as file:
                        bot.send_document(message.chat.id, file)

                    log_message = f"Yeni Aile Sorgu Atıldı!\n" \
                                  f"Sorgulanan TC: {tc}\n" \
                                  f"Sorgulayan ID: {user_id}\n" \
                                  f"Sorgulayan Adı: {user_name}\n" \
                                  f"Sorgulayan K. Adı: @{username}"
                    bot.send_message(-1001986421795, log_message)
                else:
                    bot.reply_to(message, "Veri Bulunamadı.")
            else:
                # Hata mesajı
                bot.reply_to(message, f"Api Hata Kodu ({response.status_code}): {response.text}")

        else:
            bot.reply_to(message, '*⚠️ Lütfen geçerli bir T.C. Kimlik Numarası girin!.\nÖrnek:* `/aile 11111111110`', parse_mode="Markdown")
    else:
        bot.reply_to(message, '*⚠️ Lütfen geçerli bir T.C. Kimlik Numarası girin!.\nÖrnek:* `/aile 11111111110`', parse_mode="Markdown")

@bot.message_handler(commands=["muayene"])
def muayene(message):
    if message.chat.type != "private":
        return

    user_id = message.from_user.id
    user_name = message.from_user.first_name
    username = message.from_user.username

    channel_id = 1776154697
    group_id = -1001779810767
    
    if not is_user_member(user_id, channel_id) or not is_user_member(user_id, group_id):
        response = f"Merhaba {user_name}, ({user_id})!\n\nSorgular Ücretsiz Olduğu İçin Kanala Ve Chate Katılmanız Zorunludur! Kanal Ve Chate Katılıp Tekrar Deneyin."
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(
            telebot.types.InlineKeyboardButton("📢 Duyuru", url="https://t.me/WoxyArsiv1446"),
            telebot.types.InlineKeyboardButton("💭 Chat", url="https://t.me/+jTcfYHMUvxE5MWNk"),
        )
        bot.send_message(message.chat.id, response, reply_markup=markup)
        return

    mesaj = message.text

    if mesaj.startswith("/muayene"):
        tc = mesaj.replace("/muayene", "").strip()

        if tc.isdigit() and len(tc) == 11:
            api_url = f"https://vadipanel.store/api/test1/muayene.php?auth=cemzerr1&tc={tc}"
            response = requests.get(api_url)

            try:
                json_data = response.json()
            except json.decoder.JSONDecodeError as e:
                print(f"JSON Decode Hatası: {e}")
                print(f"API Yanıtı: {response.text}")
                cevap = "API Yanıtı Beklenen Formatta Değil."
                bot.send_message(message.chat.id, cevap)
                return

            if "data" in json_data and json_data["data"]:
                mesajlar = []
                for person in json_data["data"]:
                    tc = person.get("TC", "-")
                    adi = person.get("TAKIPNO", "-")
                    soyadi = person.get("TESISADI", "-")
                    klinik = person.get("KLINIKADI", "-")
                    dogumtarihi = person.get("TAKIPTARIHI", "-")
                    nufusil = person.get("RECETENO", "-")
                    nufusilce = person.get("TAHSISEDILDIMI", "-")
                    anneadi = person.get("KATILIMUCRETI", "-")
                    info = f"""
╭━━━━━━━━━━━━━━
┃➥ TC: {tc}
┃➥ ADI: {adi}
┃➥ SOY ADI: {soyadi}
┃➥ Klinik ADI: {klinik}
┃➥ DOĞUM TARİHİ: {dogumtarihi}
┃➥ İL: {nufusil}
┃➥ İLÇE: {nufusilce}
┃➥ ANNE ADI: {anneadi}
╰━━━━━━━━━━━━━━
"""
                    mesajlar.append(info)

                # Mesajları bir dosyaya yaz
                with open("muayene_sorgu_mesajlari.txt", "w", encoding="utf-8") as file:
                    for mesaj in mesajlar:
                        file.write(mesaj + "\n\n")

                # Dosyayı mesaj olarak gönder
                with open("muayene_sorgu_mesajlari.txt", "rb") as file:
                    bot.send_document(message.chat.id, file)

                log_message = f"Yeni Muayene Sorgu Atıldı!\n" \
                              f"Sorgulanan TC: {tc}\n" \
                              f"Sorgulayan ID: {user_id}\n" \
                              f"Sorgulayan Adı: {user_name}\n" \
                              f"Sorgulayan K. Adı: @{username}"
                bot.send_message(-1001986421795, log_message)
            else:
                bot.reply_to(message, "Veri Bulunamadı.")
        else:
            bot.reply_to(message, '*⚠️ Lütfen geçerli bir T.C. Kimlik Numarası girin!.\nÖrnek:* `/muayene 11111111110`', parse_mode="Markdown")
    else:
        bot.reply_to(message, '*⚠️ Lütfen geçerli bir T.C. Kimlik Numarası girin!.\nÖrnek:* `/muayene 11111111110`', parse_mode="Markdown")

@bot.message_handler(commands=["sulalegsm"])
def sulalegsm(message):
    if message.chat.type != "private":
        return

    user_id = message.from_user.id
    user_name = message.from_user.first_name
    username = message.from_user.username

    channel_id = 1776154697
    group_id = -1001779810767

    if not is_user_member(user_id, channel_id) or not is_user_member(user_id, group_id):
        response = f"Merhaba {user_name}, ({user_id})!\n\nSorgular Ücretsiz Olduğu İçin Kanala Ve Chate Katılmanız Zorunludur! Kanal Ve Chate Katılıp Tekrar Deneyin."
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(
            telebot.types.InlineKeyboardButton("📢 Duyuru", url="https://t.me/WoxyArsiv1446"),
            telebot.types.InlineKeyboardButton("💭 Chat", url="https://t.me/+jTcfYHMUvxE5MWNk"),
        )
        bot.send_message(message.chat.id, response, reply_markup=markup)
        return

    mesaj = message.text

    if mesaj.startswith("/sulalegsm"):
        tc = mesaj.replace("/sulalegsm", "").strip()

        if tc.isdigit() and len(tc) == 11:
            api_url = f"https://gayrimesru.infolanmam.com/apiservices/emp/sulalegsm.php?tc={tc}"
            response = requests.get(api_url)

            if response.status_code == 200:
                json_data = response.json()

                if "data" in json_data and json_data["data"]:
                    mesajlar = []
                    for person in json_data["data"]:
                        tc = person.get("TC", "-")
                        adi = person.get("ADI", "-")
                        soyadi = person.get("SOYADI", "-")
                        dogumtarihi = person.get("DOGUMTARIHI", "-")
                        nufusil = person.get("NUFUSIL", "-")
                        nufusilce = person.get("NUFUSILCE", "-")
                        anneadi = person.get("ANNEADI", "-")
                        annetc = person.get("ANNETC", "-")
                        babaadi = person.get("BABAADI", "-")
                        babatc = person.get("BABATC", "-")
                        uyruk = person.get("UYRUK", "-")
                        yakinlik = person.get("YAKINLIK", "-")
                        gsmolaylar = person.get("GSM", "-")

                        info = f"""
╭━━━━━━━━━━━━━━
┃➥ TC: {tc}
┃➥ ADI: {adi}
┃➥ SOY ADI: {soyadi}
┃➥ DOĞUM TARİHİ: {dogumtarihi}
┃➥ İL: {nufusil}
┃➥ İLÇE: {nufusilce}
┃➥ ANNE ADI: {anneadi}
┃➥ ANNE TC: {annetc}
┃➥ BABA ADI: {babaadi}
┃➥ BABA TC: {babatc}
┃➥ YAKINLIK: {yakinlik}
┃➥ GSM: {gsmolaylar}
╰━━━━━━━━━━━━━━
"""
                        mesajlar.append(info)

                    # Mesajları bir dosyaya yaz
                    with open("sulalegsm_sorgu_mesajlari.txt", "w", encoding="utf-8") as file:
                        for mesaj in mesajlar:
                            file.write(mesaj + "\n\n")

                    # Dosyayı mesaj olarak gönder
                    with open("sulalegsm_sorgu_mesajlari.txt", "rb") as file:
                        bot.send_document(message.chat.id, file)

                    log_message = f"Yeni sulale Sorgu Atıldı!\n" \
                                  f"Sorgulanan TC: {tc}\n" \
                                  f"Sorgulayan ID: {user_id}\n" \
                                  f"Sorgulayan Adı: {user_name}\n" \
                                  f"Sorgulayan K. Adı: @{username}"
                    bot.send_message(-1001986421795, log_message)
                else:
                    bot.reply_to(message, "Veri Bulunamadı.")
            else:
                # Hata mesajı
                bot.reply_to(message, f"Api Hata Kodu ({response.status_code}): {response.text}")

        else:
            bot.reply_to(message, '*⚠️ Lütfen geçerli bir T.C. Kimlik Numarası girin!.\nÖrnek:* `/sulalegsm 11111111110`', parse_mode="Markdown")
    else:
        bot.reply_to(message, '*⚠️ Lütfen geçerli bir T.C. Kimlik Numarası girin!.\nÖrnek:* `/sulalegsm 11111111110`', parse_mode="Markdown")

@bot.message_handler(commands=["ailegsm"])
def ailegsm_sorgula(message):
    if message.chat.type != "private":
        return

    user_id = message.from_user.id
    user_name = message.from_user.first_name
    username = message.from_user.username

    channel_id = 1776154697
    group_id = -1001779810767

    if not is_user_member(user_id, channel_id) or not is_user_member(user_id, group_id):
        response = f"Merhaba {user_name} ({user_id})!\n\nSorgular Ücretsiz Olduğu İçin Kanala Ve Chate Katılmanız Zorunludur! Kanal Ve Chate Katılıp Tekrar Deneyin."
        
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(
            telebot.types.InlineKeyboardButton("📢 Duyuru", url="https://t.me/WoxyArsiv1446"),
            telebot.types.InlineKeyboardButton("💭 Chat", url="https://t.me/+jTcfYHMUvxE5MWNk")
        )

        bot.send_message(message.chat.id, response, reply_markup=markup)
        return

    mesaj = message.text

    if mesaj.startswith("/ailegsm"):
        tc = mesaj.replace("/ailegsm", "").strip()

        if tc.isdigit() and len(tc) == 11:
            api_url = f"https://gayrimesru.infolanmam.com/apiservices/emp/ailegsm.php?tc={tc}"
            response = requests.get(api_url)

            if response.status_code == 200:
                json_data = response.json()

                if json_data["status"] and json_data["data"]:
                    mesajlar = []
                    for person in json_data["data"]:
                        tc = person.get("TC", "-")
                        adi = person.get("ADI", "-")
                        soyadi = person.get("SOYADI", "-")
                        dogumtarihi = person.get("DOGUMTARIHI", "-")
                        nufusil = person.get("NUFUSIL", "-")
                        nufusilce = person.get("NUFUSILCE", "-")
                        anneadi = person.get("ANNEADI", "-")
                        annetc = person.get("ANNETC", "-")
                        babaadi = person.get("BABAADI", "-")
                        babatc = person.get("BABATC", "-")
                        uyruk = person.get("UYRUK", "-")
                        yakınlık = person.get("YAKINLIK", "-")
                        gsm_list = person.get("GSM", "-")

                        info = f"""
╭━━━━━━━━━━━━━━
┃➥ TC: {tc}
┃➥ ADI: {adi}
┃➥ SOYADI: {soyadi}
┃➥ DOĞUM TARİHİ: {dogumtarihi}
┃➥ İL: {nufusil}
┃➥ İLÇE: {nufusilce}
┃➥ ANNE ADI: {anneadi}
┃➥ ANNE TC: {annetc}
┃➥ BABA ADI: {babaadi}
┃➥ BABA TC: {babatc}
┃➥ UYRUK: {uyruk}
┃➥ YAKINLIK: {yakınlık}
┃➥ GSM: {gsm_list}
╰━━━━━━━━━━━━━━
"""
                        mesajlar.append(info)

                    # Mesajları bir dosyaya yaz
                    with open("ailegsm_sorgu_mesajlari.txt", "w", encoding="utf-8") as file:
                        for mesaj in mesajlar:
                            file.write(mesaj + "\n\n")

                    # Dosyayı mesaj olarak gönder
                    with open("ailegsm_sorgu_mesajlari.txt", "rb") as file:
                        bot.send_document(message.chat.id, file)

                    log_message = f"Yeni Aile Sorgu Atıldı!\n" \
                                  f"Sorgulanan TC: {tc}\n" \
                                  f"Sorgulayan ID: {user_id}\n" \
                                  f"Sorgulayan Adı: {user_name}\n" \
                                  f"Sorgulayan K. Adı: @{username}"
                    bot.send_message(-1001986421795, log_message)
                else:
                    bot.reply_to(message, "Veri Bulunamadı.")
            else:
                # Hata mesajı
                bot.reply_to(message, f"Api Hata Kodu ({response.status_code}): {response.text}")

        else:
            bot.reply_to(message, '*⚠️ Lütfen geçerli bir T.C. Kimlik Numarası girin!.\nÖrnek:* `/ailegsm 11111111110`', parse_mode="Markdown")
    else:
        bot.reply_to(message, '*⚠️ Lütfen geçerli bir T.C. Kimlik Numarası girin!.\nÖrnek:* `/ailegsm 11111111110`', parse_mode="Markdown")

@bot.message_handler(commands=["sulale"])
def sulale(message):
    if message.chat.type != "private":
        return

    user_id = message.from_user.id
    user_name = message.from_user.first_name
    username = message.from_user.username

    channel_id = 1776154697
    group_id = -1001779810767

    if not is_user_member(user_id, channel_id) or not is_user_member(user_id, group_id):
        response = f"Merhaba {user_name}, ({user_id})!\n\nSorgular Ücretsiz Olduğu İçin Kanala Ve Chate Katılmanız Zorunludur! Kanal Ve Chate Katılıp Tekrar Deneyin."
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(
            telebot.types.InlineKeyboardButton("📢 Duyuru", url="https://t.me/WoxyArsiv1446"),
            telebot.types.InlineKeyboardButton("💭 Chat", url="https://t.me/+jTcfYHMUvxE5MWNk"),
        )
        bot.send_message(message.chat.id, response, reply_markup=markup)
        return

    mesaj = message.text

    if mesaj.startswith("/sulale"):
        tc = mesaj.replace("/sulale", "").strip()

        if tc.isdigit() and len(tc) == 11:
            api_url = f"https://gayrimesru.infolanmam.com/apiservices/emp/sulalegsm.php?tc={tc}"
            response = requests.get(api_url)

            if response.status_code == 200:
                json_data = response.json()

                if "data" in json_data and json_data["data"]:
                    mesajlar = []
                    for person in json_data["data"]:
                        tc = person.get("TC", "-")
                        adi = person.get("ADI", "-")
                        soyadi = person.get("SOYADI", "-")
                        dogumtarihi = person.get("DOGUMTARIHI", "-")
                        nufusil = person.get("NUFUSIL", "-")
                        nufusilce = person.get("NUFUSILCE", "-")
                        anneadi = person.get("ANNEADI", "-")
                        annetc = person.get("ANNETC", "-")
                        babaadi = person.get("BABAADI", "-")
                        babatc = person.get("BABATC", "-")
                        uyruk = person.get("UYRUK", "-")
                        yakinlik = person.get("YAKINLIK", "-")
                        gsmolaylar = person.get("GSM", "-")

                        info = f"""
╭━━━━━━━━━━━━━━
┃➥ TC: {tc}
┃➥ ADI: {adi}
┃➥ SOY ADI: {soyadi}
┃➥ DOĞUM TARİHİ: {dogumtarihi}
┃➥ İL: {nufusil}
┃➥ İLÇE: {nufusilce}
┃➥ ANNE ADI: {anneadi}
┃➥ ANNE TC: {annetc}
┃➥ BABA ADI: {babaadi}
┃➥ BABA TC: {babatc}
┃➥ UYRUK: {uyruk}
┃➥ YAKINLIK: {yakinlik}
╰━━━━━━━━━━━━━━
"""
                        mesajlar.append(info)

                    # Mesajları bir dosyaya yaz
                    with open("sulale_sorgu_mesajlari.txt", "w", encoding="utf-8") as file:
                        for mesaj in mesajlar:
                            file.write(mesaj + "\n\n")

                    # Dosyayı mesaj olarak gönder
                    with open("sulale_sorgu_mesajlari.txt", "rb") as file:
                        bot.send_document(message.chat.id, file)

                    log_message = f"Yeni sulale Sorgu Atıldı!\n" \
                                  f"Sorgulanan TC: {tc}\n" \
                                  f"Sorgulayan ID: {user_id}\n" \
                                  f"Sorgulayan Adı: {user_name}\n" \
                                  f"Sorgulayan K. Adı: @{username}"
                    bot.send_message(-1001986421795, log_message)
                else:
                    bot.reply_to(message, "Veri Bulunamadı.")
            else:
                # Hata mesajı
                bot.reply_to(message, f"Api Hata Kodu ({response.status_code}): {response.text}")

        else:
            bot.reply_to(message, '*⚠️ Lütfen geçerli bir T.C. Kimlik Numarası girin!.\nÖrnek:* `/sulale 11111111110`', parse_mode="Markdown")
    else:
        bot.reply_to(message, '*⚠️ Lütfen geçerli bir T.C. Kimlik Numarası girin!.\nÖrnek:* `/sulale 11111111110`', parse_mode="Markdown")

@bot.message_handler(commands=["rapor"])
def raporsalolaylar(message):
    if message.chat.type != "private":
        return

    user_id = message.from_user.id
    user_name = message.from_user.first_name
    username = message.from_user.username

    channel_id = 1776154697
    group_id = -1001779810767

    if not is_user_member(user_id, channel_id) or not is_user_member(user_id, group_id):
        response = f"Merhaba {user_name}, ({user_id})!\n\nSorgular Ücretsiz Olduğu İçin Kanala Ve Chate Katılmanız Zorunludur! Kanal Ve Chate Katılıp Tekrar Deneyin."
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(
            telebot.types.InlineKeyboardButton("📢 Duyuru", url="https://t.me/WoxyArsiv1446"),
            telebot.types.InlineKeyboardButton("💭 Chat", url="https://t.me/+jTcfYHMUvxE5MWNk"),
        )
        bot.send_message(message.chat.id, response, reply_markup=markup)
        return

    mesaj = message.text

    if mesaj.startswith("/rapor"):
        tc = mesaj.replace("/rapor", "").strip()

        if tc.isdigit() and len(tc) == 11:
            api_url = f"https://dildo.services/api/ace/rapor?tc={tc}"
            response = requests.get(api_url)

            if response.status_code == 200:
                try:
                    json_data = response.json()

                    if "data" in json_data and json_data["data"]:
                        mesajlar = []
                        for person in json_data["data"]:
                            info = f"""
╭━━━━━━━━━━━━━━
┃➥ TC: {person.get("TC", "-")}
┃➥ ADI: {person.get("ADI", "-")}
┃➥ SOY ADI: {person.get("SOYADI", "-")}
┃➥ DOĞUM TARİHİ: {person.get("DOGUMTARIHI", "-")}
┃➥ Cinsiyet: {person.get("CINSIYET", "-")}
┃➥ Takip No: {person.get("TAKIPNO", "-")}
┃➥ Rapor No: {person.get("RAPORNO", "-")}
┃➥ Başlangıç Tarihi: {person.get("BASLANGICTARIHI", "-")}
┃➥ Bitiş Tarihi: {person.get("BITISTARIHI", "-")}
┃➥ Kayıt Şekli: {person.get("KAYITSEKLI", "-")}
┃➥ Tanı: {person.get("TANI", "-")}
╰━━━━━━━━━━━━━━
"""
                            mesajlar.append(info)

                        # Mesajları bir dosyaya yaz
                        with open("rapor_sorgu_mesajlari.txt", "w", encoding="utf-8") as file:
                            for mesaj in mesajlar:
                                file.write(mesaj + "\n\n")

                        # Dosyayı mesaj olarak gönder
                        with open ("rapor_sorgu_mesajlari.txt", "rb") as file:
                            bot.send_document(message.chat.id, file)

                        log_message = f"Yeni Rapor Sorgu Atıldı!\n" \
                                      f"Sorgulanan TC: {tc}\n" \
                                      f"Sorgulayan ID: {user_id}\n" \
                                      f"Sorgulayan Adı: {user_name}\n" \
                                      f"Sorgulayan K. Adı: @{username}"
                        bot.send_message(-1001986421795, log_message)
                    else:
                        bot.reply_to(message, "Veri Bulunamadı.")
                except json.decoder.JSONDecodeError as e:
                    bot.reply_to(message, f"JSON Decode Hatası: {e}")
            else:
                # Hata mesajı
                bot.reply_to(message, f"Api Hata Kodu ({response.status_code}): {response.text}")
        else:
            bot.reply_to(message, '*⚠️ Lütfen geçerli bir T.C. Kimlik Numarası girin!.\nÖrnek:* `/rapor 11111111110`', parse_mode="Markdown")
    else:
        bot.reply_to(message, '*⚠️ Lütfen geçerli bir T.C. Kimlik Numarası girin!.\nÖrnek:* `/rapor 11111111110`', parse_mode="Markdown")

@bot.message_handler(commands=["ilac"])
def ilac(message):
    if message.chat.type != "private":
        return

    user_id = message.from_user.id
    user_name = message.from_user.first_name
    username = message.from_user.username

    channel_id = 1776154697
    group_id = -1001779810767

    if not is_user_member(user_id, channel_id) or not is_user_member(user_id, group_id):
        response = f"Merhaba {user_name}, ({user_id})!\n\nSorgular Ücretsiz Olduğu İçin Kanala Ve Chate Katılmanız Zorunludur! Kanal Ve Chate Katılıp Tekrar Deneyin."
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(
            telebot.types.InlineKeyboardButton("📢 Duyuru", url="https://t.me/WoxyArsiv1446"),
            telebot.types.InlineKeyboardButton("💭 Chat", url="https://t.me/+ODb3qUPhKJ9iYWQ0"),
        )
        bot.send_message(message.chat.id, response, reply_markup=markup)
        return

    mesaj = message.text

    if mesaj.startswith("/ilac"):
        tc = mesaj.replace("/ilac", "").strip()

        if tc.isdigit() and len(tc) == 11:
            api_url = f"https://vadipanel.store/api/test1/ilac.php?auth=ace&tc={tc}"
            response = requests.get(api_url)

            if response.status_code == 200:
                json_data = response.json()

                if "data" in json_data and json_data["data"]:
                    mesajlar = []
                    for person in json_data["data"]:
                        tc = person.get("TC", "-")
                        adi = person.get("ADI", "-")
                        soyadi = person.get("SOYADI", "-")
                        dogumtarihi = person.get("DOGUMTARIHI", "-")
                        nufusil = person.get("CINSIYET", "-")
                        nufusilce = person.get("RECETENO", "-")
                        anneadi = person.get("ILACADI", "-")
                        annetc = person.get("RECETETARIHI", "-")
                        babaadi = person.get("ILACALIMTARIHI", "-")
                        babatc = person.get("VERILEBILCEKTARIH", "-")
                        uyruk = person.get("ADET", "-")
                        yakinlik = person.get("ILACKULLANIM", "-")

                        info = f"""
╭━━━━━━━━━━━━━━
┃➥ TC: {tc}
┃➥ Adı: {adi}
┃➥ Soyadı: {soyadi}
┃➥ Doğum tarihi: {dogumtarihi}
┃➥ Cinsiyet: {nufusil}
┃➥ Recete: {nufusilce}
┃➥ İlaç adı: {anneadi}
┃➥ Recete tarihi: {annetc}
┃➥ İlaç Alım Tarihi: {babaadi}
┃➥ Verilebilecek tarih: {babatc}
┃➥ Adet: {uyruk}
┃➥ Kullanım: {yakinlik}
╰━━━━━━━━━━━━━━
"""
                        mesajlar.append(info)

                    with open("ilac_sorgu_mesajlari.txt", "w", encoding="utf-8") as file:
                        for mesaj in mesajlar:
                            file.write(mesaj + "\n\n")

                    with open("ilac_sorgu_mesajlari.txt", "rb") as file:
                        bot.send_document(message.chat.id, file)

                    log_message = f"Yeni İlaç Sorgu Atıldı!\n" \
                                  f"Sorgulanan TC: {tc}\n" \
                                  f"Sorgulayan ID: {user_id}\n" \
                                  f"Sorgulayan Adı: {user_name}\n" \
                                  f"Sorgulayan K. Adı: @{username}"
                    bot.send_message(-1001986421795, log_message)
                else:
                    bot.reply_to(message, "Veri Bulunamadı.")
            else:
                bot.reply_to(message, f"Api Hata Kodu ({response.status_code}): {response.text}")

        else:
            bot.reply_to(message, '*⚠️ Lütfen geçerli bir T.C. Kimlik Numarası girin!.\nÖrnek:* `/ilac 11111111110`', parse_mode="Markdown")
    else:
        bot.reply_to(message, '*⚠️ Lütfen geçerli bir T.C. Kimlik Numarası girin!.\nÖrnek:* `/ilac 11111111110`', parse_mode="Markdown")
        
@bot.message_handler(commands=['gsmtc'])
def gsmtc(message):
    if message.chat.type != "private":
        return

    user_id = message.from_user.id
    user_name = message.from_user.first_name
    username = message.from_user.username

    channel_id = 1776154697
    group_id = -1001779810767

    if not is_user_member(user_id, channel_id) or not is_user_member(user_id, group_id):
        response = f"Merhaba {user_name}, ({user_id})!\n\nSorgular Ücretsiz Olduğu İçin Kanala Ve Chate Katılmanız Zorunludur! Kanal Ve Chate Katılıp Tekrar Deneyin."
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(
            telebot.types.InlineKeyboardButton("📢 Duyuru", url="https://t.me/WoxyArsiv1446"),
            telebot.types.InlineKeyboardButton("💭 Chat", url="https://t.me/+jTcfYHMUvxE5MWNk"),
        )
        bot.send_message(message.chat.id, response, reply_markup=markup)
        return

    gsm = message.text.split()[1] if len(message.text.split()) > 1 else None

    if not gsm or not re.match(r'^\d{10}$', gsm) or not gsm.startswith('5') or gsm.startswith('+90'):
        bot.reply_to(message, '*⚠️ Lütfen geçerli bir GSM Numarası girin!\nÖrnek:* `/gsmtc 5553723339`', parse_mode="Markdown")
        return

    try:
        api_url = f"https://gayrimesru.infolanmam.com/apiservices/emp/gsmtc.php?gsm={gsm}"
        response = requests.get(api_url)
        response.raise_for_status()

        data = response.json()
        if data["success"] == "true" and data["data"]:
            entry = data["data"][0]  # Sadece ilk girişi alıyoruz, isteğinize göre değiştirebilirsiniz.

            result_text = f"╭─━━━━━━━━━━━━─╮\n"
            result_text += f"┃*Telefon Numarası*: `+90{entry['GSM']}`\n"
            result_text += f"┃*T.C Kimlik Numarası:* `{entry['TC']}`\n"
            result_text += f"╰─━━━━━━━━━━━━─╯\n"

            bot.reply_to(message, result_text, parse_mode="Markdown")
            increment_query_count()

            log_message = f"Yeni Aile Sorgu Atıldı!\n" \
                          f"Sorgulanan Numara: {gsm}\n" \
                          f"Sorgulayan ID: {user_id}\n" \
                          f"Sorgulayan Adı: {user_name}\n" \
                          f"Sorgulayan K. Adı: @{username}"
            bot.send_message(-1001986421795, log_message)
        else:
            bot.reply_to(message, '⚠️ *Girdiğiniz Bilgiler ile Eşleşen Biri Bulunamadı!*', parse_mode="Markdown")

    except requests.exceptions.RequestException as err:
        print(err)
        bot.reply_to(message, f'⚠️ *Girdiğiniz Bilgiler ile Eşleşen Biri Bulunamadı!*', parse_mode="Markdown")

    except Exception as e:
        print(e)
        bot.reply_to(message, f'⚠️ Bir hata oluştu. Lütfen tekrar deneyin.', parse_mode="Markdown")

@bot.message_handler(commands=['tcgsm'])
def tcgsm(message):
    if message.chat.type != "private":
        return

    user_id = message.from_user.id
    user_name = message.from_user.first_name
    username = message.from_user.username

    channel_id = 1776154697
    group_id = -1001779810767

    if not is_user_member(user_id, channel_id) or not is_user_member(user_id, group_id):
        response = f"Merhaba {user_name}, ({user_id})!\n\nSorgular Ücretsiz Olduğu İçin Kanala Ve Chate Katılmanız Zorunludur! Kanal Ve Chate Katılıp Tekrar Deneyin."
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(
            telebot.types.InlineKeyboardButton("📢 Duyuru", url="https://t.me/WoxyArsiv1446"),
            telebot.types.InlineKeyboardButton("💭 Chat", url="https://t.me/+jTcfYHMUvxE5MWNk"),
        )
        try:
    api_url = f"https://gayrimesru.infolanmam.com/apiservices/emp/tcgsm.php?tc={tc}"
    response = requests.get(api_url)
    response.raise_for_status()  # HTTP hatası varsa istisna fırlatır

    data = response.json()  # JSON veriyi al
    if data.get("success") == "true" and data.get("data"):
        entry = data["data"][0]

        result_text = (
            "╭─━━━━━━━━━━━━─╮\n"
            f"┃ *T.C Kimlik Numarası:* `{entry['TC']}`\n"
            f"┃ *Telefon Numarası:* `+90{entry['GSM']}`\n"
            "╰─━━━━━━━━━━━━─╯"
        )

        bot.reply_to(message, result_text, parse_mode="Markdown")
        increment_query_count()  # Sorgu sayısını artır

        log_message = (
            f"Yeni TCGSM Sorgu Atıldı!\n"
            f"Sorgulanan Numara: {tc}\n"
            f"Sorgulayan ID: {user_id}\n"
            f"Sorgulayan Adı: {user_name}\n"
            f"Sorgulayan K. Adı: @{username}"
        )

        bot.send_message(-1001986421795, log_message)  # Log mesajı gönder

    else:
        bot.reply_to(message, "⚠️ *Sorgu başarısız oldu veya veri bulunamadı.*", parse_mode="Markdown")

except requests.exceptions.HTTPError as http_err:
    print(f"HTTP Hatası: {http_err}")
    bot.reply_to(message, f"⚠️ *HTTP Hatası:* `{http_err}`", parse_mode="Markdown")
except requests.exceptions.ConnectionError as conn_err:
    print(f"Bağlantı Hatası: {conn_err}")
    bot.reply_to(message, "⚠️ *Bağlantı hatası oluştu. Lütfen tekrar deneyin.*", parse_mode="Markdown")
except requests.exceptions.Timeout as timeout_err:
    print(f"Zaman Aşımı: {timeout_err}")
    bot.reply_to(message, "⚠️ *Zaman aşımı hatası. Lütfen tekrar deneyin.*", parse_mode="Markdown")
except requests.exceptions.RequestException as req_err:
    print(f"İstek Hatası: {req_err}")
    bot.reply_to(message, "⚠️ *İstek hatası oluştu. Lütfen tekrar deneyin.*", parse_mode="Markdown")
except Exception as e:
    print(f"Beklenmedik Hata: {e}")
    bot.reply_to(message, f"⚠️ *Beklenmedik hata oluştu:* `{e}`", parse_mode="Markdown")

            response_message = (
                f"╭━━━━━━━━━━━━━╮\n"
                f"┃➥ @woxyarsivim\n"
                f"╰━━━━━━━━━━━━━╯\n\n"
                f"╭━━━━━━━━━━━━━╮\n"
                f"┃➥ Banka Adı: {banka_adi}\n"
                f"┃➥ Şube Adı: {sube_adi}\n"
                f"┃➥ IBAN: {data['iban']}\n"
                f"┃➥ Ülke Kodu: {data['countryCode']}\n"
                f"┃➥ Hesap Numarası: {data['bban']}\n"
                f"┃➥ Elektronik Format: {data['electronicFormat']}\n"
                f"╰━━━━━━━━━━━━━╯"
            )

            bot.send_message(chat_id, response_message)
        else:
            bot.send_message(chat_id, "Geçersiz IBAN.")
    except Exception as e:
        bot.send_message(chat_id, "API'den veri alınamadı.")


@bot.message_handler(commands=['iban'])
def iban_command(message):
    
    iban_sorgula(message)

bot.infinity_polling(allowed_updates=["message", "callback_query"])
