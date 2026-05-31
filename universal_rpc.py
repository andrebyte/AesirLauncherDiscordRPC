import time
import logging
import requests
import psutil
from pypresence import Presence
from pypresence.exceptions import DiscordNotFound

# ─────────────────────────────────────────────────────────────────
# ⚙️ AYARLAR
# ─────────────────────────────────────────────────────────────────
CLIENT_ID = "1504506373654839326"  # Uygulamanızın Client ID'si
MY_USERNAME = "iAndrex28"          # Sabit Oyuncu Adınız
SERVER_NAME = "Aesir Network"

SMALL_IMAGE_KEY = "aesir"     # Developer Portal'daki küçük logonun key'i
LARGE_IMAGE_FALLBACK = "aesir" # Kafa API'si çalışmazsa kullanılacak yedek büyük resim key'i

# İzlenecek Süreç İsimleri (Görev Yöneticisindeki Adlar)
LAUNCHER_PROCESS_NAME = "Aesir Launcher.exe" 
GAME_PROCESS_NAME = ["javaw.exe", "java.exe"] 

# ─────────────────────────────────────────────────────────────────
# 🛠️ LOGGING AYARI
# ─────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s │ %(levelname)s │ %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger("AesirRPC")


def get_validated_avatar(player_name):
    """
    mc-heads.net API'sini kullanarak kullanıcının kafa resmini getirir.
    Erişilemezse yedek logoya geçer.
    """
    url = f"https://mc-heads.net/avatar/{player_name}/128"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return url
        else:
            return LARGE_IMAGE_FALLBACK
    except requests.exceptions.RequestException:
        return LARGE_IMAGE_FALLBACK


class LauncherRPC:
    def __init__(self):
        self.client_id = CLIENT_ID
        self.rpc = None
        self.connected = False
        self.last_state = None
        self.start_time = None
        
        # Sabit oyuncu ismini al ve avatar linkini doğrula
        self.player_name = MY_USERNAME
        self.large_image_data = get_validated_avatar(self.player_name)

    def check_processes(self):
        """Sistemde launcher veya oyunun açık olup olmadığını kontrol eder."""
        launcher_running = False
        game_running = False

        launcher_names = [LAUNCHER_PROCESS_NAME.lower()]
        game_names = [n.lower() for n in GAME_PROCESS_NAME]

        try:
            for proc in psutil.process_iter(['name']):
                name = proc.info['name'].lower()
                if any(ln in name for ln in launcher_names):
                    launcher_running = True
                if any(gn in name for gn in game_names):
                    game_running = True
        except:
            pass

        return launcher_running, game_running

    def connect(self):
        """Discord IPC soketine bağlanmaya çalışır."""
        if self.connected:
            return True
            
        try:
            self.rpc = Presence(self.client_id)
            self.rpc.connect()
            self.connected = True
            self.start_time = int(time.time())
            logger.info("✅ Discord RPC başarıyla bağlandı!")
            return True
        except DiscordNotFound:
            return False
        except Exception:
            return False

    def disconnect(self):
        """Discord bağlantısını temizler ve kapatır."""
        if self.connected:
            try:
                if self.rpc:
                    self.rpc.clear()
                    self.rpc.close()
                logger.info("🛑 Launcher kapandı, Discord durumu temizlendi.")
            except:
                pass
            self.connected = False
            self.rpc = None
            self.last_state = None
            self.start_time = None

    def update(self, state_type):
        """Premium RPC verilerini Discord'a gönderir."""
        if not self.connect():
            return

        try:
            if state_type == "GAME":
                self.rpc.update(
                    details=f"{self.player_name} olarak oyunda",
                    state=f"Sunucu: {SERVER_NAME}",
                    large_image=self.large_image_data, 
                    large_text=f"Oyuncu: {self.player_name}",
                    small_image=SMALL_IMAGE_KEY,          # KÜÇÜK LOGO (Örn: aesir_logo)
                    small_text="Aesir Launcher",          # ÜSTÜNE GELİNCE YAZAN YAZI
                    start=self.start_time
                )
                if self.last_state != "GAME":
                    logger.info(f"🎮 Durum: Oyunda ({self.player_name})")
                    
            elif state_type == "LAUNCHER":
                self.rpc.update(
                    details=f"{self.player_name} (Launcher)",
                    state="Ana Menüde",
                    large_image=self.large_image_data, 
                    large_text=f"Oyuncu: {self.player_name}",
                    small_image=SMALL_IMAGE_KEY,          # KÜÇÜK LOGO (Örn: aesir_logo)
                    small_text="Aesir Launcher",          # ÜSTÜNE GELİNCE YAZAN YAZI
                    start=self.start_time
                )
                if self.last_state != "LAUNCHER":
                    logger.info(f"📋 Durum: Ana Menü ({self.player_name})")

            self.last_state = state_type
        except Exception as e:
            logger.error(f"⚠️ RPC Güncelleme hatası: {e}")
            self.connected = False

    def run(self):
        """Sistemi ayakta tutan ve izleyen ana döngü."""
        logger.info("🚀 Aesir RPC Otomatik İzleyici Başlatıldı! (Arka planda bekliyor)")
        try:
            while True:
                launcher_active, game_active = self.check_processes()

                if game_active:
                    self.update("GAME")
                elif launcher_active:
                    self.update("LAUNCHER")
                else:
                    if self.connected:
                        self.disconnect()
                
                # Sistemi yormamak için 10 saniyede bir kontrol et
                time.sleep(10)
        except KeyboardInterrupt:
            self.disconnect()


if __name__ == "__main__":
    rpc_system = LauncherRPC()
    rpc_system.run()
