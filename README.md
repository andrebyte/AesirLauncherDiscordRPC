# 🛡️ Aesir Launcher — Universal Discord Rich Presence (RPC)

Aesir Launcher kullanıcıları (Hem Premium hem Offline/Crack) için özel olarak hazırlanmış, dinamik bir Discord Rich Presence (Zengin Varlık Durumu) scripti. Orijinal hesabı olan veya olmayan tüm oyuncuların kendi cilt/kafa (skin) resimlerini Discord profilinde gösterir!

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![Discord](https://img.shields.io/badge/Discord-RPC-5865F2?style=for-the-badge&logo=discord)

## ✨ Özellikler

- 🧑‍🦲 **Dinamik Kafa (Avatar):** `mc-heads.net` API sayesinde isminize tanımlı skini anında Discord'a çeker.
- 🔌 **Universal Destek:** Premium ve Crack oyuncular fark etmeksizin ismi eşleşen skinleri bulur, bulamazsa hata vermeden varsayılan resme geçer.
- 🤖 **Tam Otomatik:** Launcher ile tam entegre çalışabilir veya kendi config dosyasından isminizi otomatik okuyabilir.
- 🛠️ **Hata Yönetimi:** Discord kapalı olsa bile çökmez, arka planda güvenle bekler.

## 📋 Gereksinimler

- **Python 3.8+:** Sisteminizde [Python](https://www.python.org/downloads/) yüklü olmalıdır. (Kurarken "Add Python to PATH" seçeneğini açmayı unutmayın).
- **Discord Masaüstü Uygulaması** açık olmalıdır.

## 🚀 Kurulum ve Kullanım

### 1. Bağımlılıkları Yükleyin
Klasör içindeyken CMD veya terminali açıp şu komutu girin:
```bash
pip install -r requirements.txt
```

### 2. İsminizi Ayarlayın (aesir_config.json)
Script ilk çalıştığında (veya siz oluşturduğunuzda) klasörde otomatik olarak **`aesir_config.json`** adında bir dosya oluşur. 
1. Bu dosyayı Not Defteri ile açın.
2. İçindeki `"AesirPlayer"` yazısını silip kendi **Minecraft/Aesir Launcher kullanıcı adınızı** yazın ve kaydedin.
   Örnek: `{"username": "iAndrex28"}`

*(Not: Eğer geliştiriciyseniz, scripti launcher içinden doğrudan argümanla başlatabilirsiniz: `python universal_rpc.py OYUNCU_ADI`)*

### 3. Çalıştırın!
Her şey hazır! Klasördeki **`Universal_RPC_Baslat.bat`** dosyasına çift tıklamanız yeterli. Komut penceresi anında kapanacak, script arka planda sessizce (görünmez olarak) çalışmaya başlayacak ve Discord profilinizi güncelleyecektir. 

*(Scripti kapatmak isterseniz, Windows Görev Yöneticisi -> Ayrıntılar kısmından `pythonw.exe` işlemini sonlandırabilirsiniz).*

## 🤝 Geliştirici Bilgisi & Katkıda Bulunma

Bu script Aesir Launcher ekosistemi için özel tasarlanmıştır ancak istenilen her projede rahatlıkla kullanılabilir. Katkıda bulunmak için Pull Request göndermekten çekinmeyin!
