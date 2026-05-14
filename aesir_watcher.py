import time
import psutil
import logging
import atexit
import os
import shutil
from pypresence import Presence
from pypresence.exceptions import DiscordNotFound

# ─────────────────────────────────────────────────────────────────
# ⚙️ AYARLAR
# ─────────────────────────────────────────────────────────────────
CLIENT_ID = "1504506373654839326" 
LAUNCHER_PROCESS_NAME = "Aesir Launcher.exe" 
GAME_PROCESS_NAME = ["javaw.exe", "java.exe"] 
LARGE_IMAGE_KEY = "aesir" 
SMALL_IMAGE_KEY = "minecraft_logo" 
MC_VERSION = "1.21.8"
CHECK_INTERVAL = 5 

# ─────────────────────────────────────────────────────────────────
# 🧹 AKILLI KLASOR TEMIZLIGI
# ─────────────────────────────────────────────────────────────────
def klasoru_pırıl_pırıl_yap():
    su_an_buradayim = os.path.dirname(os.path.abspath(__file__))
    cope_gidecekler = ["__pycache__", "find_my_process.py", "launcher_example.py", "aesir_rpc.py"]
    for cop in cope_gidecekler:
        yol = os.path.join(su_an_buradayim, cop)
        if os.path.exists(yol):
            try:
                if os.path.isdir(yol):
                    shutil.rmtree(yol)
                else:
                    os.remove(yol)
            except:
                pass

# ─────────────────────────────────────────────────────────────────
# 🛠️ LOGGING AYARI
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
        launcher_running = False
        game_running = False
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
        if not self.connected:
            try:
                self.rpc = Presence(CLIENT_ID)
                self.rpc.connect()
                self.connected = True
                self.start_time = int(time.time())
                logger.info("✅ Discord RPC bağlantısı kuruldu.")
                return True
            except:
                return False
        return True

    def disconnect_rpc(self):
        if self.connected:
            try:
                if self.rpc:
                    self.rpc.clear()
                    self.rpc.close()
                logger.info("🛑 Durum temizlendi ve bağlantı kapatıldı.")
            except:
                pass
            self.connected = False
            self.rpc = None
            self.last_state = None

    def update_presence(self, state_type):
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
                    logger.info("🎮 Durum: Oyunda")
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
                    logger.info("📋 Durum: Ana Menü")
            self.last_state = state_type
        except:
            self.connected = False

    def run(self):
        klasoru_pırıl_pırıl_yap()
        logger.info(f"🚀 İzleme başladı. Kontrol aralığı: {CHECK_INTERVAL}s")
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
            self.disconnect_rpc()
            klasoru_pırıl_pırıl_yap()

if __name__ == "__main__":
    watcher = AesirWatcher()
    atexit.register(watcher.disconnect_rpc)
    atexit.register(klasoru_pırıl_pırıl_yap)
    watcher.run()
