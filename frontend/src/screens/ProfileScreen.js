import React, { useState, useCallback } from "react";
import { Text } from "react-native";
import { useFocusEffect } from "@react-navigation/native";
import PlantList from "../components/PlantList";
import { getPlants } from "../../services/api";

const ProfileScreen = () => {
  const [plants, setPlants] = useState([]);
  const [loading, setLoading] = useState(true);

  useFocusEffect(
    useCallback(() => {
      const fetchPlants = async () => {
        try {
          setLoading(true);
          const data = await getPlants();
          setPlants(data);
          console.log("Plants:", data);
        } catch (error) {
          console.error("Error fetching plants:", error);
        } finally {
          setLoading(false);
        }
      };

      fetchPlants();
    }, [])
  );

  if (loading) {
    return <Text>Loading p lants...</Text>;
  }

  return <PlantList plants={plants} />;
};

export default ProfileScreen;
