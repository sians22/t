import React, { useState, useEffect, useRef } from 'react';
import { MapPin, Navigation, Route, X } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { toast } from '@/components/ui/use-toast';
import { useTranslation } from 'react-i18next';

const RouteMapComponent = ({ 
  pickupLocation, 
  deliveryLocation, 
  onRouteCalculated, 
  apiKey,
  showRoute = true 
}) => {
  const [mapInstance, setMapInstance] = useState(null);
  const [mapLoaded, setMapLoaded] = useState(false);
  const [routeInstance, setRouteInstance] = useState(null);
  const [routeInfo, setRouteInfo] = useState(null);
  const mapRef = useRef(null);
  const { t } = useTranslation();

  useEffect(() => {
    // Load Yandex Maps API
    if (!window.ymaps) {
      const script = document.createElement('script');
      script.src = `https://api-maps.yandex.ru/2.1/?apikey=${apiKey || 'your-api-key'}&lang=tr_TR`;
      script.onload = () => {
        window.ymaps.ready(() => {
          setMapLoaded(true);
        });
      };
      document.head.appendChild(script);
    } else {
      setMapLoaded(true);
    }
  }, [apiKey]);

  useEffect(() => {
    if (mapLoaded && mapRef.current && !mapInstance) {
      const map = new window.ymaps.Map(mapRef.current, {
        center: [41.0082, 28.9784], // Istanbul coordinates
        zoom: 10,
        controls: ['zoomControl', 'fullscreenControl']
      });

      setMapInstance(map);
    }
  }, [mapLoaded]);

  useEffect(() => {
    if (mapInstance && pickupLocation && deliveryLocation && showRoute) {
      createRoute();
    } else if (mapInstance && routeInstance) {
      // Clear existing route
      mapInstance.geoObjects.remove(routeInstance);
      setRouteInstance(null);
      setRouteInfo(null);
    }
  }, [mapInstance, pickupLocation, deliveryLocation, showRoute]);

  const createRoute = () => {
    if (!mapInstance || !pickupLocation || !deliveryLocation) return;

    // Clear existing route
    if (routeInstance) {
      mapInstance.geoObjects.remove(routeInstance);
    }

    // Create route points
    const referencePoints = [
      [pickupLocation.lat, pickupLocation.lng],
      [deliveryLocation.lat, deliveryLocation.lng]
    ];

    // Create multiRoute instance
    const multiRoute = new window.ymaps.multiRouter.MultiRoute({
      referencePoints: referencePoints,
      params: {
        routingMode: 'auto' // auto, masstransit, pedestrian
      }
    }, {
      boundsAutoApply: true,
      routeActiveStrokeWidth: 6,
      routeActiveStrokeColor: '#8B5CF6', // Purple color
      routeStrokeWidth: 4,
      routeStrokeColor: '#A855F7',
      wayPointStartIconLayout: 'default#imageWithContent',
      wayPointStartIconImageHref: 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTEyIDJDOC4xMyAyIDUgNS4xMyA1IDlDNSAxNC4yNSAxMiAyMiAxMiAyMkMxMiAyMiAxOSAxNC4yNSAxOSA5QzE5IDUuMTMgMTUuODcgMiAxMiAyWk0xMiAxMS41QzEwLjYyIDExLjUgOS41IDEwLjM4IDkuNSA5QzkuNSA3LjYyIDEwLjYyIDYuNSAxMiA2LjVDMTMuMzggNi41IDE0LjUgNy42MiAxNC41IDlDMTQuNSAxMC4zOCAxMy4zOCAxMS41IDEyIDExLjVaIiBmaWxsPSIjMTBCOTgxIi8+Cjwvc3ZnPgo=',
      wayPointStartIconImageSize: [24, 24],
      wayPointFinishIconLayout: 'default#imageWithContent',
      wayPointFinishIconImageHref: 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTEyIDJDOC4xMyAyIDUgNS4xMyA1IDlDNSAxNC4yNSAxMiAyMiAxMiAyMkMxMiAyMiAxOSAxNC4yNSAxOSA5QzE5IDUuMTMgMTUuODcgMiAxMiAyWk0xMiAxMS41QzEwLjYyIDExLjUgOS41IDEwLjM4IDkuNSA5QzkuNSA3LjYyIDEwLjYyIDYuNSAxMiA2LjVDMTMuMzggNi41IDE0LjUgNy42MiAxNC41IDlDMTQuNSAxMC4zOCAxMy4zOCAxMS41IDEyIDExLjVaIiBmaWxsPSIjRUY0NDQ0Ii8+Cjwvc3ZnPgo=',
      wayPointFinishIconImageSize: [24, 24]
    });

    // Add route to map
    mapInstance.geoObjects.add(multiRoute);
    setRouteInstance(multiRoute);

    // Listen for route calculation completion
    multiRoute.model.events.add('requestsuccess', () => {
      const activeRoute = multiRoute.getActiveRoute();
      if (activeRoute) {
        const distance = activeRoute.properties.get('distance');
        const duration = activeRoute.properties.get('duration');
        
        const routeData = {
          distance: Math.round(distance.value / 1000 * 100) / 100, // Convert to km
          duration: Math.round(duration.value / 60), // Convert to minutes
          distanceText: distance.text,
          durationText: duration.text
        };
        
        setRouteInfo(routeData);
        
        if (onRouteCalculated) {
          onRouteCalculated(routeData);
        }

        toast({
          title: "Rota Hesaplandı",
          description: `Mesafe: ${routeData.distance} km, Süre: ${routeData.duration} dakika`,
        });
      }
    });

    multiRoute.model.events.add('requestfail', () => {
      toast({
        title: "Rota Hatası",
        description: "Rota hesaplanamadı. Lütfen farklı konumlar deneyin.",
        variant: "destructive",
      });
    });
  };

  const clearRoute = () => {
    if (mapInstance && routeInstance) {
      mapInstance.geoObjects.remove(routeInstance);
      setRouteInstance(null);
      setRouteInfo(null);
      
      if (onRouteCalculated) {
        onRouteCalculated(null);
      }
    }
  };

  if (!mapLoaded) {
    return (
      <div className="space-y-4">
        <div className="h-64 bg-gray-100 flex items-center justify-center">
          <div className="text-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mx-auto mb-2"></div>
            <p className="text-sm text-gray-600">Harita yükleniyor...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {/* Route Controls */}
      <div className="flex gap-2 items-center">
        <div className="flex items-center gap-2 text-white">
          <Route className="w-5 h-5 text-purple-400" />
          <span className="text-sm font-medium">Rota Görünümü</span>
        </div>
        
        {routeInstance && (
          <Button
            type="button"
            variant="outline"
            onClick={clearRoute}
            size="sm"
            className="bg-red-500/20 border-red-500/30 text-red-300 hover:bg-red-500/30"
          >
            <X className="w-4 h-4 mr-1" />
            Rotayı Temizle
          </Button>
        )}
      </div>

      {/* Map Container */}
      <div 
        ref={mapRef}
        className="h-80 border-2 border-purple-500/30 rounded-lg overflow-hidden"
      />

      {/* Route Information */}
      {routeInfo && (
        <div className="bg-purple-500/20 border border-purple-500/30 rounded-lg p-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-purple-300">
                {routeInfo.distance} km
              </div>
              <div className="text-sm text-purple-400">Mesafe</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-purple-300">
                {routeInfo.duration} dk
              </div>
              <div className="text-sm text-purple-400">Tahmini Süre</div>
            </div>
          </div>
        </div>
      )}

      {/* Location Information */}
      {pickupLocation && deliveryLocation && (
        <div className="space-y-2">
          <div className="flex items-center gap-2 text-sm text-gray-300">
            <div className="w-3 h-3 bg-green-500 rounded-full"></div>
            <span>Alış: {pickupLocation.lat.toFixed(4)}, {pickupLocation.lng.toFixed(4)}</span>
          </div>
          <div className="flex items-center gap-2 text-sm text-gray-300">
            <div className="w-3 h-3 bg-red-500 rounded-full"></div>
            <span>Teslimat: {deliveryLocation.lat.toFixed(4)}, {deliveryLocation.lng.toFixed(4)}</span>
          </div>
        </div>
      )}
    </div>
  );
};

export default RouteMapComponent;

