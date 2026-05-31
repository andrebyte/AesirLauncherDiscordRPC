import sys
import time
import json
import os
import logging
import requests
from pypresence import Presence
from pypresence.exceptions import DiscordNotFound

# ─────────────────────────────────────────────────────────────────
# ⚙️ AYARLAR
# ─────────────────────────────────────────────────────────────────
CLIENT_ID = "1504506373654839326"  # Uygulamanızın Client ID'si
SMALL_IMAGE_KEY = "aesir_logo"     # Developer Portal'daki küçük logonun key'i
LARGE_IMAGE_FALLBACK = "aesir_logo" # Kafa API'si çalışmazsa kullanılacak yedek büyük resim key'i
SERVER_NAME = "Aesir Network"

# Aesir Launcher Özel Ayarları
CONFIG_FILE_PATH = "aesir_config.json"
DEFAULT_PLAYER_NAME = "AesirPlayer"

# ─────────────────────────────────────────────────────────────────
# 🛠️ LOGGING AYARI
# ─────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s │ %(levelname)s │ %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger("AesirRPC")


def get_player_name():
    """
    Oyuncu adını otomatik olarak belirler.
    1. Terminal argümanı (örn: python universal_rpc.py iAndrex28)
    2. aesir_config.json dosyası (yoksa otomatik oluşturulur)
    """
    # 1. Argüman Kontrolü (En Yüksek Öncelik)
    if len(sys.argv) > 1:
        name_from_arg = sys.argv[1].strip()
        logger.info(f"✅ Oyuncu adı terminal argümanından alındı: {name_from_arg}")
        return name_from_arg
        
    # 2. Aesir Config Dosyası Kontrolü ve Otomatik Oluşturma
    if os.path.exists(CONFIG_FILE_PATH):
        try:
            with open(CONFIG_FILE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                if "username" in data and data["username"]:
                    name_from_file = data["username"].strip()
                    logger.info(f"✅ Oyuncu adı aesir_config.json dosyasından okundu: {name_from_file}")
                    return name_from_file
        except Exception as e:
            logger.warning(f"⚠️ {CONFIG_FILE_PATH} okunamadı: {e}")
    else:
        # Dosya yoksa temiz bir JSON formatında otomatik oluştur
        try:
            default_data = {"username": DEFAULT_PLAYER_NAME}
            with open(CONFIG_FILE_PATH, "w", encoding="utf-8") as f:
                json.dump(default_data, f, indent=4)
            logger.info(f"📝 {CONFIG_FILE_PATH} bulunamadı, otomatik olarak oluşturuldu!")
        except Exception as e:
            logger.warning(f"⚠️ {CONFIG_FILE_PATH} oluşturulurken hata: {e}")
            
    # Hiçbir şey bulunamazsa varsayılan isme düş
    return DEFAULT_PLAYER_NAME


def get_validated_avatar(player_name):
    """
    mc-heads.net API'sini kullanarak kullanıcının kafa resmini getirir.
    requests.get ile URL'nin çalışıp çalışmadığını kontrol eder.
    Erişilemezse yedek logoya (aesir_logo) geçer.
    """
    url = f"https://mc-heads.net/avatar/{player_name}/128"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return url
        else:
            logger.warning(f"Avatar API'si yanıt vermedi (Kod: {response.status_code}). Yedek logoya geçiliyor.")
            return LARGE_IMAGE_FALLBACK
    except requests.exceptions.RequestException as e:
        logger.warning(f"Avatar API bağlantı hatası. Yedek logoya geçiliyor. Hata detayı: {e}")
        return LARGE_IMAGE_FALLBACK


class LauncherRPC:
    def __init__(self, player_name):
        self.client_id = CLIENT_ID
        self.player_name = player_name
        self.rpc = None
        
        # Oyuna giriş anı
        self.start_time = int(time.time())
        self.connected = False
        
        # Kafa (Avatar) resmi doğrulanıyor
        logger.info(f"🔍 '{self.player_name}' için skin resmi doğrulanıyor...")
        self.large_image_data = get_validated_avatar(self.player_name)

    def connect(self):
        """Discord IPC soketine bağlanmaya çalışır."""
        if self.connected:
            return True
            
        try:
            self.rpc = Presence(self.client_id)
            self.rpc.connect()
            self.connected = True
            logger.info("✅ Discord RPC başarıyla bağlandı!")
            return True
        except DiscordNotFound:
            logger.warning("⚠️ Discord arkada açık değil, bekleniyor...")
            return False
        except Exception as e:
            logger.error(f"❌ Bağlantı hatası: {e}")
            return False

    def update(self):
        """Premium RPC verilerini Discord'a gönderir."""
        if not self.connect():
            return

        try:
            self.rpc.update(
                details=f"{self.player_name} olarak oyunda",
                state=f"Sunucu: {SERVER_NAME}",
                large_image=self.large_image_data, 
                large_text=f"Oyuncu: {self.player_name}",
                small_image=SMALL_IMAGE_KEY,
                small_text="Aesir Launcher",
                start=self.start_time
            )
            logger.info(f"🎮 Discord durumu güncellendi: {self.player_name} | {SERVER_NAME}")
        except Exception as e:
            logger.error(f"⚠️ RPC Güncelleme hatası: {e}")
            self.connected = False

    def run(self):
        """Sistemi ayakta tutan ana döngü."""
        logger.info(f"🚀 Aesir RPC Başlatılıyor... (Oyuncu: {self.player_name})")
        try:
            while True:
                self.update()
                # Rate-limit koruması (15 saniye)
                time.sleep(15)
        except KeyboardInterrupt:
            logger.info("👋 Sistem kapatılıyor, RPC temizleniyor...")
            if self.connected and self.rpc:
                try:
                    self.rpc.clear()
                    self.rpc.close()
                except:
                    pass


if __name__ == "__main__":
    print("==================================================")
    print("        AESIR LAUNCHER - CUSTOM ENTEGRE RPC       ")
    print("==================================================")
    
    # 1. Argüman -> 2. aesir_config.json -> 3. Default
    aktif_oyuncu = get_player_name()
    
    # Sistemi başlat
    rpc_system = LauncherRPC(player_name=aktif_oyuncu)
    rpc_system.run()
