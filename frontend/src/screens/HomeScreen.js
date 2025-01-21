import React from 'react';
import { View, Text, Button, StyleSheet } from 'react-native';

const HomeScreen = ({ navigation }) => {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Welcome to MyPlantApp!</Text>
      <View style={styles.buttonContainer}>
      <Button
        title="Register"
        onPress={() => navigation.navigate('Register')}
      />
      <Button
        title="Login"
        onPress={() => navigation.navigate('LoadingScreen')}
      />
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#F5F5F5',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 20,
  },
  buttonContainer: {
    flexDirection: 'row', 
    justifyContent: 'space-between', 
    width: '40%', 
  },
});

export default HomeScreen;
