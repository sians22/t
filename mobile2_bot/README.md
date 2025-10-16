# 🎮 GGBOT v2 - Mobile2 Global Bot

**Öğretmen ödevi için geliştirilmiş kapsamlı Mobile2 Global oyun botu**

## 📋 İçindekiler

- [Özellikler](#-özellikler)
- [Kurulum](#-kurulum)
- [Kullanım](#-kullanım)
- [Ayarlar](#-ayarlar)
- [Güvenlik](#-güvenlik)
- [Sorun Giderme](#-sorun-giderme)
- [Katkıda Bulunma](#-katkıda-bulunma)

## ✨ Özellikler

### 🧪 Potion Sistemi
- **Red Potion**: Can yüzdeliğine göre otomatik kırmızı potion kullanımı
- **Blue Potion**: Mana yüzdeliğine göre otomatik mavi potion kullanımı
- Özelleştirilebilir eşik değerleri ve tuş atamaları

### 🏴‍☠️ Hack Özellikleri
- **Wallhack**: Nesne, obje ve mobların içinden geçme
- **Restart Here**: Öldüğünde belirlenen konumda yeniden başlama
- **Upgrade Item Slot 1**: 1. slottaki iteme uzaktan upgrade yapma

### ⚔️ Savaş Sistemi
- **Mob Saldırısı**: Canavarları otomatik hedef alma
- **Stone Saldırısı**: Metinleri otomatik hedef alma
- **Grup Saldırısı**: Birden fazla gruba aynı anda saldırı
- **Base Skills**: Hava Öfke gibi hasar vermeyen becerileri otomatik kullanma
- **ESP**: Oyuncu ve stone görüntüleme

### 🏃‍♂️ Hareket Hack'leri
- **Wait Hack**: Yakın mesafede animasyon olmadan saldırı
- **Wait Hack Range**: Uzak mesafede animasyon olmadan saldırı  
- **Movement Speed**: Hareket hızını artırma
- Güvenlik seviyeleri ve algılanma karşıtı özellikler

### 📦 Item Yönetimi
- **Pickup Filter**: Sadece belirlenen itemleri toplama
- **Drop No Bonus**: Efsunsuz itemleri otomatik atma
- Item arama ve filtreleme sistemi
- Popüler item şablonları

### 👥 Oyuncu Algılama
- **Whitelist**: Güvenli oyuncu listesi
- **Player Detection**: Oyuncu algılandığında otomatik tepkiler
- **GM Detection**: GM algılandığında acil güvenlik önlemleri
- Alarm sistemi ve otomatik durdurma

### 🗺️ Rota Sistemi
- **Route Recording**: Hareket rotası kaydetme
- **Auto Route**: Kaydedilen rotayı otomatik takip etme
- Rota görselleştirme ve düzenleme
- Çoklu rota desteği

### 🎣 Balık Botu
- **Kill Fish**: Balıkları otomatik öldürme
- **Grill Fish**: Balıkları otomatik ızgara yapma
- **Drop Management**: Ölü balık ve saç boyası yönetimi
- **Dead Alarm**: Ölüm durumunda alarm
- Ayarlanabilir gecikme süreleri

### 💬 Spam Bot
- Otomatik mesaj gönderme
- Ayarlanabilir süre aralıkları
- Mesaj şablonları
- Rastgele gecikme özellikleri

## 🔧 Kurulum

### Sistem Gereksinimleri

- **İşletim Sistemi**: Windows 10/11 (64-bit)
- **Python**: 3.8 veya üzeri
- **RAM**: Minimum 4GB (8GB önerilen)
- **Disk Alanı**: 500MB boş alan

### Adım 1: Python Kurulumu

1. [Python.org](https://www.python.org/downloads/) adresinden Python'u indirin
2. Kurulum sırasında "Add Python to PATH" seçeneğini işaretleyin
3. Kurulumu tamamlayın

### Adım 2: Bot Kurulumu

```bash
# Repository'yi klonlayın
git clone <repository-url>
cd mobile2_bot

# Gerekli kütüphaneleri yükleyin
pip install -r requirements.txt

# Bot'u çalıştırın
python main.py
```

### Adım 3: İlk Kurulum

1. Bot'u ilk çalıştırdığınızda ayar dosyaları otomatik oluşturulur
2. `config/` klasöründe ayarlarınız saklanır
3. Varsayılan ayarlar güvenli değerlere ayarlıdır

## 🎯 Kullanım

### Bot'u Başlatma

1. `main.py` dosyasını çalıştırın
2. Ana pencere açıldığında "Bot Başlat" butonuna tıklayın
3. Mobile2 Global oyununu açın ve bot otomatik olarak algılar

### Hotkey'ler

- **F9**: Bot'u başlat/durdur
- **F10**: Bot'u duraklat/devam ettir
- **F11**: Acil durdurma

### Temel Ayarlar

1. **Potions** sekmesinden potion ayarlarını yapın
2. **Combat** sekmesinden savaş tercihlerinizi belirleyin
3. **Movement** sekmesinden hız ayarlarını dikkatli bir şekilde yapın
4. **Player Detection** sekmesinden güvenlik ayarlarını yapın

## ⚙️ Ayarlar

### Potion Ayarları

```
Red Potion:
- Aktif/Pasif: ✅ Aktif
- Can Yüzdesi: 50%
- Tuş: F1

Blue Potion:
- Aktif/Pasif: ✅ Aktif  
- Mana Yüzdesi: 30%
- Tuş: F2
```

### Güvenlik Ayarları

```
Player Detection:
- Whitelist: Güvenli oyuncular
- Range: 100 pixel
- Tepkiler: Bot durdur, Alarm çal

GM Detection:
- Acil Durdurma: ✅ Aktif
- Oyun Kapatma: ❌ Pasif
- Alarm: ✅ Aktif
```

### Hız Ayarları

```
Güvenli Ayarlar (Önerilen):
- Movement Speed: 100-150%
- Wait Hack: 800-1200ms
- Wait Hack Range: 800-1200ms

Dikkat: Yüksek hız değerleri ban riskini artırır!
```

## 🔒 Güvenlik

### Algılanma Karşıtı Özellikler

- **Rastgele Zamanlamalar**: İnsan benzeri davranış simülasyonu
- **Güvenlik Seviyeleri**: Low, Medium, High, Paranoid
- **Anti-Detection**: Otomatik güvenlik önlemleri
- **Player Detection**: Oyuncu algılandığında otomatik durdurma

### Güvenli Kullanım İpuçları

1. **Düşük hızlarla başlayın** ve yavaş yavaş artırın
2. **Whitelist kullanın** - tanıdık oyuncuları ekleyin
3. **GM Detection'ı aktif tutun** - otomatik güvenlik için
4. **Uzun süreli kullanmaktan kaçının** - molalar verin
5. **Ayarları kaydedin** - güvenli ayar kombinasyonlarını saklayın

### Risk Seviyeleri

| Özellik | Düşük Risk | Orta Risk | Yüksek Risk |
|---------|------------|-----------|-------------|
| Potion Bot | ✅ Güvenli | ✅ Güvenli | ✅ Güvenli |
| Combat Bot | ✅ Güvenli | ⚠️ Dikkat | ⚠️ Dikkat |
| Speed Hacks | ⚠️ Dikkat | ❌ Riskli | ❌ Riskli |
| Fishing Bot | ✅ Güvenli | ✅ Güvenli | ⚠️ Dikkat |

## 🐛 Sorun Giderme

### Sık Karşılaşılan Sorunlar

#### Bot oyunu algılamıyor
```
Çözüm:
1. Mobile2 Global'in açık olduğundan emin olun
2. Oyun penceresinin minimize olmadığından emin olun
3. Bot'u yönetici olarak çalıştırın
4. Antivirus yazılımını geçici olarak kapatın
```

#### Potion çalışmıyor
```
Çözüm:
1. Potion tuşlarının doğru ayarlandığından emin olun
2. Inventory'de potion olduğundan emin olun
3. Can/Mana yüzdelerini kontrol edin
4. Oyun penceresinin aktif olduğundan emin olun
```

#### Speed hack çalışmıyor
```
Çözüm:
1. Oyun güncellemesi sonrası normal bir durumdur
2. Güvenlik yazılımları engelliyor olabilir
3. Daha düşük hız değerleri deneyin
4. Anti-cheat sistemleri aktif olabilir
```

### Log Dosyaları

Bot otomatik olarak log dosyaları oluşturur:
- `logs/bot.log` - Genel bot kayıtları
- `logs/combat.log` - Savaş kayıtları
- `logs/detection.log` - Oyuncu algılama kayıtları

### Hata Raporlama

Hata ile karşılaştığınızda:

1. Log dosyalarını kontrol edin
2. Hatanın tekrarlanabilir olup olmadığını test edin
3. Sistem bilgilerinizi toplayın (Settings > Sistem Bilgileri)
4. Hata raporunu detaylı bir şekilde yazın

## 📁 Dosya Yapısı

```
mobile2_bot/
├── main.py                 # Ana çalıştırma dosyası
├── requirements.txt        # Python bağımlılıkları
├── README.md              # Bu dosya
├── config/                # Ayar dosyaları
│   ├── bot_settings.json  # Ana ayarlar
│   ├── routes/            # Kaydedilen rotalar
│   └── items/             # Item listeleri
├── src/                   # Kaynak kodlar
│   ├── core/              # Ana bot motoru
│   ├── gui/               # Kullanıcı arayüzü
│   ├── utils/             # Yardımcı fonksiyonlar
│   └── config/            # Ayar yönetimi
├── logs/                  # Log dosyaları
├── assets/                # Görüntü şablonları
└── backup/                # Otomatik yedekler
```

## 🤝 Katkıda Bulunma

Bu proje öğretmen ödevi olarak geliştirilmiştir. Katkıda bulunmak isterseniz:

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

### Geliştirme Kuralları

- Kod kalitesini koruyun
- Yorum satırları ekleyin
- Test edin
- Dokümantasyonu güncelleyin

## 📄 Lisans

Bu proje eğitim amaçlı geliştirilmiştir. Ticari kullanım yasaktır.

## ⚠️ Yasal Uyarı

- Bu bot sadece eğitim amaçlıdır
- Oyun kurallarını ihlal edebilir
- Kullanım riski size aittir
- Ban riskini göze alarak kullanın
- Sorumluluğu kabul ederek kullanın

## 🆘 Destek

Yardım için:
- README dosyasını okuyun
- Log dosyalarını kontrol edin
- Sorun giderme bölümünü inceleyin
- Güvenli ayarları kullanın

---

**GGBOT v2** - Mobile2 Global için kapsamlı bot çözümü 🎮✨

*Öğretmen ödevi - 2025*