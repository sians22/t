import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  StatusBar,
  FlatList,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import * as Animatable from 'react-native-animatable';
import OrderStatusTracker from '../components/OrderStatusTracker';
import { formatPrice, getDistanceText } from '../data/pricing';

export default function OrderTrackingScreen({ orders, onBackToCustomer }) {
  const getStatusText = (status) => {
    switch (status) {
      case 'waiting_courier':
        return 'Kurye bekleniyor...';
      case 'courier_assigned':
        return 'Kurye atandı';
      case 'courier_on_way':
        return 'Kurye yolda';
      case 'picked_up':
        return 'Sipariş alındı';
      case 'delivered':
        return 'Sipariş teslim edildi';
      default:
        return 'Bilinmeyen durum';
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'waiting_courier':
        return '#FFA500';
      case 'courier_assigned':
        return '#4CAF50';
      case 'courier_on_way':
        return '#2196F3';
      case 'picked_up':
        return '#9C27B0';
      case 'delivered':
        return '#4CAF50';
      default:
        return '#666';
    }
  };

  const renderOrderItem = ({ item }) => (
    <Animatable.View 
      animation="fadeInUp" 
      duration={600}
      style={styles.orderCard}
    >
      <View style={styles.orderHeader}>
        <View style={styles.orderIdContainer}>
          <Text style={styles.orderIdLabel}>Sipariş No:</Text>
          <Text style={styles.orderIdText}>#{item.id.slice(-6)}</Text>
        </View>
        <View style={[styles.statusBadge, { backgroundColor: getStatusColor(item.status) }]}>
          <Text style={styles.statusBadgeText}>{getStatusText(item.status)}</Text>
        </View>
      </View>

      <OrderStatusTracker status={item.status} />

      <View style={styles.orderDetails}>
        <View style={styles.detailRow}>
          <Ionicons name="location-outline" size={16} color="#666" />
          <Text style={styles.detailText} numberOfLines={1}>
            {item.pickupAddress.title} → {item.deliveryAddress.title}
          </Text>
        </View>
        
        <View style={styles.detailRow}>
          <Ionicons name="car-outline" size={16} color="#666" />
          <Text style={styles.detailText}>
            {getDistanceText(item.distance)} • {formatPrice(item.price)}
          </Text>
        </View>

        <View style={styles.detailRow}>
          <Ionicons name="time-outline" size={16} color="#666" />
          <Text style={styles.detailText}>
            {new Date(item.createdAt).toLocaleString('tr-TR')}
          </Text>
        </View>
      </View>
    </Animatable.View>
  );

  return (
    <View style={styles.container}>
      <StatusBar backgroundColor="#FF69B4" barStyle="light-content" />
      
      {/* Header */}
      <View style={styles.header}>
        <TouchableOpacity style={styles.backButton} onPress={onBackToCustomer}>
          <Ionicons name="arrow-back" size={24} color="white" />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>💖 Siparişlerim</Text>
        <TouchableOpacity style={styles.refreshButton}>
          <Ionicons name="refresh" size={24} color="white" />
        </TouchableOpacity>
      </View>

      {orders.length === 0 ? (
        <View style={styles.emptyContainer}>
          <Animatable.View 
            animation="bounceIn" 
            duration={1000}
            style={styles.emptyIconContainer}
          >
            <Ionicons name="heart-dislike-outline" size={80} color="#FFB6C1" />
          </Animatable.View>
          <Text style={styles.emptyTitle}>Henüz sipariş yok</Text>
          <Text style={styles.emptySubtitle}>
            İlk siparişinizi oluşturmak için ana sayfaya dönün
          </Text>
          <TouchableOpacity style={styles.createOrderButton} onPress={onBackToCustomer}>
            <Ionicons name="add-circle" size={20} color="white" />
            <Text style={styles.createOrderButtonText}>Sipariş Oluştur</Text>
          </TouchableOpacity>
        </View>
      ) : (
        <FlatList
          data={orders}
          renderItem={renderOrderItem}
          keyExtractor={(item) => item.id}
          style={styles.ordersList}
          showsVerticalScrollIndicator={false}
          contentContainerStyle={styles.ordersListContent}
        />
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#FFF5F8',
  },
  header: {
    backgroundColor: '#FF69B4',
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingTop: 50,
    paddingBottom: 20,
    paddingHorizontal: 20,
    shadowColor: '#FF69B4',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 8,
  },
  backButton: {
    padding: 5,
  },
  headerTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: 'white',
  },
  refreshButton: {
    padding: 5,
  },
  emptyContainer: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    paddingHorizontal: 40,
  },
  emptyIconContainer: {
    marginBottom: 20,
  },
  emptyTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 10,
    textAlign: 'center',
  },
  emptySubtitle: {
    fontSize: 16,
    color: '#666',
    textAlign: 'center',
    lineHeight: 22,
    marginBottom: 30,
  },
  createOrderButton: {
    backgroundColor: '#FF69B4',
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 30,
    paddingVertical: 15,
    borderRadius: 25,
    shadowColor: '#FF69B4',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 8,
  },
  createOrderButtonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: 'bold',
    marginLeft: 8,
  },
  ordersList: {
    flex: 1,
  },
  ordersListContent: {
    padding: 20,
  },
  orderCard: {
    backgroundColor: 'white',
    borderRadius: 20,
    padding: 20,
    marginBottom: 15,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 3,
  },
  orderHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 15,
  },
  orderIdContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  orderIdLabel: {
    fontSize: 14,
    color: '#666',
    marginRight: 5,
  },
  orderIdText: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
  },
  statusBadge: {
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 15,
  },
  statusBadgeText: {
    color: 'white',
    fontSize: 12,
    fontWeight: 'bold',
  },
  orderDetails: {
    marginTop: 15,
  },
  detailRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 8,
  },
  detailText: {
    fontSize: 14,
    color: '#666',
    marginLeft: 8,
    flex: 1,
  },
});