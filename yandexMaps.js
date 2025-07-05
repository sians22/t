class YandexMapsService {
  constructor() {
    this.apiKey = import.meta.env.VITE_YANDEX_MAPS_API_KEY || 'demo-key';
    this.geocodeBaseUrl = 'https://geocode-maps.yandex.ru/1.x/';
    this.suggestBaseUrl = 'https://suggest-maps.yandex.ru/v1/suggest';
  }

  // Adres önerileri al
  async getSuggestions(text, options = {}) {
    try {
      const params = new URLSearchParams({
        apikey: this.apiKey,
        text: text,
        lang: options.lang || 'tr_TR',
        results: options.results || 7,
        types: options.types || 'geo,biz',
        print_address: 1,
        ...options
      });

      const response = await fetch(`${this.suggestBaseUrl}?${params}`);
      
      if (!response.ok) {
        throw new Error(`Suggest API error: ${response.status}`);
      }

      const data = await response.json();
      return this.formatSuggestions(data);
    } catch (error) {
      console.error('Yandex Suggest API error:', error);
      // Fallback: demo önerileri döndür
      return this.getDemoSuggestions(text);
    }
  }

  // Geocoding - adres -> koordinat
  async geocodeAddress(address, options = {}) {
    try {
      const params = new URLSearchParams({
        apikey: this.apiKey,
        geocode: address,
        format: 'json',
        lang: options.lang || 'tr_TR',
        results: options.results || 1,
        ...options
      });

      const response = await fetch(`${this.geocodeBaseUrl}?${params}`);
      
      if (!response.ok) {
        throw new Error(`Geocode API error: ${response.status}`);
      }

      const data = await response.json();
      return this.formatGeocodeResponse(data);
    } catch (error) {
      console.error('Yandex Geocode API error:', error);
      // Fallback: demo koordinatlar döndür
      return this.getDemoCoordinates(address);
    }
  }

  // Reverse geocoding - koordinat -> adres
  async reverseGeocode(lat, lng, options = {}) {
    try {
      const params = new URLSearchParams({
        apikey: this.apiKey,
        geocode: `${lng},${lat}`,
        format: 'json',
        lang: options.lang || 'tr_TR',
        kind: 'house',
        ...options
      });

      const response = await fetch(`${this.geocodeBaseUrl}?${params}`);
      
      if (!response.ok) {
        throw new Error(`Reverse geocode API error: ${response.status}`);
      }

      const data = await response.json();
      return this.formatReverseGeocodeResponse(data);
    } catch (error) {
      console.error('Yandex Reverse Geocode API error:', error);
      // Fallback: demo adres döndür
      return this.getDemoAddress(lat, lng);
    }
  }

  // Önerileri formatla
  formatSuggestions(data) {
    if (!data.results) return [];

    return data.results.map(item => ({
      title: item.title?.text || '',
      subtitle: item.subtitle?.text || '',
      address: item.address?.formatted_address || '',
      coordinates: item.pos ? {
        lng: parseFloat(item.pos.split(' ')[0]),
        lat: parseFloat(item.pos.split(' ')[1])
      } : null,
      type: item.tags?.join(', ') || '',
      distance: item.distance?.text || '',
      uri: item.uri || ''
    }));
  }

  // Geocode yanıtını formatla
  formatGeocodeResponse(data) {
    const geoObjects = data?.response?.GeoObjectCollection?.featureMember || [];
    
    if (geoObjects.length === 0) {
      return null;
    }

    const geoObject = geoObjects[0].GeoObject;
    const coordinates = geoObject.Point.pos.split(' ');
    
    return {
      address: geoObject.metaDataProperty.GeocoderMetaData.text,
      coordinates: {
        lng: parseFloat(coordinates[0]),
        lat: parseFloat(coordinates[1])
      },
      precision: geoObject.metaDataProperty.GeocoderMetaData.precision,
      kind: geoObject.metaDataProperty.GeocoderMetaData.kind
    };
  }

  // Reverse geocode yanıtını formatla
  formatReverseGeocodeResponse(data) {
    const geoObjects = data?.response?.GeoObjectCollection?.featureMember || [];
    
    if (geoObjects.length === 0) {
      return null;
    }

    const geoObject = geoObjects[0].GeoObject;
    
    return {
      address: geoObject.metaDataProperty.GeocoderMetaData.text,
      components: this.parseAddressComponents(geoObject.metaDataProperty.GeocoderMetaData.Address),
      kind: geoObject.metaDataProperty.GeocoderMetaData.kind
    };
  }

  // Adres bileşenlerini parse et
  parseAddressComponents(addressData) {
    if (!addressData?.Components) return {};

    const components = {};
    addressData.Components.forEach(component => {
      components[component.kind] = component.name;
    });

    return components;
  }

  // Demo önerileri (API anahtarı yoksa)
  getDemoSuggestions(text) {
    const demoSuggestions = [
      {
        title: 'Taksim Meydanı',
        subtitle: 'Beyoğlu, İstanbul',
        address: 'Taksim Meydanı, Beyoğlu, İstanbul',
        coordinates: { lng: 28.9869, lat: 41.0369 },
        type: 'landmark',
        distance: '2.5 km'
      },
      {
        title: 'Sultanahmet Camii',
        subtitle: 'Fatih, İstanbul',
        address: 'Sultanahmet Camii, Fatih, İstanbul',
        coordinates: { lng: 28.9769, lat: 41.0054 },
        type: 'landmark',
        distance: '3.2 km'
      },
      {
        title: 'Galata Kulesi',
        subtitle: 'Beyoğlu, İstanbul',
        address: 'Galata Kulesi, Beyoğlu, İstanbul',
        coordinates: { lng: 28.9744, lat: 41.0256 },
        type: 'landmark',
        distance: '1.8 km'
      }
    ];

    return demoSuggestions.filter(item => 
      item.title.toLowerCase().includes(text.toLowerCase()) ||
      item.address.toLowerCase().includes(text.toLowerCase())
    );
  }

  // Demo koordinatlar
  getDemoCoordinates(address) {
    const demoLocations = {
      'taksim': { lng: 28.9869, lat: 41.0369 },
      'sultanahmet': { lng: 28.9769, lat: 41.0054 },
      'galata': { lng: 28.9744, lat: 41.0256 },
      'beşiktaş': { lng: 29.0027, lat: 41.0422 },
      'kadıköy': { lng: 29.0244, lat: 40.9833 }
    };

    const key = Object.keys(demoLocations).find(k => 
      address.toLowerCase().includes(k)
    );

    if (key) {
      return {
        address: address,
        coordinates: demoLocations[key],
        precision: 'exact',
        kind: 'locality'
      };
    }

    // Varsayılan İstanbul koordinatları
    return {
      address: address,
      coordinates: { lng: 28.9784, lat: 41.0082 },
      precision: 'other',
      kind: 'locality'
    };
  }

  // Demo adres
  getDemoAddress(lat, lng) {
    return {
      address: `${lat.toFixed(4)}, ${lng.toFixed(4)} koordinatları`,
      components: {
        country: 'Türkiye',
        province: 'İstanbul',
        locality: 'İstanbul',
        street: 'Demo Sokak'
      },
      kind: 'house'
    };
  }

  // Mesafe hesapla (Haversine formülü)
  calculateDistance(lat1, lng1, lat2, lng2) {
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

  // Rota hesapla (basit düz çizgi)
  calculateRoute(fromLat, fromLng, toLat, toLng) {
    const distance = this.calculateDistance(fromLat, fromLng, toLat, toLng);
    const duration = Math.max(15, Math.round(distance * 2)); // Minimum 15 dakika

    return {
      distance: Math.round(distance * 100) / 100,
      duration: duration,
      route: [
        [fromLng, fromLat],
        [toLng, toLat]
      ]
    };
  }
}

export default new YandexMapsService();

