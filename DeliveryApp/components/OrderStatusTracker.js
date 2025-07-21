import React, { useEffect, useRef } from 'react';
import { View, Text, StyleSheet, Animated } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import * as Animatable from 'react-native-animatable';

export default function OrderStatusTracker({ status }) {
  const pulseAnimation = useRef(new Animated.Value(1)).current;

  const statusSteps = [
    {
      key: 'waiting_courier',
      title: 'Kurye Bekleniyor',
      icon: 'hourglass-outline',
      description: 'Siparişiniz için kurye aranıyor',
    },
    {
      key: 'courier_assigned',
      title: 'Kurye Atandı',
      icon: 'person-add',
      description: 'Kurye siparişi kabul etti',
    },
    {
      key: 'courier_on_way',
      title: 'Kurye Yolda',
      icon: 'bicycle',
      description: 'Kurye alım noktasına gidiyor',
    },
    {
      key: 'picked_up',
      title: 'Sipariş Alındı',
      icon: 'checkmark-circle',
      description: 'Kurye siparişi teslim alındı',
    },
    {
      key: 'delivered',
      title: 'Teslim Edildi',
      icon: 'heart-circle',
      description: 'Sipariş başarıyla teslim edildi',
    },
  ];

  const getCurrentStepIndex = () => {
    return statusSteps.findIndex(step => step.key === status);
  };

  const isStepCompleted = (stepIndex) => {
    return stepIndex <= getCurrentStepIndex();
  };

  const isStepActive = (stepIndex) => {
    return stepIndex === getCurrentStepIndex();
  };

  useEffect(() => {
    if (isStepActive(getCurrentStepIndex())) {
      const pulse = () => {
        Animated.sequence([
          Animated.timing(pulseAnimation, {
            toValue: 1.2,
            duration: 800,
            useNativeDriver: true,
          }),
          Animated.timing(pulseAnimation, {
            toValue: 1,
            duration: 800,
            useNativeDriver: true,
          }),
        ]).start(() => pulse());
      };
      pulse();
    }
  }, [status]);

  const getStepColor = (stepIndex) => {
    if (isStepCompleted(stepIndex)) {
      return '#4CAF50';
    } else if (isStepActive(stepIndex)) {
      return '#FF69B4';
    } else {
      return '#E0E0E0';
    }
  };

  const getLineColor = (stepIndex) => {
    return isStepCompleted(stepIndex) ? '#4CAF50' : '#E0E0E0';
  };

  const renderStep = (step, index) => {
    const isCompleted = isStepCompleted(index);
    const isActive = isStepActive(index);
    const color = getStepColor(index);

    return (
      <View key={step.key} style={styles.stepContainer}>
        <View style={styles.stepIndicatorContainer}>
          {isActive ? (
            <Animated.View
              style={[
                styles.stepIndicator,
                { backgroundColor: color, transform: [{ scale: pulseAnimation }] }
              ]}
            >
              <Animatable.View
                animation="rotate"
                iterationCount="infinite"
                duration={2000}
                style={styles.stepIconContainer}
              >
                <Ionicons name={step.icon} size={16} color="white" />
              </Animatable.View>
            </Animated.View>
          ) : (
            <View style={[styles.stepIndicator, { backgroundColor: color }]}>
              {isCompleted ? (
                <Ionicons name="checkmark" size={16} color="white" />
              ) : (
                <Ionicons name={step.icon} size={16} color="white" />
              )}
            </View>
          )}
          
          {index < statusSteps.length - 1 && (
            <View
              style={[
                styles.stepLine,
                { backgroundColor: getLineColor(index) }
              ]}
            />
          )}
        </View>

        <View style={styles.stepContent}>
          <Text style={[
            styles.stepTitle,
            { color: isActive ? '#FF69B4' : isCompleted ? '#4CAF50' : '#666' }
          ]}>
            {step.title}
          </Text>
          {isActive && (
            <Animatable.Text
              animation="fadeIn"
              duration={500}
              style={styles.stepDescription}
            >
              {step.description}
            </Animatable.Text>
          )}
        </View>
      </View>
    );
  };

  return (
    <View style={styles.container}>
      <View style={styles.headerContainer}>
        <Ionicons name="location" size={20} color="#FF69B4" />
        <Text style={styles.headerTitle}>Sipariş Durumu</Text>
        {status === 'delivered' && (
          <Animatable.View animation="bounceIn" duration={1000}>
            <Ionicons name="heart" size={20} color="#4CAF50" />
          </Animatable.View>
        )}
      </View>
      
      <View style={styles.stepsContainer}>
        {statusSteps.map((step, index) => renderStep(step, index))}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: '#FFF0F5',
    borderRadius: 15,
    padding: 15,
    marginVertical: 10,
  },
  headerContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 15,
  },
  headerTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
    marginLeft: 8,
    flex: 1,
  },
  stepsContainer: {
    paddingLeft: 10,
  },
  stepContainer: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    marginBottom: 5,
  },
  stepIndicatorContainer: {
    alignItems: 'center',
    width: 30,
  },
  stepIndicator: {
    width: 30,
    height: 30,
    borderRadius: 15,
    alignItems: 'center',
    justifyContent: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 2,
  },
  stepIconContainer: {
    alignItems: 'center',
    justifyContent: 'center',
  },
  stepLine: {
    width: 2,
    height: 25,
    marginTop: 5,
  },
  stepContent: {
    flex: 1,
    marginLeft: 15,
    paddingTop: 5,
  },
  stepTitle: {
    fontSize: 14,
    fontWeight: '600',
    marginBottom: 2,
  },
  stepDescription: {
    fontSize: 12,
    color: '#666',
    fontStyle: 'italic',
  },
});