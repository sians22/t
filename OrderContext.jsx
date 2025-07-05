import React, { createContext, useContext, useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { toast } from '@/components/ui/use-toast';
import ApiService from '@/services/api';
import { useAuth } from './AuthContext';

const OrderContext = createContext();

export const useOrders = () => {
  const context = useContext(OrderContext);
  if (!context) {
    throw new Error('useOrders must be used within an OrderProvider');
  }
  return context;
};

export const OrderProvider = ({ children }) => {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(false);
  const { t } = useTranslation();
  const { user } = useAuth();

  // Siparişleri yükle
  const loadOrders = async () => {
    if (!user) return;
    
    try {
      setLoading(true);
      const params = {
        user_id: user.id,
        role: user.role
      };
      
      const response = await ApiService.getOrders(params);
      setOrders(response.orders || []);
    } catch (error) {
      console.error('Failed to load orders:', error);
      // Fallback: localStorage'dan siparişleri yükle
      const savedOrders = localStorage.getItem('orders');
      if (savedOrders) {
        try {
          const parsedOrders = JSON.parse(savedOrders);
          setOrders(parsedOrders);
        } catch (parseError) {
          console.error('Failed to parse saved orders:', parseError);
          setOrders([]);
        }
      } else {
        setOrders([]);
      }
      
      toast({
        title: t('orders.error'),
        description: 'Siparişler yüklenirken hata oluştu, yerel veriler kullanılıyor',
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadOrders();
  }, [user]);

  // Siparişleri localStorage'a kaydet
  useEffect(() => {
    if (orders.length > 0) {
      localStorage.setItem('orders', JSON.stringify(orders));
    }
  }, [orders]);

  // Sipariş oluştur
  const createOrder = async (orderData) => {
    try {
      setLoading(true);
      
      // API'ye göndermeyi dene
      try {
        const response = await ApiService.createOrder({
          ...orderData,
          customer_id: user.id
        });
        
        if (response.order) {
          setOrders(prev => [response.order, ...prev]);
          toast({
            title: t('orders.success'),
            description: 'Sipariş başarıyla oluşturuldu',
          });
          return response.order;
        }
      } catch (apiError) {
        console.error('API create order failed, using fallback:', apiError);
        
        // Fallback: Yerel sipariş oluştur
        const newOrder = {
          id: Date.now().toString(),
          ...orderData,
          customer_id: user.id,
          status: 'pending',
          created_at: new Date().toISOString(),
          price: orderData.price || 0,
          distance: orderData.distance || 0
        };
        
        setOrders(prev => [newOrder, ...prev]);
        toast({
          title: t('orders.success'),
          description: 'Sipariş yerel olarak oluşturuldu (çevrimdışı mod)',
        });
        return newOrder;
      }
    } catch (error) {
      console.error('Failed to create order:', error);
      toast({
        title: t('orders.error'),
        description: error.message || 'Sipariş oluşturulurken hata oluştu',
        variant: "destructive",
      });
      throw error;
    } finally {
      setLoading(false);
    }
  };

  // Sipariş güncelle
  const updateOrder = async (orderId, updateData) => {
    try {
      setLoading(true);
      const response = await ApiService.updateOrder(orderId, updateData);
      
      if (response.order) {
        setOrders(prev => prev.map(order => 
          order.id === orderId ? response.order : order
        ));
        toast({
          title: t('orders.success'),
          description: 'Sipariş başarıyla güncellendi',
        });
        return response.order;
      }
    } catch (error) {
      console.error('Failed to update order:', error);
      toast({
        title: t('orders.error'),
        description: error.message || 'Sipariş güncellenirken hata oluştu',
        variant: "destructive",
      });
      throw error;
    } finally {
      setLoading(false);
    }
  };

  // Fiyat hesapla
  const calculatePrice = async (coordinates) => {
    try {
      const response = await ApiService.calculatePrice(coordinates);
      return response;
    } catch (error) {
      console.error('Failed to calculate price:', error);
      throw error;
    }
  };

  // Promosyon kodu doğrula
  const validatePromoCode = async (code, orderAmount) => {
    try {
      const response = await ApiService.validatePromoCode(code, orderAmount);
      return response;
    } catch (error) {
      console.error('Failed to validate promo code:', error);
      throw error;
    }
  };

  // Sipariş kabul et (kurye için)
  const acceptOrder = async (orderId) => {
    try {
      const response = await updateOrder(orderId, {
        status: 'accepted',
        courier_id: user.id
      });
      return response;
    } catch (error) {
      throw error;
    }
  };

  // Sipariş durumu güncelle
  const updateOrderStatus = async (orderId, status) => {
    try {
      const response = await updateOrder(orderId, { status });
      return response;
    } catch (error) {
      throw error;
    }
  };

  const value = {
    orders,
    loading,
    createOrder,
    updateOrder,
    calculatePrice,
    validatePromoCode,
    acceptOrder,
    updateOrderStatus,
    loadOrders,
  };

  return (
    <OrderContext.Provider value={value}>
      {children}
    </OrderContext.Provider>
  );
};

