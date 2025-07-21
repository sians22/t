import React, { useState } from 'react';
import { StatusBar } from 'expo-status-bar';
import { StyleSheet, View } from 'react-native';
import CustomerScreen from './screens/CustomerScreen';
import CourierScreen from './screens/CourierScreen';
import OrderTrackingScreen from './screens/OrderTrackingScreen';

export default function App() {
  const [currentScreen, setCurrentScreen] = useState('customer'); // 'customer', 'courier', 'tracking'
  const [orders, setOrders] = useState([]);

  const addOrder = (order) => {
    const newOrder = {
      id: Date.now().toString(),
      ...order,
      status: 'waiting_courier', // waiting_courier, courier_assigned, courier_on_way, picked_up, delivered
      createdAt: new Date().toISOString(),
    };
    setOrders(prev => [...prev, newOrder]);
    setCurrentScreen('tracking');
    return newOrder.id;
  };

  const updateOrderStatus = (orderId, status) => {
    setOrders(prev => prev.map(order => 
      order.id === orderId ? { ...order, status } : order
    ));
  };

  const renderScreen = () => {
    switch (currentScreen) {
      case 'customer':
        return (
          <CustomerScreen 
            onCreateOrder={addOrder}
            onNavigateToTracking={() => setCurrentScreen('tracking')}
          />
        );
      case 'courier':
        return (
          <CourierScreen 
            orders={orders.filter(order => order.status === 'waiting_courier')}
            onAcceptOrder={(orderId) => updateOrderStatus(orderId, 'courier_assigned')}
            onUpdateStatus={updateOrderStatus}
          />
        );
      case 'tracking':
        return (
          <OrderTrackingScreen 
            orders={orders}
            onBackToCustomer={() => setCurrentScreen('customer')}
          />
        );
      default:
        return <CustomerScreen onCreateOrder={addOrder} />;
    }
  };

  return (
    <View style={styles.container}>
      {renderScreen()}
      <StatusBar style="auto" />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
});
