// src/services/auth.js
import apiClient from "./axios";
import qs from "qs";

export const authApi = {
  login: async (credentials) => {
    const formData = qs.stringify({
      username: credentials.username,
      password: credentials.password,
      grant_type: "password",
    });
    console.log("[login] Request Data:", formData);

    try {
      const response = await apiClient.post("/token", formData, {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
      });
      console.log("[login] Response Data:", response);

      if (response.data?.access_token) {
        localStorage.setItem("token", response.data.access_token);
      }
      return response;
    } catch (error) {
      console.error("[login] Error Response:", error);
      throw error.response?.data || error;
    }
  },

  register: async (userData) => {
    console.log("[register] Request Data:", userData);
    try {
      const response = await apiClient.post("/register", userData);
      console.log("[register] Response Data:", response);

      if (response.data?.access_token) {
        localStorage.setItem("token", response.data.access_token);
      }
      return response;
    } catch (error) {
      console.error("[register] Error Response:", error);
      throw error.response?.data || error;
    }
  },

  logout: () => {
    console.log("[logout] Logging out user.");
    localStorage.removeItem("token");
  },
};
