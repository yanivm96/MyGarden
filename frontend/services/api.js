import AsyncStorage from "@react-native-async-storage/async-storage";

export const API_URL = "http://127.0.0.1:8000";

export const saveToken = async (token) => {
  await AsyncStorage.setItem("access_token", token);
};

export const getToken = async () => {
  return await AsyncStorage.getItem("access_token");
};

export const checkToken = async (navigation) => {
  try {
    const token = await AsyncStorage.getItem("access_token");
    if (!token) {
      navigation.navigate("Login");
      return;
    }

    const response = await fetch(`${API_URL}/token_login/`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (response.ok) {
      navigation.navigate("User");
    } else {
      await AsyncStorage.removeItem("access_token");
      navigation.navigate("Login");
    }
  } catch (error) {
    console.error("Error checking token:", error);
    navigation.navigate("Login");
  }
};

export const registerUser = async (username, password) => {
  try {
    console.log(username);
    const response = await fetch(API_URL + "/register/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });

    if (!response.ok) {
      throw new Error("Registration failed");
    }

    return await response.json();
  } catch (error) {
    console.error(error.message);
    throw error;
  }
};

export const LoginUser = async (username, password) => {
  try {
    console.log(username);
    const response = await fetch(API_URL + "/login/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });

    if (!response.ok) {
      throw new Error("Login failed");
    }

    return await response.json();
  } catch (error) {
    console.error(error.message);
    throw error;
  }
};

export const SendPhoto = async (image_base64) => {
  try {
    const token = await getToken();
    const response = await fetch(`${API_URL}/add_new_plant/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ image_base64 }),
    });
    if (!response.ok) {
      throw new Error("sending photo failed");
    }

    return await response.json();
  } catch (error) {
    console.error(error.message);
    throw error;
  }
};
