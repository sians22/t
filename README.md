# GGBOT v2 - Mobile2 Global Bot

Öğretmen ödevi için geliştirilmiş kapsamlı oyun botu. Mobile2 Global oyunu için Python ile yazılmıştır.

## 🚀 Özellikler

### Potion Sistemi
- **Red Potion**: Can yüzdeliğine göre otomatik kırmızı potion kullanımı
- **Blue Potion**: Mana yüzdeliğine göre otomatik mavi potion kullanımı
- **Stop Bot**: Kırmızı pot bittiğinde bot durdurma

### Hack Özellikleri
- **Wallhack**: Nesne, Obje ve Mobların içinden geçme
- **Restart Here**: Öldüğünde belirlenen yerde yeniden başlama
- **Upgrade Item Slot 1**: 1. Slotta bulunan iteme uzaktan + basma

### Farm Sistemi
- **Farm Range**: Farm alanı belirleme
- **Fixed Position**: Alanı belirleme ve sabit pozisyon

### Saldırı Sistemi
- **Mob Saldırısı**: Canavarlara otomatik saldırı
- **Stone Saldırısı**: Metinlere otomatik saldırı
- **Grup Saldırısı**: Birden fazla gruba aynı anda saldırı
- **Base Skills**: Hava Öfke gibi hasar vermeyen base itemleri otomatik yakma

### ESP Sistemi
- **ESP Player**: Oyuncuları görüntüleme
- **ESP Stone**: Metinleri görüntüleme
- **Renk Kalibrasyonu**: Özelleştirilebilir renk ayarları

### Hız Sistemi
- **Wait Hack**: Yakın mesafede animasyon olmadan saldırı
- **Wait Hack Range**: Uzak mesafede animasyon olmadan saldırı
- **Movement Speed**: Hareket hızını değiştirme

### Item Sistemi
- **Search Item**: İtemleri arama
- **Add Item**: Seçilen itemi listeye ekleme
- **Delete Item**: Seçilen itemi silme
- **Clear Items**: Tüm itemleri temizleme
- **Pickup Filter**: Sadece listeye eklenen itemleri toplama
- **Drop No Bonus**: Efsunsuz itemleri yere atma

### Whitelist Sistemi
- **Add to Whitelist**: Oyuncuları beyaz listeye ekleme
- **Player Range**: Alan belirleme
- **Player Search**: Oyuncu ismi arama
- **If Player Actions**: Oyuncu alanına girdiğinde yapılacak işlemler

### Spam Bot
- **Text Input**: Otomatik yazılacak metin
- **Timing**: Mesaj gönderme süresi
- **Start/Stop**: Spam bot kontrolü

### Fishing Bot
- **Kill Fish**: Balıkları öldürme
- **Grill Fish**: Balıkları ızgara yapma
- **Drop Dead Fish**: Ölü balıkları yere atma
- **Drop Hair Color**: Saç boyalarını yere atma
- **Dead Alarm**: Öldüğünde alarm çalma

### Route Sistemi
- **Record Route**: Rota kaydetme
- **Route Range**: Farm alanı belirleme
- **Route Management**: Rota yönetimi
- **Auto Route**: Otomatik rota takibi

### Ayarlar
- **Save Settings**: Ayarları kaydetme
- **Load Settings**: Ayarları yükleme
- **File Management**: Dosya yönetimi

## 📦 Kurulum

### Gereksinimler
- Python 3.8+
- Windows 10/11 (önerilen)

### Adımlar
1. Projeyi klonlayın:
```bash
git clone <repository-url>
cd ggbot-v2
```

2. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

3. Botu çalıştırın:
```bash
python main.py
```

## 🎮 Kullanım

1. **Bot Başlatma**: Ana pencerede "Bot Başlat" butonuna tıklayın
2. **Ayarları Yapma**: Her sekmede istediğiniz ayarları yapın
3. **Kalibrasyon**: Gerekli sistemler için renk/pozisyon kalibrasyonu yapın
4. **Kaydetme**: Ayarlarınızı "Ayarlar" sekmesinden kaydedin

## ⚙️ Konfigürasyon

### Potion Sistemi
- HP/MP threshold değerlerini ayarlayın
- Potion tuşlarını oyununuza göre düzenleyin
- HP/MP bar koordinatlarını kalibre edin

### Saldırı Sistemi
- Saldırı tuşlarını ayarlayın
- Mob/Stone renklerini kalibre edin
- Saldırı aralığını belirleyin

### ESP Sistemi
- Player/Stone renklerini kalibre edin
- ESP penceresini istediğiniz konuma yerleştirin

### Item Sistemi
- Toplanacak itemleri listeye ekleyin
- Item renklerini kalibre edin
- Toplama aralığını ayarlayın

## 🔧 Gelişmiş Ayarlar

### Renk Kalibrasyonu
Çoğu sistem için renk kalibrasyonu gereklidir:
1. İlgili sekmede "Kalibre Et" butonuna tıklayın
2. Mouse ile rengi seçin
3. Sistem otomatik olarak renk aralığını hesaplayacaktır

### Pozisyon Kalibrasyonu
Farm ve potion sistemleri için pozisyon kalibrasyonu:
1. "Pozisyonu Kaydet" butonuna tıklayın
2. Mouse ile bölgeyi seçin
3. Sistem koordinatları kaydedecektir

## 📁 Dosya Yapısı

```
ggbot-v2/
├── main.py                 # Ana bot dosyası
├── requirements.txt        # Gerekli paketler
├── README.md              # Bu dosya
├── modules/               # Bot modülleri
│   ├── potion_system.py   # Potion sistemi
│   ├── attack_system.py   # Saldırı sistemi
│   ├── esp_system.py      # ESP sistemi
│   ├── speed_system.py    # Hız sistemi
│   └── item_system.py     # Item sistemi
├── data/                  # Veri dosyaları
│   └── items.json         # Item listesi
├── routes/                # Kaydedilmiş rotalar
└── settings/              # Bot ayarları
    └── settings.json      # Varsayılan ayarlar
```

## ⚠️ Uyarılar

- Bu bot eğitim amaçlı geliştirilmiştir
- Oyun kurallarına uygun kullanın
- Ban riski olabilir, dikkatli kullanın
- Sadece kendi hesabınızda kullanın

## 🐛 Sorun Giderme

### Bot Çalışmıyor
- Python sürümünü kontrol edin (3.8+)
- Gerekli paketlerin yüklü olduğundan emin olun
- Windows sürümünü kontrol edin

### Renk Tespiti Çalışmıyor
- Renk kalibrasyonu yapın
- Oyun grafik ayarlarını kontrol edin
- Ekran çözünürlüğünü kontrol edin

### Saldırı Sistemi Çalışmıyor
- Saldırı tuşlarını kontrol edin
- Mob/Stone renklerini kalibre edin
- Saldırı aralığını artırın

## 📞 Destek

Sorunlar için GitHub Issues kullanın veya öğretmeninize danışın.

## 📄 Lisans

Bu proje eğitim amaçlı geliştirilmiştir. Ticari kullanım yasaktır.

## 🔄 Güncellemeler

### v2.0.0
- İlk sürüm
- Tüm temel özellikler eklendi
- Modüler yapı oluşturuldu
- GUI arayüzü geliştirildi

---

**Not**: Bu bot sadece eğitim amaçlı geliştirilmiştir. Oyun kurallarına uygun kullanın ve ban riskini göz önünde bulundurun.