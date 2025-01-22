import React, { useState } from "react";
import {
  View,
  Button,
  Image,
  StyleSheet,
  Alert,
  Text,
  Platform,
} from "react-native";
import * as ImagePicker from "expo-image-picker";
import * as FileSystem from "expo-file-system";
import { SendPhoto } from "../../services/api";

const CameraScreen = () => {
  const [imageUri, setImageUri] = useState(null);
  const [base64, setBase64] = useState(null);

  const takePhoto = async () => {
    const { status } = await ImagePicker.requestCameraPermissionsAsync();
    if (status !== "granted") {
      Alert.alert(
        "Permission denied",
        "We need camera access to take a photo."
      );
      return;
    }

    const result = await ImagePicker.launchCameraAsync({
      allowsEditing: true,
      aspect: [4, 3],
      quality: 1,
    });

    if (!result.canceled) {
      const uri = result.assets[0].uri;
      setImageUri(uri);

      try {
        if (Platform.OS === "web") {
          const response = await fetch(uri);
          const blob = await response.blob();

          const reader = new FileReader();
          reader.onload = () => {
            setBase64(reader.result.split(",")[1]);
          };
          reader.onerror = (error) => {
            console.error("Error reading file:", error);
            Alert.alert("Error", "Failed to process the image.");
          };
          reader.readAsDataURL(blob);
        } else {
          const base64Data = await FileSystem.readAsStringAsync(uri, {
            encoding: FileSystem.EncodingType.Base64,
          });
          setBase64(base64Data);
        }
      } catch (error) {
        console.error("Error processing image:", error);
        Alert.alert("Error", "Failed to process the image.");
      }
    }
  };

  const send = () => {
    if (base64) {
      Alert.alert("Base64", `Base64 Length: ${base64.length}`);
      
    } else {
      Alert.alert("Error", "No photo taken yet!");
    }
  };

  return (
    <View style={styles.container}>
      <Button title="Take Photo" onPress={takePhoto} />
      {imageUri && <Image source={{ uri: imageUri }} style={styles.image} />}
      {base64 && (
        <Text style={styles.text}>Base64 Length: {base64.length}</Text>
      )}
      <Button title="send" onPress={send} />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    padding: 20,
    backgroundColor: "transparent",
  },
  image: {
    width: 200,
    height: 200,
    marginTop: 20,
    borderRadius: 10,
  },
  text: {
    marginTop: 20,
    color: "gray",
  },
});

export default CameraScreen;
