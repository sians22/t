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
import { formatPrice, getDistanceText } from '../data/pricing';

export default function CourierScreen({ orders, onAcceptOrder, onUpdateStatus }) {
  const renderOrderItem = ({ item }) => (
    <View style={styles.orderCard}>
      <View style={styles.orderHeader}>
        <Text style={styles.orderTitle}>Yeni Sipariş</Text>
        <Text style={styles.orderPrice}>{formatPrice(item.price)}</Text>
      </View>

      <View style={styles.routeContainer}>
        <View style={styles.addressRow}>
          <Ionicons name="radio-button-on" size={16} color="#4CAF50" />
          <Text style={styles.addressText}>{item.pickupAddress.title}</Text>
        </View>
        
        <View style={styles.routeLine} />
        
        <View style={styles.addressRow}>
          <Ionicons name="location" size={16} color="#FF6B35" />
          <Text style={styles.addressText}>{item.deliveryAddress.title}</Text>
        </View>
      </View>

      <View style={styles.orderDetails}>
        <Text style={styles.detailText}>📏 {getDistanceText(item.distance)}</Text>
        <Text style={styles.detailText}>📞 {item.customerPhone}</Text>
      </View>

      <TouchableOpacity
        style={styles.acceptButton}
        onPress={() => onAcceptOrder(item.id)}
      >
        <Ionicons name="checkmark-circle" size={20} color="white" />
        <Text style={styles.acceptButtonText}>Siparişi Kabul Et</Text>
      </TouchableOpacity>
    </View>
  );

  return (
    <View style={styles.container}>
      <StatusBar backgroundColor="#FF6B35" barStyle="light-content" />
      
      <View style={styles.header}>
        <Text style={styles.headerTitle}>🚴‍♂️ Kurye Paneli</Text>
        <Text style={styles.headerSubtitle}>Mevcut Siparişler</Text>
      </View>

      {orders.length === 0 ? (
        <View style={styles.emptyContainer}>
          <Ionicons name="bicycle-outline" size={80} color="#ccc" />
          <Text style={styles.emptyTitle}>Henüz sipariş yok</Text>
          <Text style={styles.emptySubtitle}>Yeni siparişler geldiğinde burada görünecek</Text>
        </View>
      ) : (
        <FlatList
          data={orders}
          renderItem={renderOrderItem}
          keyExtractor={(item) => item.id}
          style={styles.ordersList}
          contentContainerStyle={styles.ordersListContent}
        />
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#FFF8F5',
  },
  header: {
    backgroundColor: '#FF6B35',
    paddingTop: 50,
    paddingBottom: 30,
    paddingHorizontal: 20,
    borderBottomLeftRadius: 30,
    borderBottomRightRadius: 30,
  },
  headerTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: 'white',
    textAlign: 'center',
    marginBottom: 5,
  },
  headerSubtitle: {
    fontSize: 16,
    color: 'white',
    textAlign: 'center',
    opacity: 0.9,
  },
  emptyContainer: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    paddingHorizontal: 40,
  },
  emptyTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
    marginTop: 20,
    marginBottom: 10,
    textAlign: 'center',
  },
  emptySubtitle: {
    fontSize: 16,
    color: '#666',
    textAlign: 'center',
    lineHeight: 22,
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
  orderTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
  },
  orderPrice: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#FF6B35',
  },
  routeContainer: {
    marginBottom: 15,
  },
  addressRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 5,
  },
  addressText: {
    fontSize: 14,
    color: '#666',
    marginLeft: 10,
    flex: 1,
  },
  routeLine: {
    width: 2,
    height: 20,
    backgroundColor: '#ddd',
    marginLeft: 7,
    marginVertical: 5,
  },
  orderDetails: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 15,
  },
  detailText: {
    fontSize: 14,
    color: '#666',
  },
  acceptButton: {
    backgroundColor: '#4CAF50',
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 15,
    borderRadius: 15,
  },
  acceptButtonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: 'bold',
    marginLeft: 8,
  },
});