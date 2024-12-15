// src/services/team.js
import apiClient from "./axios";

export const teamApi = {
  createTeam: async (teamData) => {
    console.log("[createTeam] Request Data:", teamData);
    const response = await apiClient.post("/teams", teamData);
    console.log("[createTeam] Response Data:", response);
    return response;
  },

  joinTeam: async (teamId) => {
    console.log("[joinTeam] Team ID:", teamId);
    const response = await apiClient.post(`/teams/${teamId}/join`);
    console.log("[joinTeam] Response Data:", response);
    return response;
  },

  getAllTeams: async ({
    page = 1,
    size = 20,
    search = "",
    sortBy = null,
    sortDesc = true,
  } = {}) => {
    console.log("[getAllTeams] Request Params:", {
      page,
      size,
      search,
      sortBy,
      sortDesc,
    });
    const response = await apiClient.get("/teams", {
      params: {
        page,
        size,
        search,
        sort_by: sortBy,
        sort_desc: sortDesc,
      },
    });
    console.log("[getAllTeams] Response Data:", response);
    return response;
  },

  getTeamRankings: async ({ page = 1, size = 20, minScore = null } = {}) => {
    console.log("[getTeamRankings] Request Params:", { page, size, minScore });
    const response = await apiClient.get("/teams/rankings", {
      params: {
        page,
        size,
        min_score: minScore,
      },
    });
    console.log("[getTeamRankings] Response Data:", response);
    return response;
  },

  getTeamDetails: async (teamId) => {
    console.log("[getTeamDetails] Team ID:", teamId);
    const response = await apiClient.get(`/teams/${teamId}`);
    console.log("[getTeamDetails] Response Data:", response);
    return response;
  },
};
