import React, { useState } from 'react';
import { View, Text, TextInput, Button, StyleSheet } from 'react-native';
import { registerUser } from '../../services/api';

const RegisterScreen = ({ navigation }) => {
  const [username, setUserName] = useState('');
  const [password, setPassword] = useState('');
``
  const handleRegister = async () => {
    try {
        console.log(username, password);
        const data = await registerUser(username, password);
        console.log('User registered:', data);
        if (data[1] == 200){
            alert('Registration successful!');
            navigation.navigate('Login');
        }
        else{
            throw new Error('Registration failed');
        }
        } catch (error) {
        alert('Registration failed. Please try again.');
    }
  };


  return (
    <View style={styles.container}>
      <Text style={styles.title}></Text>
      <TextInput
        style={styles.input}
        placeholder="Username"
        value={username}
        onChangeText={setUserName}
      />
      <TextInput
        style={styles.input}
        placeholder="Password"
        value={password}
        onChangeText={setPassword}
        secureTextEntry={true}
      />
      <Button title="Register" onPress={handleRegister} />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    padding: 20,
    backgroundColor: '#FFF',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 20,
    textAlign: 'center',
  },
  input: {
    height: 50,
    borderColor: '#CCC',
    borderWidth: 1,
    marginBottom: 20,
    paddingHorizontal: 10,
    borderRadius: 5,
  },
});

export default RegisterScreen;
