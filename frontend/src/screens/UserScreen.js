import React from "react";
import { View, TouchableOpacity, StyleSheet, Text } from "react-native";
import Icon from "react-native-vector-icons/MaterialCommunityIcons";

const UserScreen = ({ navigation }) => {
  return (
    <View style={styles.container}>
      <Text style={styles.welcomeText}>Welcome Back, Plant Lover!</Text>
      <Text style={styles.subtitle}>What would you like to do today?</Text>
      <View style={styles.actionContainer}>
        {/* Identify a New Plant */}
        <TouchableOpacity
          style={styles.actionButton}
          onPress={() => navigation.navigate("Camera")}
        >
          <Icon name="camera" size={50} color="#FFFFFF" style={styles.icon} />
          <Text style={styles.buttonText}>Identify New Plant</Text>
        </TouchableOpacity>
        {/* My Plants */}
        <TouchableOpacity
          style={styles.actionButton}
          onPress={() => navigation.navigate("MyPlants")}
        >
          <Icon name="leaf" size={50} color="#FFFFFF" style={styles.icon} />
          <Text style={styles.buttonText}>View My Plants</Text>
        </TouchableOpacity>
        {/* Explore Tips */}
        <TouchableOpacity
          style={styles.actionButton}
          onPress={() => navigation.navigate("Tips")}
        >
          <Icon
            name="lightbulb-on"
            size={50}
            color="#FFFFFF"
            style={styles.icon}
          />
          <Text style={styles.buttonText}>Explore Gardening Tips</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    padding: 20,
  },
  welcomeText: {
    fontSize: 28,
    fontWeight: "bold",
    color: "#006D5B",
    marginBottom: 10,
    textAlign: "center",
  },
  subtitle: {
    fontSize: 16,
    color: "#444",
    marginBottom: 30,
    textAlign: "center",
  },
  actionContainer: {
    flexDirection: "row",
    flexWrap: "wrap",
    justifyContent: "center",
    gap: 15,
  },
  actionButton: {
    width: 120,
    height: 120,
    borderRadius: 15,
    backgroundColor: "#006D5B",
    justifyContent: "center",
    alignItems: "center",
    margin: 10,
    elevation: 5,
  },
  icon: {
    marginBottom: 10,
  },
  buttonText: {
    fontSize: 14,
    color: "#FFFFFF",
    fontWeight: "bold",
    textAlign: "center",
  },
});

export default UserScreen;
