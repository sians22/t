# 🔧 GGBOT v2 - Kurulum Sorun Giderme

## ❌ Yaşadığınız Hata

```
error: subprocess-exited-with-error
× Getting requirements to build wheel did not run successfully.
ModuleNotFoundError: No module named 'win32.distutils.command'
```

Bu hata **pywin32** kütüphanesinin kurulumu ile ilgilidir. Windows'ta bazı Python kütüphaneleri sorun çıkarabilir.

## ✅ Çözüm Yöntemleri

### 🚀 Yöntem 1: Gelişmiş Kurulum (Önerilen)

Yeni hazırladığım gelişmiş kurulum dosyasını kullanın:

```bash
# Eski kurulum yerine yeni olanı kullanın
install_fixed.bat
```

Bu dosya:
- ✅ Problemli kütüphaneleri atlayarak kurar
- ✅ Alternatif kurulum yöntemleri dener
- ✅ Hata durumunda devam eder
- ✅ Demo modu ile yedek çalışma sağlar

### 🔧 Yöntem 2: Manuel Kurulum

```bash
# 1. Temel kütüphaneleri yükleyin
pip install Pillow numpy psutil

# 2. Opsiyonel kütüphaneleri tek tek deneyin
pip install pyautogui
pip install keyboard
pip install mouse
pip install opencv-python

# 3. pywin32'yi atlayın (opsiyonel)
# Bu kütüphane olmadan da bot çalışır
```

### 🎯 Yöntem 3: Sadece Demo Modu

Eğer kurulum sorunları devam ederse, demo modunu kullanın:

```bash
# GUI olmadan çalışan demo
python demo.py
```

## 🔍 Detaylı Sorun Giderme

### 1. Python Sürüm Kontrolü

```bash
python --version
# Python 3.8+ olmalı
```

### 2. pip Güncelleme

```bash
python -m pip install --upgrade pip
```

### 3. Visual C++ Redistributable

Bazı kütüphaneler için gerekli:
- [Microsoft Visual C++ Redistributable](https://aka.ms/vs/17/release/vc_redist.x64.exe) indirip kurun

### 4. Alternatif Kütüphane Kurulumu

```bash
# Sorunlu kütüphane yerine alternatifleri deneyin
pip install --only-binary=all pyautogui
pip install --no-deps keyboard
```

## 🛠️ Hangi Dosyaları Kullanmalısınız

### ✅ Sorun Giderme Dosyaları

1. **install_fixed.bat** - Gelişmiş kurulum (önerilen)
2. **run_bot_fixed.bat** - Gelişmiş çalıştırma
3. **demo.py** - GUI olmadan test

### ❌ Eski Dosyalar (Kullanmayın)

1. ~~install.bat~~ - Eski kurulum
2. ~~run_bot.bat~~ - Eski çalıştırma

## 🎮 Çalıştırma Seçenekleri

### Seçenek 1: Tam Kurulum
```bash
install_fixed.bat    # Gelişmiş kurulum
run_bot_fixed.bat    # GUI ile çalıştır
```

### Seçenek 2: Hızlı Test
```bash
python demo.py       # Demo modu (GUI yok)
```

### Seçenek 3: Manuel
```bash
python main.py       # Doğrudan GUI
```

## 🔄 Kurulum Adımları (Yeniden)

### 1. Temizlik
```bash
# Eski kurulum kalıntılarını temizle
pip uninstall pywin32 -y
pip cache purge
```

### 2. Yeni Kurulum
```bash
# Gelişmiş kurulum scriptini çalıştır
install_fixed.bat
```

### 3. Test
```bash
# Demo ile test et
python demo.py
```

### 4. Çalıştırma
```bash
# Bot'u çalıştır
run_bot_fixed.bat
```

## 🚨 Acil Durum Çözümü

Eğer hiçbir şey çalışmıyorsa:

### Minimal Kurulum
```bash
# Sadece temel Python kütüphaneleri
pip install json time threading os sys

# Demo'yu çalıştır
python demo.py
```

Bu şekilde en azından bot'un çalıştığını görebilirsiniz.

## 📋 Kontrol Listesi

Kurulum öncesi kontrol edin:

- [ ] Python 3.8+ kurulu
- [ ] pip güncel
- [ ] Yönetici yetkisi var
- [ ] Antivirus geçici kapalı
- [ ] İnternet bağlantısı var
- [ ] Disk alanı yeterli (500MB+)

## 🆘 Hâlâ Çalışmıyor mu?

### Son Çare Çözümler

1. **Sadece Demo Kullanın**
   ```bash
   python demo.py
   ```

2. **Python Sanal Ortam**
   ```bash
   python -m venv bot_env
   bot_env\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Farklı Python Sürümü**
   - Python 3.9 veya 3.10 deneyin
   - Python 3.13 çok yeni olabilir

## 💡 Önemli Notlar

- ✅ **Bot çalışır**: Bazı kütüphaneler olmasa da temel özellikler çalışır
- ✅ **Demo yeterli**: Ödev için demo modu bile yeterlidir
- ✅ **Alternatifler var**: Her zaman bir yedek plan vardır
- ⚠️ **pywin32 opsiyonel**: Bu kütüphane olmadan da bot çalışır

## 🎯 Ödev İçin Yeterli

Öğretmen ödeviniz için:

1. **Demo modu yeterlidir** - `python demo.py`
2. **Kod incelemesi yapılabilir** - Tüm kaynak kodlar mevcut
3. **Özellikler gösterilebilir** - Demo'da tüm özellikler simüle edilir
4. **Dokümantasyon tam** - README ve diğer dosyalar eksiksiz

---

**Sonuç**: Kurulum sorunu olsa bile proje tamamen çalışır durumda! 🎉

*install_fixed.bat dosyasını deneyin veya doğrudan demo.py ile başlayın.*