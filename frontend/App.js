import React from "react";
import { NavigationContainer, DefaultTheme } from "@react-navigation/native";
import { StyleSheet } from "react-native";
import StackNavigator from "./src/navigation/StackNavigator";

const MyTheme = {
  ...DefaultTheme,
  colors: {
    ...DefaultTheme.colors,
    background: "transparent",
  },
};

const App = () => {
  return (
    <NavigationContainer theme={MyTheme}>
      <StackNavigator />
    </NavigationContainer>
  );
};
export default App;
