import { View, Text } from 'react-native';
import { useLocalSearchParams } from 'expo-router';

export default function TaskDetailScreen() {
  const { taskId } = useLocalSearchParams<{ taskId: string }>();

  return (
    <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
      <Text style={{ fontSize: 24 }}>Task Detail for #{taskId}</Text>
    </View>
  );
}