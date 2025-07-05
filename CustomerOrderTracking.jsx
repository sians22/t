import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { MapPin, Clock, User, Phone, Package, CheckCircle, Truck, Navigation } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { useTranslation } from 'react-i18next';
import RouteMapComponent from './RouteMapComponent';

const CustomerOrderTracking = ({ order, onClose }) => {
  const { t } = useTranslation();
  const [currentTime, setCurrentTime] = useState(new Date());

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTime(new Date());
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  const getStatusColor = (status) => {
    switch (status) {
      case 'pending':
        return 'bg-yellow-500/20 text-yellow-300 border-yellow-500/30';
      case 'accepted':
        return 'bg-blue-500/20 text-blue-300 border-blue-500/30';
      case 'in-transit':
        return 'bg-purple-500/20 text-purple-300 border-purple-500/30';
      case 'delivered':
        return 'bg-green-500/20 text-green-300 border-green-500/30';
      default:
        return 'bg-gray-500/20 text-gray-300 border-gray-500/30';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'pending':
        return <Clock className="w-4 h-4" />;
      case 'accepted':
        return <CheckCircle className="w-4 h-4" />;
      case 'in-transit':
        return <Truck className="w-4 h-4" />;
      case 'delivered':
        return <Package className="w-4 h-4" />;
      default:
        return <Clock className="w-4 h-4" />;
    }
  };

  const formatTime = (date) => {
    return new Date(date).toLocaleTimeString('tr-TR', {
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const formatDate = (date) => {
    return new Date(date).toLocaleDateString('tr-TR', {
      day: 'numeric',
      month: 'long',
      year: 'numeric'
    });
  };

  if (!order) return null;

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        exit={{ opacity: 0, scale: 0.9 }}
        className="bg-gradient-to-br from-purple-900/90 to-blue-900/90 backdrop-blur-lg rounded-xl border border-white/20 max-w-4xl w-full max-h-[90vh] overflow-y-auto"
      >
        <div className="p-6">
          {/* Header */}
          <div className="flex items-center justify-between mb-6">
            <div>
              <h2 className="text-2xl font-bold text-white">
                {t('order.id', { id: order.id })}
              </h2>
              <p className="text-gray-300">
                {formatDate(order.createdAt)} - {formatTime(order.createdAt)}
              </p>
            </div>
            <Button
              variant="outline"
              onClick={onClose}
              className="bg-white/10 border-white/20 text-white hover:bg-white/20"
            >
              Kapat
            </Button>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Order Details */}
            <div className="space-y-6">
              {/* Status */}
              <Card className="glass-effect border-white/20">
                <CardHeader>
                  <CardTitle className="text-white flex items-center gap-2">
                    {getStatusIcon(order.status)}
                    Sipariş Durumu
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <Badge className={`${getStatusColor(order.status)} border`}>
                    {t(`order.status.${order.status}`)}
                  </Badge>
                  
                  {order.status === 'in-transit' && (
                    <div className="mt-4 p-3 bg-purple-500/20 rounded-lg border border-purple-500/30">
                      <div className="flex items-center gap-2 text-purple-300">
                        <Navigation className="w-4 h-4" />
                        <span className="text-sm font-medium">Kurye yolda</span>
                      </div>
                      <p className="text-xs text-purple-400 mt-1">
                        Siparişiniz teslimat adresine doğru yola çıktı
                      </p>
                    </div>
                  )}
                </CardContent>
              </Card>

              {/* Order Info */}
              <Card className="glass-effect border-white/20">
                <CardHeader>
                  <CardTitle className="text-white flex items-center gap-2">
                    <Package className="w-5 h-5" />
                    Sipariş Bilgileri
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <p className="text-gray-300 text-sm">Açıklama</p>
                    <p className="text-white font-medium">{order.description}</p>
                  </div>
                  
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <p className="text-gray-300 text-sm">{t('order.distance')}</p>
                      <p className="text-white font-medium">{order.distance?.toFixed(2)} km</p>
                    </div>
                    <div>
                      <p className="text-gray-300 text-sm">{t('order.price')}</p>
                      <p className="text-white font-medium">{order.price} TL</p>
                    </div>
                  </div>

                  {order.promoCode && (
                    <div className="p-3 bg-green-500/20 rounded-lg border border-green-500/30">
                      <p className="text-green-300 text-sm">
                        💰 Promosyon kodu uygulandı: <span className="font-medium">{order.promoCode}</span>
                      </p>
                    </div>
                  )}
                </CardContent>
              </Card>

              {/* Courier Info */}
              {order.courier && (
                <Card className="glass-effect border-white/20">
                  <CardHeader>
                    <CardTitle className="text-white flex items-center gap-2">
                      <User className="w-5 h-5" />
                      Kurye Bilgileri
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-3">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
                        <User className="w-5 h-5 text-white" />
                      </div>
                      <div>
                        <p className="text-white font-medium">{order.courier.name}</p>
                        <p className="text-gray-300 text-sm">Kurye</p>
                      </div>
                    </div>
                    
                    {order.courier.phone && (
                      <div className="flex items-center gap-2 text-gray-300">
                        <Phone className="w-4 h-4" />
                        <span className="text-sm">{order.courier.phone}</span>
                      </div>
                    )}
                  </CardContent>
                </Card>
              )}

              {/* Contact Info */}
              <Card className="glass-effect border-white/20">
                <CardHeader>
                  <CardTitle className="text-white flex items-center gap-2">
                    <Phone className="w-5 h-5" />
                    İletişim Bilgileri
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="flex items-center gap-2 text-gray-300">
                    <Phone className="w-4 h-4" />
                    <span className="text-sm">{order.customerPhone}</span>
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Map */}
            <div className="space-y-6">
              {/* Locations */}
              <Card className="glass-effect border-white/20">
                <CardHeader>
                  <CardTitle className="text-white flex items-center gap-2">
                    <MapPin className="w-5 h-5" />
                    Konum Bilgileri
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="space-y-3">
                    <div className="flex items-start gap-3">
                      <div className="w-3 h-3 bg-green-500 rounded-full mt-1.5"></div>
                      <div>
                        <p className="text-green-300 font-medium text-sm">Alış Konumu</p>
                        <p className="text-gray-300 text-xs">
                          {order.pickupLocation?.lat?.toFixed(4)}, {order.pickupLocation?.lng?.toFixed(4)}
                        </p>
                      </div>
                    </div>
                    
                    <div className="flex items-start gap-3">
                      <div className="w-3 h-3 bg-red-500 rounded-full mt-1.5"></div>
                      <div>
                        <p className="text-red-300 font-medium text-sm">Teslimat Konumu</p>
                        <p className="text-gray-300 text-xs">
                          {order.deliveryLocation?.lat?.toFixed(4)}, {order.deliveryLocation?.lng?.toFixed(4)}
                        </p>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Route Map */}
              {order.pickupLocation && order.deliveryLocation && (
                <Card className="glass-effect border-white/20">
                  <CardHeader>
                    <CardTitle className="text-white flex items-center gap-2">
                      <Navigation className="w-5 h-5" />
                      Rota Haritası
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <RouteMapComponent
                      pickupLocation={order.pickupLocation}
                      deliveryLocation={order.deliveryLocation}
                      showRoute={true}
                      onRouteCalculated={(routeData) => {
                        console.log('Route data:', routeData);
                      }}
                    />
                  </CardContent>
                </Card>
              )}
            </div>
          </div>

          {/* Timeline */}
          <Card className="glass-effect border-white/20 mt-6">
            <CardHeader>
              <CardTitle className="text-white flex items-center gap-2">
                <Clock className="w-5 h-5" />
                Sipariş Geçmişi
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex items-center gap-4">
                  <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center">
                    <Package className="w-4 h-4 text-white" />
                  </div>
                  <div>
                    <p className="text-white font-medium">Sipariş oluşturuldu</p>
                    <p className="text-gray-300 text-sm">
                      {formatDate(order.createdAt)} - {formatTime(order.createdAt)}
                    </p>
                  </div>
                </div>

                {order.acceptedAt && (
                  <div className="flex items-center gap-4">
                    <div className="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center">
                      <CheckCircle className="w-4 h-4 text-white" />
                    </div>
                    <div>
                      <p className="text-white font-medium">Sipariş kabul edildi</p>
                      <p className="text-gray-300 text-sm">
                        {formatDate(order.acceptedAt)} - {formatTime(order.acceptedAt)}
                      </p>
                    </div>
                  </div>
                )}

                {order.status === 'in-transit' && (
                  <div className="flex items-center gap-4">
                    <div className="w-8 h-8 bg-purple-500 rounded-full flex items-center justify-center">
                      <Truck className="w-4 h-4 text-white" />
                    </div>
                    <div>
                      <p className="text-white font-medium">Kurye yolda</p>
                      <p className="text-gray-300 text-sm">
                        Şu anda: {formatTime(currentTime)}
                      </p>
                    </div>
                  </div>
                )}

                {order.deliveredAt && (
                  <div className="flex items-center gap-4">
                    <div className="w-8 h-8 bg-emerald-500 rounded-full flex items-center justify-center">
                      <CheckCircle className="w-4 h-4 text-white" />
                    </div>
                    <div>
                      <p className="text-white font-medium">Sipariş teslim edildi</p>
                      <p className="text-gray-300 text-sm">
                        {formatDate(order.deliveredAt)} - {formatTime(order.deliveredAt)}
                      </p>
                    </div>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        </div>
      </motion.div>
    </div>
  );
};

export default CustomerOrderTracking;

