import React, { useState } from "react";
import {
  StyleSheet,
  SafeAreaView,
  ScrollView,
  TouchableOpacity,
  View,
  Image,
  Text,
} from "react-native";
import FontAwesome from "react-native-vector-icons/FontAwesome5";
import FeatherIcon from "react-native-vector-icons/Feather";

function getImageUri(base64, mimeType = "image/jpeg") {
  if (!base64) {
    console.warn("Base64 string is missing or invalid.");
    return "https://via.placeholder.com/160";
  }
  return `data:${mimeType};base64,${base64}`;
}

export default function PlantList({ plants }) {
  const [saved, setSaved] = useState([]);

  if (!plants || !Array.isArray(plants)) {
    return <Text>No plants available.</Text>;
  }

  return (
    <SafeAreaView style={{ flex: 1, backgroundColor: "#f2f2f2" }}>
      {/* Header */}
      <View style={styles.header}>
        <View style={styles.headerTop}>
          <View style={styles.headerAction} />
          <View style={styles.headerAction}>
            <TouchableOpacity onPress={() => {}}>
              <FeatherIcon color="#000" name="sliders" size={21} />
            </TouchableOpacity>
          </View>
        </View>
        <Text style={styles.headerTitle}>Your Plants</Text>
      </View>

      <ScrollView contentContainerStyle={styles.content}>
        {plants.map(
          (
            { description, id, image_base64, name, sunny_hours, watering },
            index
          ) => {
            const isSaved = saved.includes(id);

            return (
              <TouchableOpacity key={id} onPress={() => {}}>
                <View style={styles.card}>
                  {/* Like Button */}
                  <View style={styles.cardLikeWrapper}>
                    <TouchableOpacity
                      onPress={() =>
                        setSaved((prev) =>
                          isSaved
                            ? prev.filter((val) => val !== id)
                            : [...prev, id]
                        )
                      }
                    >
                      <View style={styles.cardLike}>
                        <FontAwesome
                          color={isSaved ? "#ea266d" : "#222"}
                          name="heart"
                          solid={isSaved}
                          size={20}
                        />
                      </View>
                    </TouchableOpacity>
                  </View>

                  {/* Image */}
                  <View style={styles.cardTop}>
                    <Image
                      alt=""
                      resizeMode="cover"
                      style={styles.cardImg}
                      source={{ uri: getImageUri(image_base64) }}
                    />
                  </View>

                  {/* Card Body */}
                  <View style={styles.cardBody}>
                    <View style={styles.iconRow}>
                      <Text style={styles.cardTitle}>{name}</Text>
                      <Text style={styles.cardDescription}>{description}</Text>

                      <View style={styles.iconWithText}>
                        <FontAwesome
                          name="sun"
                          size={25}
                          color="#f5a623"
                          style={styles.icon}
                        />
                        <Text style={styles.iconText}>{sunny_hours} hrs</Text>
                      </View>
                      <View style={styles.iconWithText}>
                        <FontAwesome
                          name="tint"
                          size={22}
                          color="#00aaff"
                          style={[styles.icon, styles.wateringIcon]}
                        />
                        <Text style={styles.iconText}>{watering}</Text>
                      </View>
                    </View>
                  </View>
                </View>
              </TouchableOpacity>
            );
          }
        )}
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  content: {
    paddingTop: 8,
    paddingHorizontal: 16,
  },
  header: {
    paddingHorizontal: 16,
    marginBottom: 12,
  },
  headerTop: {
    marginHorizontal: -6,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
  },
  headerAction: {
    width: 40,
    height: 40,
    alignItems: "center",
    justifyContent: "center",
  },
  headerTitle: {
    fontSize: 32,
    fontWeight: "700",
    color: "#1d1d1d",
  },
  card: {
    borderRadius: 8,
    backgroundColor: "#fff",
    marginBottom: 16,
    shadowColor: "rgba(0, 0, 0, 0.5)",
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.2,
    shadowRadius: 1.41,
    elevation: 2,
  },
  cardLikeWrapper: {
    position: "absolute",
    zIndex: 1,
    top: 12,
    right: 12,
  },
  cardLike: {
    width: 40,
    height: 40,
    borderRadius: 9999,
    backgroundColor: "#fff",
    alignItems: "center",
    justifyContent: "center",
  },
  cardTop: {
    borderTopLeftRadius: 8,
    borderTopRightRadius: 8,
  },
  cardImg: {
    width: "100%",
    height: 160,
    borderTopLeftRadius: 8,
    borderTopRightRadius: 8,
  },
  cardBody: {
    padding: 12,
  },
  cardTitle: {
    fontSize: 18,
    fontWeight: "500",
    color: "#232425",
  },
  cardDescription: {
    fontSize: 14,
    color: "#595a63",
    marginBottom: 8,
  },
  iconRow: {
    flexDirection: "column",
    alignItems: "flex-start",
    marginTop: 8,
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
