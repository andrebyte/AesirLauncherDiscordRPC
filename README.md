# 🛡️ Aesir Launcher — Discord Rich Presence (RPC)

Aesir Launcher ve Minecraft süreçlerini sistem üzerinden izleyerek Discord profilinizde dinamik olarak gösteren profesyonel bir RPC scriptidir. Bu araç, oyunun kodlarına müdahale etmeden dışarıdan çalışır.

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![Discord](https://img.shields.io/badge/Discord-RPC-5865F2?style=for-the-badge&logo=discord)

## 📋 Gereksinimler

Scriptin çalışabilmesi için bilgisayarınızda şunların kurulu olması gerekir:
- **Python 3.8 veya üzeri:** [python.org](https://www.python.org/downloads/) adresinden indirebilirsiniz. (Kurulum sırasında "Add Python to PATH" seçeneğini işaretlemeyi unutmayın!)
- **Discord Masaüstü Uygulaması:** Web sürümü RPC desteklemez.

## 🚀 Kurulum ve Kullanım

### 1. Dosyaları İndirin
Bu depoyu indirin ve bir klasöre çıkartın.

### 2. Bağımlılıkları Yükleyin
Klasörün içindeyken terminali (veya CMD) açın ve gerekli kütüphaneleri yükleyin:
```bash
pip install -r requirements.txt
```

### 3. Konfigürasyon (Opsiyonel)
`aesir_watcher.py` dosyasını bir metin düzenleyici ile açarak en üstteki **⚙️ AYARLAR** bölümünden şu bilgileri güncelleyebilirsiniz:
- `CLIENT_ID`: Kendi Discord Application ID'nizi kullanmak isterseniz.
- `MC_VERSION`: Discord'da görünecek oyun sürümü.
- `CHECK_INTERVAL`: Sistem kontrol sıklığı (varsayılan 5 saniye).

### 4. Çalıştırma
En kolay yöntem, klasördeki **`Aesir_RPC_Baslat.bat`** dosyasına çift tıklamaktır. 
Alternatif olarak manuel başlatmak için:
```bash
python aesir_watcher.py
```

## 🔍 Script Nasıl Çalışır?

1. **İzleme:** Script her 5 saniyede bir sistemdeki aktif işlemleri kontrol eder.
2. **Algılama:**
   - Eğer `Aesir Launcher.exe` çalışıyorsa durumunuz: **"Ana Menüde Takılıyor"** olarak güncellenir.
   - Eğer `java.exe` veya `javaw.exe` (Minecraft) çalışıyorsa durumunuz: **"Minecraft - Oyunda"** olarak güncellenir.
3. **Öncelik:** Oyun açıkken launcher kapansa bile durumunuz "Oyunda" kalmaya devam eder.
4. **Kapanış:** Hem launcher hem oyun kapandığında Discord durumunuz otomatik olarak temizlenir.

## 🧹 Temizlik Özelliği
Script çalıştığında klasör içindeki şu gereksiz dosyaları otomatik olarak temizler:
- `__pycache__` klasörleri
- Eski deneme dosyaları (`find_my_process.py`, `launcher_example.py` vb.)

## 🤝 Katkıda Bulunun
Her türlü iyileştirme önerisine ve hata bildirimine açığız. Lütfen bir Pull Request göndermekten veya Issue açmaktan çekinmeyin.

---
*Aesir Ekosistemi için özel olarak geliştirilmiştir. by iandrexcb*
