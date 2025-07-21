// Haversine formula to calculate distance between two coordinates
export const calculateDistance = (lat1, lon1, lat2, lon2) => {
  const R = 6371; // Radius of the Earth in kilometers
  const dLat = deg2rad(lat2 - lat1);
  const dLon = deg2rad(lon2 - lon1);
  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(deg2rad(lat1)) * Math.cos(deg2rad(lat2)) *
    Math.sin(dLon / 2) * Math.sin(dLon / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  const distance = R * c; // Distance in kilometers
  return distance;
};

const deg2rad = (deg) => {
  return deg * (Math.PI / 180);
};

// Mock function to simulate address search
export const searchAddresses = async (query) => {
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 500));
  
  // Mock addresses for demo
  const mockAddresses = [
    {
      id: '1',
      title: 'Kadıköy Moda',
      description: 'Moda Caddesi, Kadıköy/İstanbul',
      latitude: 40.9872,
      longitude: 29.0251,
    },
    {
      id: '2',
      title: 'Beşiktaş Merkez',
      description: 'Barbaros Bulvarı, Beşiktaş/İstanbul',
      latitude: 41.0426,
      longitude: 29.0079,
    },
    {
      id: '3',
      title: 'Taksim Meydanı',
      description: 'Taksim Meydanı, Beyoğlu/İstanbul',
      latitude: 41.0370,
      longitude: 28.9857,
    },
    {
      id: '4',
      title: 'Ataşehir AVM',
      description: 'Ataşehir Bulvarı, Ataşehir/İstanbul',
      latitude: 40.9833,
      longitude: 29.1167,
    },
    {
      id: '5',
      title: 'Levent Metro',
      description: 'Büyükdere Caddesi, Şişli/İstanbul',
      latitude: 41.0814,
      longitude: 29.0128,
    },
  ];

  return mockAddresses.filter(address =>
    address.title.toLowerCase().includes(query.toLowerCase()) ||
    address.description.toLowerCase().includes(query.toLowerCase())
  );
};