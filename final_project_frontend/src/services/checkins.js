// src/services/checkin.js
import apiClient from "./axios";

export const checkinApi = {
  createCheckin: async (checkinData) => {
    console.log("[createCheckin] Request Data:", checkinData);
    const response = await apiClient.post("/checkin", checkinData);
    console.log("[createCheckin] Response Data:", response);
    return response;
  },

  getCheckinStatus: async (teamId) => {
    console.log("[getCheckinStatus] Team ID:", teamId);
    const response = await apiClient.get(`/checkin/status/${teamId}`);
    console.log("[getCheckinStatus] Response Data:", response);
    return response;
  },
};
