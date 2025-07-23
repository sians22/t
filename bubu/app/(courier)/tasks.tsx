import { View, Text, Button } from 'react-native';
import { router } from 'expo-router';

export default function TasksScreen() {
  return (
    <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
      <Text style={{ fontSize: 24, marginBottom: 16 }}>Courier Tasks (Placeholder)</Text>
      <Button title="Go To Task #123" onPress={() => router.push('/(courier)/123')} />
    </View>
  );
}