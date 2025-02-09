import React from "react";
import {
  Modal,
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Image,
} from "react-native";
import FontAwesome from "react-native-vector-icons/FontAwesome5";

export default function PlantModal({ visible, onClose, plant }) {
  if (!plant) return null;

  return (
    <Modal animationType="slide" transparent visible={visible}>
      <View style={styles.modalOverlay}>
        <View style={styles.modalContent}>
          {/* Close Button */}
          <TouchableOpacity style={styles.closeButton} onPress={onClose}>
            <FontAwesome name="times" size={24} color="#fff" />
          </TouchableOpacity>

          {/* Plant Image */}
          <Image
            source={{
              uri: plant.image_base64
                ? `${plant.image_base64}`
                : "https://via.placeholder.com/160",
            }}
            style={styles.modalImage}
            resizeMode="contain"
          />

          {/* Plant Details */}
          <View style={styles.modalDetails}>
            <Text style={styles.plantName}>{plant.name}</Text>
            <Text style={styles.plantDescription}>{plant.description}</Text>

            <View style={styles.iconWithText}>
              <FontAwesome
                name="sun"
                size={25}
                color="#f5a623"
                style={styles.icon}
              />
              <Text style={styles.iconText}>{plant.sunny_hours} hrs</Text>
            </View>
            <View style={styles.iconWithText}>
              <FontAwesome
                name="tint"
                size={22}
                color="#00aaff"
                style={[styles.icon, styles.wateringIcon]}
              />
              <Text style={styles.iconText}>{plant.watering}</Text>
            </View>
          </View>
        </View>
      </View>
    </Modal>
  );
}

const styles = StyleSheet.create({
  modalOverlay: {
    flex: 1,
    backgroundColor: "rgba(0, 0, 0, 0.5)",
    justifyContent: "center",
    alignItems: "center",
  },
  modalContent: {
    width: "90%",
    backgroundColor: "#fff",
    borderRadius: 8,
    overflow: "hidden",
    alignItems: "center",
    elevation: 10,
  },
  closeButton: {
    position: "absolute",
    top: 10,
    right: 10,
    zIndex: 1,
    backgroundColor: "#000",
    borderRadius: 20,
    padding: 5,
  },
  modalImage: {
    width: "100%",
    height: 300,
    marginBottom: 16,
    backgroundColor: "#f2f2f2",
  },
  modalDetails: {
    padding: 16,
  },
  plantName: {
    fontSize: 22,
    fontWeight: "bold",
    color: "#232425",
    marginBottom: 8,
  },
  plantDescription: {
    fontSize: 16,
    color: "#595a63",
    marginBottom: 16,
    textAlign: "center",
  },
  iconWithText: {
    flexDirection: "row",
    alignItems: "center",
    marginBottom: 8,
  },
  icon: {
    marginRight: 8,
  },
  iconText: {
    fontSize: 14,
    color: "#232425",
  },
  wateringIcon: {
    marginLeft: 3,
  },
});
