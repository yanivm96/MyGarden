import AsyncStorage from '@react-native-async-storage/async-storage';

const API_URL = 'http://127.0.0.1:8000'; 

export const saveToken = async (token) => {
    await AsyncStorage.setItem('access_token', token);
  };

export const getToken = async () => {
    return await AsyncStorage.getItem('access_token');
  };

export const registerUser = async (username, password) => {
    try {
        console.log(username)
        const response = await fetch(API_URL + '/register/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
      });
  
      if (!response.ok) {
        throw new Error('Registration failed');
      }
  
      return await response.json();
    } 
    catch (error) {
      console.error(error.message);
      throw error; 
    }
  };

  export const LoginUser = async (username, password) => {
    try {
        console.log(username)
        const response = await fetch('http://127.0.0.1:8000/login/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
      });
  
      if (!response.ok) {
        throw new Error('Login failed');
      }
  
      return await response.json();
    } 
    catch (error) {
      console.error(error.message);
      throw error; 
    }
  };
  