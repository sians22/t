import React, { useState } from 'react';
import { StyleSheet, TextInput, Button, Alert } from 'react-native';
import { Text, View } from '@/components/Themed';

// Mesafe ve fiyat hesaplama için örnek fonksiyon
const calculatePrice = (distanceKm: number) => {
  if (distanceKm <= 3) return 20;
  if (distanceKm <= 10) return 50;
  return 100;
};

export default function OrderCreateScreen() {
  const [pickup, setPickup] = useState('');
  const [dropoff, setDropoff] = useState('');
  const [customerPhone, setCustomerPhone] = useState('');
  const [receiverPhone, setReceiverPhone] = useState('');
  const [price, setPrice] = useState<number | null>(null);
  const [distance, setDistance] = useState<number | null>(null);

  // Mock mesafe (km) - ileride API ile hesaplanacak
  const mockDistance = 5;

  const handleOrder = () => {
    // Adresler ve numaralar girilmiş mi kontrolü
    if (!pickup || !dropoff || !customerPhone || !receiverPhone) {
      Alert.alert('Eksik Bilgi', 'Lütfen tüm alanları doldurun.');
      return;
    }
    setDistance(mockDistance);
    const calculated = calculatePrice(mockDistance);
    setPrice(calculated);
    Alert.alert(
      'Fiyat Onayı',
      `Mesafe: ${mockDistance} km\nFiyat: ${calculated} TL\nOnaylıyor musunuz?`,
      [
        { text: 'İptal', style: 'cancel' },
        { text: 'Onayla', onPress: () => Alert.alert('Sipariş Oluşturuldu', 'Siparişiniz başarıyla oluşturuldu!') },
      ]
    );
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Sipariş Oluştur</Text>
      <TextInput
        style={styles.input}
        placeholder="Teslim Alınacak Yer"
        value={pickup}
        onChangeText={setPickup}
      />
      <TextInput
        style={styles.input}
        placeholder="Teslim Edilecek Yer"
        value={dropoff}
        onChangeText={setDropoff}
      />
      <TextInput
        style={styles.input}
        placeholder="Kendi Numaranız"
        keyboardType="phone-pad"
        value={customerPhone}
        onChangeText={setCustomerPhone}
      />
      <TextInput
        style={styles.input}
        placeholder="Teslim Alacak Kişinin Numarası"
        keyboardType="phone-pad"
        value={receiverPhone}
        onChangeText={setReceiverPhone}
      />
      <Button title="Siparişi Oluştur" onPress={handleOrder} color="#d16ba5" />
      {price !== null && distance !== null && (
        <Text style={styles.priceInfo}>Mesafe: {distance} km - Fiyat: {price} TL</Text>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    padding: 20,
    backgroundColor: '#fff0f6',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#d16ba5',
    marginBottom: 24,
  },
  input: {
    width: '100%',
    height: 48,
    borderColor: '#d16ba5',
    borderWidth: 1,
    borderRadius: 12,
    paddingHorizontal: 16,
    marginBottom: 16,
    backgroundColor: '#fff',
  },
  priceInfo: {
    marginTop: 20,
    fontSize: 18,
    color: '#d16ba5',
    fontWeight: 'bold',
  },
});
