// src/services/axios.js
import axios from "axios";

const apiClient = axios.create({
  baseURL: process.env.REACT_APP_BASE_API_URL,
});

apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    console.log("[Request Interceptor] Token:", token);
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    console.log("[Request Interceptor] Config:", config);
    return config;
  },
  (error) => {
    console.error("[Request Interceptor] Error:", error);
    return Promise.reject(error);
  }
);

apiClient.interceptors.response.use(
  (response) => {
    console.log("[Response Interceptor] Response:", response);
    return response.data;
  },
  (error) => {
    console.error("[Response Interceptor] Error:", error);
    if (error.response?.status === 401) {
      localStorage.removeItem("token");
      window.location.href = "/login";
    }
    throw error.response?.data || error;
  }
);

export default apiClient;
