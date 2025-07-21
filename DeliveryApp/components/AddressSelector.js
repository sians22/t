import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  FlatList,
  StyleSheet,
  Modal,
  ActivityIndicator,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { searchAddresses } from '../utils/distance';

export default function AddressSelector({ selectedAddress, onSelectAddress, placeholder, icon }) {
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSearch = async (query) => {
    setSearchQuery(query);
    if (query.length > 2) {
      setIsLoading(true);
      try {
        const results = await searchAddresses(query);
        setSearchResults(results);
      } catch (error) {
        console.error('Search error:', error);
      } finally {
        setIsLoading(false);
      }
    } else {
      setSearchResults([]);
    }
  };

  const selectAddress = (address) => {
    onSelectAddress(address);
    setIsModalVisible(false);
    setSearchQuery('');
    setSearchResults([]);
  };

  const renderAddressItem = ({ item }) => (
    <TouchableOpacity style={styles.addressItem} onPress={() => selectAddress(item)}>
      <View style={styles.addressIconContainer}>
        <Ionicons name="location" size={20} color="#FF69B4" />
      </View>
      <View style={styles.addressTextContainer}>
        <Text style={styles.addressTitle}>{item.title}</Text>
        <Text style={styles.addressDescription}>{item.description}</Text>
      </View>
      <Ionicons name="chevron-forward" size={20} color="#ccc" />
    </TouchableOpacity>
  );

  return (
    <>
      <TouchableOpacity
        style={styles.selectorButton}
        onPress={() => setIsModalVisible(true)}
      >
        <Ionicons name={icon} size={20} color="#FF69B4" style={styles.selectorIcon} />
        <Text style={[
          styles.selectorText,
          selectedAddress ? styles.selectedText : styles.placeholderText
        ]}>
          {selectedAddress ? selectedAddress.title : placeholder}
        </Text>
        <Ionicons name="chevron-down" size={20} color="#FF69B4" />
      </TouchableOpacity>

      <Modal
        visible={isModalVisible}
        animationType="slide"
        presentationStyle="pageSheet"
      >
        <View style={styles.modalContainer}>
          <View style={styles.modalHeader}>
            <Text style={styles.modalTitle}>Adres Seçin</Text>
            <TouchableOpacity
              style={styles.closeButton}
              onPress={() => setIsModalVisible(false)}
            >
              <Ionicons name="close" size={24} color="#FF69B4" />
            </TouchableOpacity>
          </View>

          <View style={styles.searchContainer}>
            <Ionicons name="search" size={20} color="#FF69B4" style={styles.searchIcon} />
            <TextInput
              style={styles.searchInput}
              placeholder="Adres ara..."
              value={searchQuery}
              onChangeText={handleSearch}
              autoFocus
            />
          </View>

          {isLoading && (
            <View style={styles.loadingContainer}>
              <ActivityIndicator size="large" color="#FF69B4" />
              <Text style={styles.loadingText}>Aranıyor...</Text>
            </View>
          )}

          <FlatList
            data={searchResults}
            renderItem={renderAddressItem}
            keyExtractor={(item) => item.id}
            style={styles.resultsList}
            showsVerticalScrollIndicator={false}
            ListEmptyComponent={() => 
              searchQuery.length > 2 && !isLoading ? (
                <View style={styles.emptyContainer}>
                  <Ionicons name="location-outline" size={48} color="#ccc" />
                  <Text style={styles.emptyText}>Adres bulunamadı</Text>
                </View>
              ) : searchQuery.length <= 2 ? (
                <View style={styles.emptyContainer}>
                  <Ionicons name="search-outline" size={48} color="#ccc" />
                  <Text style={styles.emptyText}>Adres aramak için en az 3 karakter girin</Text>
                </View>
              ) : null
            }
          />
        </View>
      </Modal>
    </>
  );
}

const styles = StyleSheet.create({
  selectorButton: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#F8F9FA',
    borderRadius: 15,
    borderWidth: 1,
    borderColor: '#FFB6C1',
    paddingHorizontal: 15,
    paddingVertical: 15,
  },
  selectorIcon: {
    marginRight: 10,
  },
  selectorText: {
    flex: 1,
    fontSize: 16,
  },
  selectedText: {
    color: '#333',
    fontWeight: '500',
  },
  placeholderText: {
    color: '#999',
  },
  modalContainer: {
    flex: 1,
    backgroundColor: '#FFF5F8',
  },
  modalHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 20,
    paddingTop: 50,
    paddingBottom: 20,
    backgroundColor: '#FF69B4',
  },
  modalTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: 'white',
  },
  closeButton: {
    padding: 5,
  },
  searchContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'white',
    margin: 20,
    paddingHorizontal: 15,
    borderRadius: 15,
    borderWidth: 1,
    borderColor: '#FFB6C1',
  },
  searchIcon: {
    marginRight: 10,
  },
  searchInput: {
    flex: 1,
    paddingVertical: 15,
    fontSize: 16,
    color: '#333',
  },
  loadingContainer: {
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 40,
  },
  loadingText: {
    marginTop: 10,
    fontSize: 16,
    color: '#FF69B4',
    fontWeight: '500',
  },
  resultsList: {
    flex: 1,
    paddingHorizontal: 20,
  },
  addressItem: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'white',
    padding: 15,
    borderRadius: 15,
    marginBottom: 10,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 2,
  },
  addressIconContainer: {
    width: 40,
    height: 40,
    backgroundColor: '#FFF0F5',
    borderRadius: 20,
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: 15,
  },
  addressTextContainer: {
    flex: 1,
  },
  addressTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
    marginBottom: 4,
  },
  addressDescription: {
    fontSize: 14,
    color: '#666',
  },
  emptyContainer: {
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 40,
  },
  emptyText: {
    marginTop: 10,
    fontSize: 16,
    color: '#999',
    textAlign: 'center',
  },
});