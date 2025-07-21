import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
  StatusBar,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { formatPrice, getDistanceText } from '../data/pricing';

export default function PriceConfirmation({ orderData, onConfirm, onCancel }) {
  const { pickupAddress, deliveryAddress, customerPhone, recipientPhone, distance, price } = orderData;

  return (
    <View style={styles.container}>
      <StatusBar backgroundColor="#FF69B4" barStyle="light-content" />
      
      {/* Header */}
      <View style={styles.header}>
        <TouchableOpacity style={styles.backButton} onPress={onCancel}>
          <Ionicons name="arrow-back" size={24} color="white" />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>💖 Sipariş Özeti</Text>
        <View style={styles.placeholder} />
      </View>

      <ScrollView style={styles.content} showsVerticalScrollIndicator={false}>
        {/* Distance and Price Info */}
        <View style={styles.priceCard}>
          <View style={styles.priceHeader}>
            <Ionicons name="car-outline" size={32} color="#FF69B4" />
            <Text style={styles.priceHeaderText}>Teslimat Bilgileri</Text>
          </View>
          
          <View style={styles.priceRow}>
            <Text style={styles.priceLabel}>📏 Mesafe</Text>
            <Text style={styles.priceValue}>{getDistanceText(distance)}</Text>
          </View>
          
          <View style={styles.priceRow}>
            <Text style={styles.priceLabel}>💰 Teslimat Ücreti</Text>
            <Text style={styles.priceValueHighlight}>{formatPrice(price)}</Text>
          </View>
        </View>

        {/* Address Details */}
        <View style={styles.detailsCard}>
          <Text style={styles.cardTitle}>📍 Adres Bilgileri</Text>
          
          <View style={styles.addressRow}>
            <View style={styles.addressIcon}>
              <Ionicons name="radio-button-on" size={16} color="#4CAF50" />
            </View>
            <View style={styles.addressTextContainer}>
              <Text style={styles.addressLabel}>Alınacak Adres</Text>
              <Text style={styles.addressText}>{pickupAddress.title}</Text>
              <Text style={styles.addressDescription}>{pickupAddress.description}</Text>
            </View>
          </View>

          <View style={styles.routeLine} />

          <View style={styles.addressRow}>
            <View style={styles.addressIcon}>
              <Ionicons name="location" size={16} color="#FF69B4" />
            </View>
            <View style={styles.addressTextContainer}>
              <Text style={styles.addressLabel}>Teslim Edilecek Adres</Text>
              <Text style={styles.addressText}>{deliveryAddress.title}</Text>
              <Text style={styles.addressDescription}>{deliveryAddress.description}</Text>
            </View>
          </View>
        </View>

        {/* Contact Details */}
        <View style={styles.detailsCard}>
          <Text style={styles.cardTitle}>📞 İletişim Bilgileri</Text>
          
          <View style={styles.contactRow}>
            <Ionicons name="person-circle" size={24} color="#FF69B4" />
            <View style={styles.contactTextContainer}>
              <Text style={styles.contactLabel}>Siparişi Veren</Text>
              <Text style={styles.contactText}>{customerPhone}</Text>
            </View>
          </View>

          <View style={styles.contactRow}>
            <Ionicons name="person-circle-outline" size={24} color="#666" />
            <View style={styles.contactTextContainer}>
              <Text style={styles.contactLabel}>Alıcı Kişi</Text>
              <Text style={styles.contactText}>{recipientPhone}</Text>
            </View>
          </View>
        </View>

        {/* Important Note */}
        <View style={styles.noteCard}>
          <Ionicons name="information-circle" size={24} color="#FF69B4" />
          <Text style={styles.noteText}>
            Siparişinizi onayladıktan sonra bir kurye atanacak ve teslimat süreci başlayacaktır.
          </Text>
        </View>
      </ScrollView>

      {/* Action Buttons */}
      <View style={styles.actionContainer}>
        <TouchableOpacity style={styles.cancelButton} onPress={onCancel}>
          <Text style={styles.cancelButtonText}>İptal Et</Text>
        </TouchableOpacity>
        
        <TouchableOpacity style={styles.confirmButton} onPress={onConfirm}>
          <Ionicons name="heart" size={20} color="white" style={styles.buttonIcon} />
          <Text style={styles.confirmButtonText}>Onayla & Siparişi Ver</Text>
        </TouchableOpacity>
      </View>
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
  placeholder: {
    width: 34,
  },
  content: {
    flex: 1,
    padding: 20,
  },
  priceCard: {
    backgroundColor: 'white',
    borderRadius: 20,
    padding: 20,
    marginBottom: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 3,
    borderLeftWidth: 4,
    borderLeftColor: '#FF69B4',
  },
  priceHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 20,
  },
  priceHeaderText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginLeft: 10,
  },
  priceRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 8,
  },
  priceLabel: {
    fontSize: 16,
    color: '#666',
  },
  priceValue: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
  },
  priceValueHighlight: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#FF69B4',
  },
  detailsCard: {
    backgroundColor: 'white',
    borderRadius: 20,
    padding: 20,
    marginBottom: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 3,
  },
  cardTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 15,
  },
  addressRow: {
    flexDirection: 'row',
    alignItems: 'flex-start',
  },
  addressIcon: {
    width: 24,
    alignItems: 'center',
    paddingTop: 2,
  },
  addressTextContainer: {
    flex: 1,
    marginLeft: 10,
  },
  addressLabel: {
    fontSize: 12,
    color: '#666',
    fontWeight: '600',
    marginBottom: 4,
  },
  addressText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
    marginBottom: 2,
  },
  addressDescription: {
    fontSize: 14,
    color: '#666',
  },
  routeLine: {
    width: 2,
    height: 20,
    backgroundColor: '#ddd',
    marginLeft: 11,
    marginVertical: 10,
  },
  contactRow: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 10,
  },
  contactTextContainer: {
    marginLeft: 12,
  },
  contactLabel: {
    fontSize: 12,
    color: '#666',
    fontWeight: '600',
    marginBottom: 2,
  },
  contactText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
  },
  noteCard: {
    backgroundColor: '#FFF0F5',
    borderRadius: 15,
    padding: 15,
    flexDirection: 'row',
    alignItems: 'flex-start',
    borderWidth: 1,
    borderColor: '#FFB6C1',
  },
  noteText: {
    flex: 1,
    fontSize: 14,
    color: '#666',
    lineHeight: 20,
    marginLeft: 10,
  },
  actionContainer: {
    flexDirection: 'row',
    padding: 20,
    paddingTop: 10,
  },
  cancelButton: {
    flex: 1,
    backgroundColor: 'white',
    borderWidth: 2,
    borderColor: '#FF69B4',
    borderRadius: 20,
    paddingVertical: 15,
    alignItems: 'center',
    marginRight: 10,
  },
  cancelButtonText: {
    color: '#FF69B4',
    fontSize: 16,
    fontWeight: 'bold',
  },
  confirmButton: {
    flex: 2,
    backgroundColor: '#FF69B4',
    borderRadius: 20,
    paddingVertical: 15,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    marginLeft: 10,
    shadowColor: '#FF69B4',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 8,
  },
  buttonIcon: {
    marginRight: 8,
  },
  confirmButtonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: 'bold',
  },
});