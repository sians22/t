import { View, Text, Button } from 'react-native';
import { router } from 'expo-router';

export default function OrderFormScreen() {
  return (
    <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
      <Text style={{ fontSize: 24, marginBottom: 16 }}>Order Form (Placeholder)</Text>
      <Button title="Create Order" onPress={() => router.push('/(customer)/orders')} />
    </View>
  );
}