import React, { useState } from 'react';
import { StyleSheet, ActivityIndicator, Button } from 'react-native';
import { Text, View } from '@/components/Themed';

const statuses = [
  { label: 'Kurye bekleniyor', color: '#d16ba5' },
  { label: 'Kurye siparişi onayladı', color: '#6a4c93' },
  { label: 'Kurye yolda', color: '#355c7d' },
  { label: 'Kurye siparişi teslim etti', color: '#2a363b' },
];

export default function OrderStatusScreen() {
  const [statusIndex, setStatusIndex] = useState(0);

  // Demo amaçlı: Durumu ilerletmek için buton
  const nextStatus = () => {
    setStatusIndex((prev) => (prev + 1 < statuses.length ? prev + 1 : prev));
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Sipariş Durumu</Text>
      <ActivityIndicator size="large" color={statuses[statusIndex].color} style={{ margin: 32 }} />
      <Text style={[styles.status, { color: statuses[statusIndex].color }]}>{statuses[statusIndex].label}</Text>
      <Button title="Durumu İlerle (Demo)" onPress={nextStatus} color="#d16ba5" />
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
  status: {
    fontSize: 20,
    fontWeight: 'bold',
    marginBottom: 24,
  },
});
