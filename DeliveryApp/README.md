# 💖 Delivery App - Kurye Uygulaması

Bu uygulama, React Native ve Expo ile geliştirilmiş bir kurye ve teslimat uygulamasıdır. Özellikle kadın kullanıcılar için tasarlanmış güzel ve kullanıcı dostu bir arayüze sahiptir.

## ✨ Özellikler

### 👩‍💼 Müşteri Özellikleri
- **Adres Seçimi**: Alım ve teslimat adreslerini arama ve seçme
- **Mesafe Bazlı Fiyatlandırma**: 
  - 0-3 km: 20 TL
  - 3-6 km: 35 TL
  - 6-10 km: 50 TL
  - 10-15 km: 70 TL
  - 15-25 km: 100 TL
  - 25+ km: 150 TL
- **İletişim Bilgileri**: Müşteri ve alıcı telefon numaraları
- **Sipariş Onayı**: Fiyat ve detayları görüntüleme
- **Sipariş Takibi**: Animasyonlu durum göstergesi

### 🚴‍♂️ Kurye Özellikleri
- **Sipariş Listesi**: Bekleyen siparişleri görüntüleme
- **Sipariş Kabul**: Siparişleri kabul etme
- **Durum Güncelleme**: Sipariş durumunu güncelleme

### 📱 Sipariş Durumları
1. **Kurye Bekleniyor**: Sipariş için kurye aranıyor
2. **Kurye Atandı**: Kurye siparişi kabul etti
3. **Kurye Yolda**: Kurye alım noktasına gidiyor
4. **Sipariş Alındı**: Kurye siparişi teslim aldı
5. **Teslim Edildi**: Sipariş başarıyla teslim edildi

## 🚀 Kurulum

```bash
# Bağımlılıkları yükle
npm install

# Uygulamayı başlat
npx expo start

# Android için
npx expo start --android

# Web için test
npx expo start --web
```

## 🎨 Tasarım Özellikleri

- **Pembe Renk Paleti**: Kadın kullanıcılar için özel tasarım
- **Yumuşak Köşeler**: Modern ve şık görünüm
- **Animasyonlar**: Kullanıcı deneyimini artıran animasyonlar
- **İkonlar**: Anlaşılır ve güzel ikonlar
- **Gölgeler**: Derinlik hissi veren gölge efektleri

## 📁 Proje Yapısı

```
DeliveryApp/
├── components/
│   ├── AddressSelector.js     # Adres seçim bileşeni
│   ├── PriceConfirmation.js   # Fiyat onay bileşeni
│   └── OrderStatusTracker.js  # Sipariş durum takip bileşeni
├── screens/
│   ├── CustomerScreen.js      # Müşteri ana ekranı
│   ├── CourierScreen.js       # Kurye ekranı
│   └── OrderTrackingScreen.js # Sipariş takip ekranı
├── data/
│   └── pricing.js             # Fiyatlandırma verileri
├── utils/
│   └── distance.js            # Mesafe hesaplama fonksiyonları
└── App.js                     # Ana uygulama dosyası
```

## 🌟 Gelecek Özellikler

- Gerçek harita entegrasyonu
- Push bildirimler
- Ödeme sistemi entegrasyonu
- Kurye konum takibi
- Kullanıcı değerlendirme sistemi
- Sipariş geçmişi

## 💡 Kullanım

1. **Sipariş Oluşturma**:
   - Alım adresini seçin
   - Teslimat adresini seçin
   - Telefon numaralarını girin
   - Fiyatı onaylayın

2. **Sipariş Takibi**:
   - "Siparişlerimi Takip Et" butonuna tıklayın
   - Gerçek zamanlı durum güncellemelerini görün

3. **Kurye Paneli**:
   - Mevcut siparişleri görüntüleyin
   - Siparişleri kabul edin
   - Durum güncellemelerini yapın

Bu uygulama demo amaçlı hazırlanmıştır ve gerçek API entegrasyonları eklenebilir.