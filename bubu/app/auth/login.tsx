import { View, Text, Button } from 'react-native';
import { router } from 'expo-router';

export default function LoginScreen() {
  return (
    <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
      <Text style={{ fontSize: 24, marginBottom: 16 }}>BuBu Login (Mock)</Text>
      <Button title="Dev Login" onPress={() => router.replace('/(customer)/order-form')} />
    </View>
  );
}