import React, { useEffect } from "react";
import { View, ActivityIndicator, StyleSheet } from "react-native";
import { checkToken } from "../../services/api";

const LoadingScreen = ({ navigation }) => {
  useEffect(() => {
    checkToken(navigation);
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
    justifyContent: "center",
    alignItems: "center",
  },
});

export default LoadingScreen;
