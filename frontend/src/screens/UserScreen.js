import React from "react";
import { View, Text, Button } from "react-native";
import { styles } from "./HomeScreen";

const UserScreen = ({ navigation }) => {
  return (
    <View style={styles.container}>
      <View style={styles.buttonContainer}>
        <Button title="Camera" onPress={() => navigation.navigate("Camera")} />
      </View>
    </View>
  );
};

export default UserScreen;
