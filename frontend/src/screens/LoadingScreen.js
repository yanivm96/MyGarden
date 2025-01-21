import React, { useEffect } from 'react';
import { View, ActivityIndicator, StyleSheet } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { getToken } from '../services/api';

const LoadingScreen = ({ navigation }) => {
  useEffect(() => {
    const checkToken = async () => {
      try {
        const token = await getToken();
        if (!token) {
          navigation.navigate('Login');
          return;
        }

        const response = await fetch('http://127.0.0.1:8000/login/', {
          method: 'POST',
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (response.ok) {
          navigation.navigate('ProfileScreen'); 
        } else {
          await AsyncStorage.removeItem('access_token');
          navigation.navigate('Login');
        }
      } catch (error) {
        console.error('Error checking token:', error);
        navigation.navigate('Login');
      }
    };

    checkToken();
  }, [navigation]);

  return (
    <View style={styles.container}>
      <ActivityIndicator size="large" color="#0000ff" />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
});

export default LoadingScreen;
