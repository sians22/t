// Fiyat hesaplama utility'si
export class PriceCalculator {
  constructor() {
    this.pricingRules = [
      { minDistance: 0, maxDistance: 3, price: 15 },
      { minDistance: 3, maxDistance: 10, price: 25 },
      { minDistance: 10, maxDistance: 20, price: 40 },
      { minDistance: 20, maxDistance: 50, price: 60 },
      { minDistance: 50, maxDistance: Infinity, price: 100 }
    ];
  }

  // Mesafe hesapla (Haversine formülü)
  calculateDistance(lat1, lng1, lat2, lng2) {
    if (!lat1 || !lng1 || !lat2 || !lng2) return 0;
    
    const R = 6371; // Earth's radius in kilometers
    const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLng = (lng2 - lng1) * Math.PI / 180;
    const a = 
      Math.sin(dLat/2) * Math.sin(dLat/2) +
      Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) * 
      Math.sin(dLng/2) * Math.sin(dLng/2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    return R * c;
  }

  // Fiyat hesapla
  calculatePrice(distance, promoCode = null) {
    if (!distance || distance <= 0) return 0;

    const rule = this.pricingRules.find(r => 
      distance >= r.minDistance && distance < r.maxDistance
    );
    
    let basePrice = rule ? rule.price : this.pricingRules[this.pricingRules.length - 1].price;
    
    // Promosyon kodu uygulaması
    if (promoCode) {
      const discount = this.applyPromoCode(basePrice, promoCode);
      basePrice = discount.finalPrice;
    }

    return Math.round(basePrice * 100) / 100;
  }

  // Tahmini süre hesapla
  calculateEstimatedTime(distance) {
    if (!distance || distance <= 0) return '15 dakika';
    
    // Base time: 15 minutes for pickup + 3 minutes per km
    const baseTime = 15;
    const timePerKm = 3;
    const estimatedMinutes = baseTime + (distance * timePerKm);
    
    const hours = Math.floor(estimatedMinutes / 60);
    const minutes = Math.round(estimatedMinutes % 60);
    
    if (hours > 0) {
      return `${hours} saat ${minutes} dakika`;
    }
    return `${minutes} dakika`;
  }

  // Promosyon kodu uygula
  applyPromoCode(basePrice, promoCode) {
    const promoCodes = {
      'WELCOME10': { discount: 10, type: 'percentage', maxUses: 100 },
      'FIRST5': { discount: 5, type: 'fixed', maxUses: 50 },
      'SAVE20': { discount: 20, type: 'percentage', maxUses: 25 },
      'NEWUSER': { discount: 15, type: 'fixed', maxUses: 200 }
    };

    const promo = promoCodes[promoCode.toUpperCase()];
    if (!promo) {
      return { valid: false, message: 'Geçersiz promosyon kodu' };
    }

    let finalPrice = basePrice;
    let discountAmount = 0;

    if (promo.type === 'percentage') {
      discountAmount = basePrice * (promo.discount / 100);
      finalPrice = basePrice - discountAmount;
    } else {
      discountAmount = Math.min(promo.discount, basePrice);
      finalPrice = basePrice - discountAmount;
    }

    finalPrice = Math.max(0, finalPrice);

    return {
      valid: true,
      originalPrice: basePrice,
      finalPrice: Math.round(finalPrice * 100) / 100,
      discountAmount: Math.round(discountAmount * 100) / 100,
      promo: promo
    };
  }

  // Fiyatlandırma kurallarını güncelle
  updatePricingRules(newRules) {
    this.pricingRules = newRules;
  }

  // Mevcut fiyatlandırma kurallarını al
  getPricingRules() {
    return this.pricingRules;
  }
}

export default new PriceCalculator();

