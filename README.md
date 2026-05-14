# 🛡️ Aesir Launcher — Discord Rich Presence (RPC)

Aesir Launcher kullanıcıları için özel olarak hazırlanmış, sistem süreçlerini izleyerek çalışan dinamik bir Discord Rich Presence (Zengin Varlık Durumu) scripti. 

![Aesthetic](https://img.shields.io/badge/Aesthetics-Premium-blueviolet?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)

## ✨ Özellikler

- 🔍 **Akıllı İzleme:** Launcher ve Minecraft süreçlerini otomatik algılar.
- 🎮 **Dinamik Durum:** Ana menüdeyken "Menüde", oyuna girdiğinde "Oyunda" yazar.
- 🚀 **Performans:** İşlemciyi yormayan (her 5sn'de bir kontrol) optimize döngü.
- 🧹 **Oto-Temizlik:** Gereksiz geçici dosyaları ve kalıntıları otomatik süpürür.
- 🛠️ **Hata Yönetimi:** Discord kapansa bile script çökmez, otomatik yeniden bağlanır.

## 🚀 Kurulum

1. **Python Yükleyin:** Bilgisayarınızda [Python](https://www.python.org/) yüklü olduğundan emin olun.
2. **Kütüphaneleri Kurun:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Konfigürasyon:** `aesir_watcher.py` dosyasını açın ve `CLIENT_ID` kısmına kendi Discord Developer ID'nizi yazın (veya varsayılanı kullanın).

## 🎮 Kullanım

Klasördeki **`Aesir_RPC_Baslat.bat`** dosyasına çift tıklamanız yeterli! Script arka planda çalışmaya başlayacak ve Discord profilinizi otomatik güncelleyecektir.

## 📁 Dosya Yapısı

- `aesir_watcher.py`: Ana script dosyası.
- `Aesir_RPC_Baslat.bat`: Windows için hızlı başlatıcı.
- `requirements.txt`: Gerekli bağımlılıklar.

## 🤝 Katkıda Bulunma

Hataları bildirmek veya yeni özellikler eklemek isterseniz bir **Issue** açabilir veya **Pull Request** gönderebilirsiniz. Kankalara kapımız her zaman açık! 😎

---
*Aesir Ekosistemi için sevgiyle hazırlandı.*
