"""
╔══════════════════════════════════════════════════════════════════╗
║           AESIR LAUNCHER — Arkadas Canlisi RPC İzleyici          ║
║                                                                  ║
║  Bu script, arka planda Minecraft veya Launcher acik mi diye     ║
║  kolacan eder, Discord'da havani atmani saglar.                  ║
╚══════════════════════════════════════════════════════════════════╝
"""

import time
import psutil
import logging
import atexit
import os
import shutil
from pypresence import Presence
from pypresence.exceptions import DiscordNotFound

# ─────────────────────────────────────────────────────────────────
# ⚙️ AYARLAR (Kanka Buraya Dikkat)
# ─────────────────────────────────────────────────────────────────

# Discord Portal'dan kaptigin o uzun Client ID'yi buraya yapistiriyoruz
CLIENT_ID = "1504506373654839326" 

# Launcher ve oyunun isimleri. Gorev yoneticisinde ne yaziyorsa o!
# Senin sistemde "java.exe" oldugu icin listeye onu da ekledim.
LAUNCHER_PROCESS_NAME = "Aesir Launcher.exe" 
GAME_PROCESS_NAME = ["javaw.exe", "java.exe"] 

# Discord'a yukledigin o yakisikli resimlerin isimleri (keyleri)
LARGE_IMAGE_KEY = "aesir" 
SMALL_IMAGE_KEY = "minecraft_logo" 

# Oynadigin surum neyse buraya yaz, Discord'da oyle gozuksun
MC_VERSION = "1.21.8"

# Islemciyi yormayalim diye buraya 5 saniyelik bir mola koyduk
CHECK_INTERVAL = 5 

# ─────────────────────────────────────────────────────────────────
# 🧹 AKILLI KLASOR TEMIZLIGI
# ─────────────────────────────────────────────────────────────────

def klasoru_pırıl_pırıl_yap():
    """
    Kanka etrafta gereksiz dosya birakmayalim, klasor cicek gibi kalsin.
    Deneme dosyalari ve pycache artiklarini supuruyoruz.
    """
    su_an_buradayim = os.path.dirname(os.path.abspath(__file__))
    
    # Silineceklerin listesi (Varsa temizle gitsin)
    # Artık aesir_watcher kullandığımız için eski rpc ve demo dosyalarına gerek yok.
    cope_gidecekler = ["__pycache__", "find_my_process.py", "launcher_example.py", "aesir_rpc.py"]
    
    for cop in cope_gidecekler:
        yol = os.path.join(su_an_buradayim, cop)
        if os.path.exists(yol):
            try:
                if os.path.isdir(yol):
                    shutil.rmtree(yol) # Klasoru komple ucur
                else:
                    os.remove(yol) # Dosyayi sil
            except:
                pass # Silemediysek dert etme, canimiz sag olsun

# ─────────────────────────────────────────────────────────────────
# 🛠️ LOGGING AYARI (Neler olup bitiyor gorelim)
# ─────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s │ %(levelname)s │ %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger("AesirWatcher")

class AesirWatcher:
    def __init__(self):
        self.rpc = None
        self.connected = False
        self.last_state = None 
        self.start_time = None

    def check_processes(self):
        """Sistemde ne var ne yok bakip geliyoruz."""
        launcher_running = False
        game_running = False

        # Isimler listeyse hepsine tek tek bakiyoruz
        launcher_names = [LAUNCHER_PROCESS_NAME.lower()] if isinstance(LAUNCHER_PROCESS_NAME, str) else [n.lower() for n in LAUNCHER_PROCESS_NAME]
        game_names = [GAME_PROCESS_NAME.lower()] if isinstance(GAME_PROCESS_NAME, str) else [n.lower() for n in GAME_PROCESS_NAME]

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

    def connect_rpc(self):
        """Discord'un kapisini caliyoruz."""
        if not self.connected:
            try:
                self.rpc = Presence(CLIENT_ID)
                self.rpc.connect()
                self.connected = True
                self.start_time = int(time.time()) # Sayaci sifirliyoruz
                logger.info("✅ Discord'a baglandik kanka, akıyoruz!")
                return True
            except:
                logger.warning("⚠️ Discord'u bulamadim, arkada acik mi bi bak istersen.")
                return False
        return True

    def disconnect_rpc(self):
        """Isimiz bitti, Discord'daki izimizi temizleyip kaciyoruz."""
        if self.connected:
            try:
                if self.rpc:
                    self.rpc.clear() # Durumu temizle ki asili kalmasin
                    self.rpc.close()
                logger.info("🛑 Isimiz bitti, durumunu temizledim kanka.")
            except:
                pass
            self.connected = False
            self.rpc = None
            self.last_state = None

    def update_presence(self, state_type):
        """Discord'daki o mehur kutucugu guncelliyoruz."""
        if not self.connect_rpc():
            return

        try:
            if state_type == "GAME":
                self.rpc.update(
                    details="Minecraft - Oyunda",
                    state=f"Sürüm: {MC_VERSION}",
                    large_image=LARGE_IMAGE_KEY,
                    large_text="Aesir Launcher",
                    small_image=SMALL_IMAGE_KEY,
                    small_text="Minecraft",
                    start=self.start_time
                )
                if self.last_state != "GAME":
                    logger.info("🎮 Oyuna girdin, Discord'u Minecraft moduna aldim!")
            
            elif state_type == "LAUNCHER":
                self.rpc.update(
                    details="Ana Menüde Takılıyor",
                    state="Aksiyon öncesi sessizlik...",
                    large_image=LARGE_IMAGE_KEY,
                    large_text="Aesir Launcher",
                    small_image=SMALL_IMAGE_KEY,
                    small_text="Launcher",
                    start=self.start_time
                )
                if self.last_state != "LAUNCHER":
                    logger.info("📋 Launcher acik, 'Ana Menude' diye yazdim bile.")

            self.last_state = state_type
        except:
            self.connected = False # Biseyler ters giderse baglantiyi tazeleyelim

    def run(self):
        """Asil mevzu burada donuyor kanka."""
        klasoru_pırıl_pırıl_yap() # Baslarken ortaligi bir supurelim
        logger.info(f"🚀 Gozumuz sistemde, {CHECK_INTERVAL} saniyede bir bakiyorum.")
        
        try:
            while True:
                launcher_active, game_active = self.check_processes()

                if game_active:
                    self.update_presence("GAME")
                elif launcher_active:
                    self.update_presence("LAUNCHER")
                else:
                    if self.connected:
                        self.disconnect_rpc()
                
                time.sleep(CHECK_INTERVAL)
        except KeyboardInterrupt:
            logger.info("👋 Eyvallah kanka, kapattim.")
            self.disconnect_rpc()
            klasoru_pırıl_pırıl_yap() # Kapatirken de temizligimizi yapalim

if __name__ == "__main__":
    watcher = AesirWatcher()
    
    # Script aniden olse bile atexit sayesinde arkamizi temizliyoruz
    atexit.register(watcher.disconnect_rpc)
    atexit.register(klasoru_pırıl_pırıl_yap)
    
    watcher.run()
