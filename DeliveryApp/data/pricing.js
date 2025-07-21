export const PRICING_TIERS = [
  { minKm: 0, maxKm: 3, price: 20 },
  { minKm: 3, maxKm: 6, price: 35 },
  { minKm: 6, maxKm: 10, price: 50 },
  { minKm: 10, maxKm: 15, price: 70 },
  { minKm: 15, maxKm: 25, price: 100 },
  { minKm: 25, maxKm: Infinity, price: 150 },
];

export const calculatePrice = (distance) => {
  const tier = PRICING_TIERS.find(tier => 
    distance >= tier.minKm && distance < tier.maxKm
  );
  return tier ? tier.price : PRICING_TIERS[PRICING_TIERS.length - 1].price;
};

export const formatPrice = (price) => {
  return `${price} TL`;
};

export const getDistanceText = (distance) => {
  return `${distance.toFixed(1)} km`;
};