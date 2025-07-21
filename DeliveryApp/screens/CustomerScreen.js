import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TextInput,
  TouchableOpacity,
  Alert,
  StatusBar,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import AddressSelector from '../components/AddressSelector';
import PriceConfirmation from '../components/PriceConfirmation';
import { calculateDistance } from '../utils/distance';
import { calculatePrice } from '../data/pricing';

export default function CustomerScreen({ onCreateOrder, onNavigateToTracking }) {
  const [pickupAddress, setPickupAddress] = useState(null);
  const [deliveryAddress, setDeliveryAddress] = useState(null);
  const [customerPhone, setCustomerPhone] = useState('');
  const [recipientPhone, setRecipientPhone] = useState('');
  const [showPriceConfirmation, setShowPriceConfirmation] = useState(false);
  const [orderData, setOrderData] = useState(null);

  const handleCreateOrder = () => {
    if (!pickupAddress || !deliveryAddress || !customerPhone || !recipientPhone) {
      Alert.alert('Eksik Bilgi', 'Lütfen tüm alanları doldurun.');
      return;
    }

    const distance = calculateDistance(
      pickupAddress.latitude,
      pickupAddress.longitude,
      deliveryAddress.latitude,
      deliveryAddress.longitude
    );

    const price = calculatePrice(distance);

    const order = {
      pickupAddress,
      deliveryAddress,
      customerPhone,
      recipientPhone,
      distance,
      price,
    };

    setOrderData(order);
    setShowPriceConfirmation(true);
  };

  const confirmOrder = () => {
    onCreateOrder(orderData);
    setShowPriceConfirmation(false);
    // Reset form
    setPickupAddress(null);
    setDeliveryAddress(null);
    setCustomerPhone('');
    setRecipientPhone('');
  };

  if (showPriceConfirmation) {
    return (
      <PriceConfirmation
        orderData={orderData}
        onConfirm={confirmOrder}
        onCancel={() => setShowPriceConfirmation(false)}
      />
    );
  }

  return (
    <ScrollView style={styles.container} showsVerticalScrollIndicator={false}>
      <StatusBar backgroundColor="#FF69B4" barStyle="light-content" />
      
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.headerTitle}>✨ Siparişinizi Oluşturun</Text>
        <Text style={styles.headerSubtitle}>Güvenli ve hızlı teslimat</Text>
      </View>

      {/* Address Selection */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>📍 Teslimat Bilgileri</Text>
        
        <View style={styles.addressContainer}>
          <Text style={styles.label}>Alınacak Adres</Text>
          <AddressSelector
            selectedAddress={pickupAddress}
            onSelectAddress={setPickupAddress}
            placeholder="Nereden alınacak?"
            icon="location-outline"
          />
        </View>

        <View style={styles.addressContainer}>
          <Text style={styles.label}>Teslim Edilecek Adres</Text>
          <AddressSelector
            selectedAddress={deliveryAddress}
            onSelectAddress={setDeliveryAddress}
            placeholder="Nereye teslim edilecek?"
            icon="location"
          />
        </View>
      </View>

      {/* Phone Numbers */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>📞 İletişim Bilgileri</Text>
        
        <View style={styles.inputContainer}>
          <Text style={styles.label}>Sizin Telefon Numaranız</Text>
          <View style={styles.phoneInputWrapper}>
            <Ionicons name="call-outline" size={20} color="#FF69B4" style={styles.inputIcon} />
            <TextInput
              style={styles.phoneInput}
              placeholder="0555 123 45 67"
              value={customerPhone}
              onChangeText={setCustomerPhone}
              keyboardType="phone-pad"
              maxLength={11}
            />
          </View>
        </View>

        <View style={styles.inputContainer}>
          <Text style={styles.label}>Alıcının Telefon Numarası</Text>
          <View style={styles.phoneInputWrapper}>
            <Ionicons name="call" size={20} color="#FF69B4" style={styles.inputIcon} />
            <TextInput
              style={styles.phoneInput}
              placeholder="0555 987 65 43"
              value={recipientPhone}
              onChangeText={setRecipientPhone}
              keyboardType="phone-pad"
              maxLength={11}
            />
          </View>
        </View>
      </View>

      {/* Create Order Button */}
      <TouchableOpacity style={styles.createOrderButton} onPress={handleCreateOrder}>
        <Ionicons name="heart" size={24} color="white" style={styles.buttonIcon} />
        <Text style={styles.createOrderButtonText}>Sipariş Oluştur</Text>
      </TouchableOpacity>

      {/* Track Orders Button */}
      <TouchableOpacity style={styles.trackOrdersButton} onPress={onNavigateToTracking}>
        <Ionicons name="eye-outline" size={20} color="#FF69B4" />
        <Text style={styles.trackOrdersButtonText}>Siparişlerimi Takip Et</Text>
      </TouchableOpacity>

      <View style={styles.bottomPadding} />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#FFF5F8',
  },
  header: {
    backgroundColor: '#FF69B4',
    paddingTop: 50,
    paddingBottom: 30,
    paddingHorizontal: 20,
    borderBottomLeftRadius: 30,
    borderBottomRightRadius: 30,
    shadowColor: '#FF69B4',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 8,
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
  section: {
    margin: 20,
    backgroundColor: 'white',
    borderRadius: 20,
    padding: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 3,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 15,
  },
  addressContainer: {
    marginBottom: 15,
  },
  label: {
    fontSize: 14,
    fontWeight: '600',
    color: '#666',
    marginBottom: 8,
  },
  inputContainer: {
    marginBottom: 15,
  },
  phoneInputWrapper: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#F8F9FA',
    borderRadius: 15,
    borderWidth: 1,
    borderColor: '#FFB6C1',
    paddingHorizontal: 15,
  },
  inputIcon: {
    marginRight: 10,
  },
  phoneInput: {
    flex: 1,
    paddingVertical: 15,
    fontSize: 16,
    color: '#333',
  },
  createOrderButton: {
    backgroundColor: '#FF69B4',
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    marginHorizontal: 20,
    paddingVertical: 18,
    borderRadius: 25,
    shadowColor: '#FF69B4',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 8,
  },
  buttonIcon: {
    marginRight: 10,
  },
  createOrderButtonText: {
    color: 'white',
    fontSize: 18,
    fontWeight: 'bold',
  },
  trackOrdersButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    marginHorizontal: 20,
    marginTop: 15,
    paddingVertical: 15,
    borderRadius: 20,
    borderWidth: 2,
    borderColor: '#FF69B4',
    backgroundColor: 'white',
  },
  trackOrdersButtonText: {
    color: '#FF69B4',
    fontSize: 16,
    fontWeight: '600',
    marginLeft: 8,
  },
  bottomPadding: {
    height: 30,
  },
});