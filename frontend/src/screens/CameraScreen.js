import React, { useState } from "react";
import {
  View,
  Image,
  StyleSheet,
  Alert,
  Text,
  TouchableOpacity,
  Platform,
} from "react-native";
import * as ImagePicker from "expo-image-picker";
import * as FileSystem from "expo-file-system";
import Icon from "react-native-vector-icons/MaterialCommunityIcons";
import { SendPhoto } from "../../services/api";

const CameraScreen = ({ navigation }) => {
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

  const saveToGarden = () => {
    if (base64) {
      Alert.alert("Saved!", "Your photo has been saved to your garden.");
      SendPhoto(base64);
      goBack();
    } else {
      Alert.alert("Error", "No photo taken yet!");
    }
  };

  const goBack = () => {
    navigation.navigate("User");
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Capture Your Plant</Text>

      <TouchableOpacity style={styles.cameraButton} onPress={takePhoto}>
        <Icon name="camera" size={50} color="#FFFFFF" />
        <Text style={styles.buttonText}>Take Photo</Text>
      </TouchableOpacity>

      {imageUri && <Image source={{ uri: imageUri }} style={styles.image} />}

      {imageUri && (
        <View style={styles.actionsContainer}>
          <TouchableOpacity style={styles.saveButton} onPress={saveToGarden}>
            <Icon name="content-save" size={30} color="#FFFFFF" />
            <Text style={styles.buttonText}>Save to Garden</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.cancelButton} onPress={goBack}>
            <Icon name="close-circle" size={30} color="#FFFFFF" />
            <Text style={styles.buttonText}>Cancel</Text>
          </TouchableOpacity>
        </View>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    padding: 20,
    backgroundColor: "#F4E1C4", // רקע נעים
  },
  title: {
    fontSize: 24,
    fontWeight: "bold",
    color: "#006D5B",
    marginBottom: 20,
  },
  cameraButton: {
    backgroundColor: "#006D5B", // ירוק כהה
    width: 150,
    height: 150,
    borderRadius: 75, // עיגול מושלם
    justifyContent: "center",
    alignItems: "center",
    marginBottom: 20,
    elevation: 5,
  },
  image: {
    width: 200,
    height: 200,
    marginTop: 20,
    borderRadius: 10, // פינות מעוגלות לתמונה
    borderWidth: 2,
    borderColor: "#006D5B", // מסגרת ירוקה
  },
  actionsContainer: {
    flexDirection: "row",
    justifyContent: "space-between",
    marginTop: 20,
    width: "100%",
    paddingHorizontal: 20,
  },
  saveButton: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: "#2ABF88", // ירוק בהיר
    paddingVertical: 15,
    paddingHorizontal: 20,
    borderRadius: 10,
    flex: 1,
    marginRight: 10,
    elevation: 5,
  },
  cancelButton: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: "#E57373", // אדום
    paddingVertical: 15,
    paddingHorizontal: 20,
    borderRadius: 10,
    flex: 1,
    marginLeft: 10,
    elevation: 5,
  },
  buttonText: {
    color: "#FFFFFF",
    fontSize: 16,
    fontWeight: "bold",
    marginLeft: 10,
  },
});

export default CameraScreen;
