# 📥 GGBOT v2 Kurulum Rehberi

Bu rehber GGBOT v2'yi adım adım kurmanızı sağlar.

## 🔧 Sistem Gereksinimleri

### Minimum Gereksinimler
- **İşletim Sistemi**: Windows 10 (64-bit)
- **RAM**: 4GB
- **Disk Alanı**: 500MB
- **Python**: 3.8+
- **İnternet**: Kurulum için gerekli

### Önerilen Gereksinimler
- **İşletim Sistemi**: Windows 11 (64-bit)
- **RAM**: 8GB
- **Disk Alanı**: 1GB
- **Python**: 3.11+
- **Antivirus**: Geçici olarak kapatılabilir

## 📋 Kurulum Öncesi Hazırlık

### 1. Python Kurulumu

#### Adım 1: Python İndirme
1. [Python.org](https://www.python.org/downloads/) adresine gidin
2. "Download Python 3.11.x" butonuna tıklayın
3. İndirilen dosyayı çalıştırın

#### Adım 2: Python Kurulum
```
Kurulum Seçenekleri:
☑️ Add Python to PATH (ÖNEMLİ!)
☑️ Install for all users
☑️ Add Python to environment variables
```

#### Adım 3: Kurulum Doğrulama
```bash
# Komut satırını açın (cmd) ve test edin:
python --version
pip --version
```

### 2. Git Kurulumu (Opsiyonel)
1. [Git-scm.com](https://git-scm.com/download/win) adresinden Git'i indirin
2. Varsayılan ayarlarla kurun

## 🚀 Bot Kurulumu

### Yöntem 1: Git ile Kurulum (Önerilen)

```bash
# 1. Klasör oluşturun
mkdir C:\GGBOT
cd C:\GGBOT

# 2. Repository'yi klonlayın
git clone <repository-url> .

# 3. Bağımlılıkları yükleyin
pip install -r requirements.txt

# 4. Bot'u çalıştırın
python main.py
```

### Yöntem 2: Manuel Kurulum

1. **Dosyaları İndirin**
   - ZIP dosyasını indirin ve çıkarın
   - `C:\GGBOT` klasörüne kopyalayın

2. **Bağımlılıkları Yükleyin**
   ```bash
   cd C:\GGBOT
   pip install -r requirements.txt
   ```

3. **Bot'u Çalıştırın**
   ```bash
   python main.py
   ```

## 📦 Gerekli Kütüphaneler

Bot aşağıdaki Python kütüphanelerini kullanır:

```
tkinter          # GUI (Python ile birlikte gelir)
Pillow==10.0.1   # Görüntü işleme
pyautogui==0.9.54 # Otomatik kontrol
keyboard==0.13.5  # Klavye kontrolü
mouse==0.7.1      # Mouse kontrolü
psutil==5.9.6     # Sistem bilgileri
opencv-python==4.8.1.78 # Görüntü tanıma
numpy==1.24.3     # Matematik işlemleri
```

### Manuel Kütüphane Kurulumu

Eğer `requirements.txt` çalışmazsa, kütüphaneleri tek tek kurun:

```bash
pip install Pillow==10.0.1
pip install pyautogui==0.9.54
pip install keyboard==0.13.5
pip install mouse==0.7.1
pip install psutil==5.9.6
pip install opencv-python==4.8.1.78
pip install numpy==1.24.3
```

## 🔧 Kurulum Sonrası Ayarlar

### 1. İlk Çalıştırma

```bash
cd C:\GGBOT
python main.py
```

### 2. Klasör Yapısı Kontrolü

Kurulum sonrası aşağıdaki klasörler oluşmalı:

```
C:\GGBOT\
├── main.py
├── requirements.txt
├── README.md
├── config\          # ✅ Otomatik oluşur
├── src\
├── logs\            # ✅ Otomatik oluşur
├── assets\          # ✅ Otomatik oluşur
└── backup\          # ✅ Otomatik oluşur
```

### 3. Ayar Dosyası Oluşturma

İlk çalıştırmada `config/bot_settings.json` otomatik oluşur:

```json
{
  "red_potion": {
    "enabled": true,
    "health_percentage": 50,
    "key": "F1"
  },
  "blue_potion": {
    "enabled": true,
    "mana_percentage": 30,
    "key": "F2"
  }
}
```

## 🎮 Mobile2 Global Ayarları

### 1. Oyun Ayarları

Bot'un düzgün çalışması için oyunda aşağıdaki ayarları yapın:

```
Grafik Ayarları:
- Pencere Modu: Tam Ekran değil, Pencere
- Çözünürlük: 1024x768 veya üzeri
- FPS Limit: 60 FPS

Kontrol Ayarları:
- Potion Tuşları: F1 (Red), F2 (Blue)
- Saldırı: Sol Tık
- Hareket: Sağ Tık
```

### 2. Oyun Penceresi

- Oyun penceresini minimize etmeyin
- Başka pencereler oyun penceresini kapatmasın
- Oyun penceresinin başlığında "Mobile2 Global" yazsın

## 🛡️ Güvenlik Ayarları

### 1. Antivirus Ayarları

Bazı antivirus yazılımları bot'u tehdit olarak algılayabilir:

```
Windows Defender:
1. Windows Security'yi açın
2. Virus & threat protection
3. Manage settings
4. Add or remove exclusions
5. C:\GGBOT klasörünü ekleyin
```

### 2. Firewall Ayarları

```
Windows Firewall:
1. Windows Defender Firewall'u açın
2. Allow an app through firewall
3. Python.exe'yi ekleyin
4. Private ve Public network'leri işaretleyin
```

## 🔍 Kurulum Testi

### 1. Bot Testi

```bash
# Bot'u test modunda çalıştırın
python main.py --test
```

### 2. Fonksiyon Testleri

Bot açıldığında aşağıdaki testleri yapın:

```
✅ GUI açılıyor mu?
✅ Ayarlar kaydediliyor mu?
✅ Hotkey'ler çalışıyor mu? (F9, F10, F11)
✅ Oyun algılanıyor mu?
✅ Log dosyaları oluşuyor mu?
```

## ❌ Sorun Giderme

### Yaygın Kurulum Sorunları

#### 1. "Python bulunamadı" Hatası
```bash
# Çözüm:
# Python'u PATH'e ekleyin veya tam yol kullanın
C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\python.exe main.py
```

#### 2. "pip bulunamadı" Hatası
```bash
# Çözüm:
python -m pip install -r requirements.txt
```

#### 3. "Modül bulunamadı" Hatası
```bash
# Çözüm:
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

#### 4. "İzin reddedildi" Hatası
```bash
# Çözüm:
# Komut satırını yönetici olarak çalıştırın
# veya
pip install --user -r requirements.txt
```

#### 5. "tkinter bulunamadı" Hatası
```bash
# Çözüm (Linux/Mac):
sudo apt-get install python3-tk  # Ubuntu/Debian
brew install python-tk           # macOS

# Windows'ta tkinter Python ile birlikte gelir
```

### Performans Sorunları

#### 1. Yavaş Başlangıç
```
Çözümler:
- SSD kullanın
- Antivirus taramasını geçici olarak kapatın
- Python'u SSD'ye kurun
- Bot klasörünü antivirus istisnalarına ekleyin
```

#### 2. Yüksek CPU Kullanımı
```
Çözümler:
- Performance ayarlarından CPU limitini düşürün
- Update frequency'yi artırın (daha az güncelleme)
- Gereksiz özellikleri kapatın
```

## 🔄 Güncelleme

### Otomatik Güncelleme (Git ile)
```bash
cd C:\GGBOT
git pull origin main
pip install -r requirements.txt --upgrade
```

### Manuel Güncelleme
1. Yeni sürümü indirin
2. Eski dosyaların üzerine yazın
3. `config/` klasörünü koruyun
4. Bağımlılıkları güncelleyin

## 🗂️ Yedekleme

### Ayar Yedekleme
```bash
# Ayarları yedekleyin
copy config\bot_settings.json backup\settings_backup.json

# Rotaları yedekleyin
xcopy config\routes backup\routes /E /I

# Item listelerini yedekleyin
xcopy config\items backup\items /E /I
```

### Otomatik Yedekleme

Bot otomatik yedekleme yapacak şekilde ayarlanabilir:
- Settings > Backup > Auto Backup ✅
- Yedekleme aralığı: 24 saat (önerilen)

## 📞 Destek

Kurulum sorunları için:

1. **Log dosyalarını kontrol edin**: `logs/bot.log`
2. **Sistem bilgilerini toplayın**: Settings > Sistem Bilgileri
3. **Hata mesajını tam olarak kaydedin**
4. **Kurulum adımlarını tekrar kontrol edin**

### Hızlı Destek Kontrol Listesi

```
☐ Python 3.8+ kurulu mu?
☐ Tüm kütüphaneler yüklenmiş mi?
☐ Antivirus engellemiyor mu?
☐ Oyun açık ve algılanıyor mu?
☐ Ayar dosyaları oluşmuş mu?
☐ Log dosyalarında hata var mı?
```

---

## 🎉 Kurulum Tamamlandı!

Kurulum başarıyla tamamlandıysa:

1. `python main.py` ile bot'u çalıştırın
2. Mobile2 Global'i açın
3. Bot'ta "Bot Başlat" butonuna tıklayın
4. Ayarları ihtiyacınıza göre düzenleyin

**İyi oyunlar! 🎮**

---

*GGBOT v2 Kurulum Rehberi - 2025*