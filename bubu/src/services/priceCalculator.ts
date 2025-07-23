export function calculatePrice(distanceKm: number): number {
  if (distanceKm <= 3) return 20;
  if (distanceKm <= 6) return 30;
  if (distanceKm <= 10) return 50;
  return 50 + (distanceKm - 10) * 3;
}

export function formatPrice(value: number): string {
  return `₺${value.toFixed(0)}`;
}