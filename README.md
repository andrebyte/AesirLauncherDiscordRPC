# 🛡️ Aesir Launcher — Universal Discord Rich Presence (RPC)

Aesir Launcher kullanıcıları (Hem Premium hem Offline/Crack) için özel olarak hazırlanmış, dinamik bir Discord Rich Presence (Zengin Varlık Durumu) scripti. 

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![Discord](https://img.shields.io/badge/Discord-RPC-5865F2?style=for-the-badge&logo=discord)

## ✨ Özellikler

- 🧑‍🦲 **Dinamik Kafa (Avatar):** `mc-heads.net` API sayesinde isminize tanımlı skini anında Discord'a çeker.
- 🖼️ **Full Görsel Entegrasyon:** Sağ alt köşede küçük Aesir logonuzu, büyük ekranda ise karakterinizi yansıtır.
- 🤖 **Tam Otomatik İzleyici (Hayalet Mod):** Arka planda gizlice çalışır. Sadece launcher ve oyun açıldığında Discord'da görünür, kapandığında otomatik silinir.
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

### 2. İsminizi Ayarlayın
**`universal_rpc.py`** (veya `universal_rpc.pyw` yaptıysanız onu) bir metin düzenleyiciyle açın. En üstteki ayarlarda bulunan `MY_USERNAME` karşısına kendi oyuncu adınızı yazın ve kaydedin:
```python
MY_USERNAME = "SizinOyuncuAdiniz" 
```

### 3. Çalıştırın!
Her şey hazır! Klasördeki **`Universal_RPC_Baslat.bat`** dosyasına çift tıklamanız yeterli. Komut penceresi anında kapanacak, script arka planda sessizce (görünmez olarak) çalışmaya başlayacak ve Discord profilinizi güncelleyecektir. 

*(Scripti kapatmak isterseniz, Windows Görev Yöneticisi -> Ayrıntılar kısmından `pythonw.exe` işlemini sonlandırabilirsiniz).*
