import React, { useState, useEffect } from "react";
import { checkinApi, teamApi } from "../services";
import {
  Box,
  Button,
  TextField,
  MenuItem,
  Select,
  InputLabel,
  FormControl,
  Typography,
  Alert,
  CircularProgress,
} from "@mui/material";

const CheckInForm = () => {
  const [teams, setTeams] = useState([]);
  const [formData, setFormData] = useState({ team_id: "", post_url: "" });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  useEffect(() => {
    fetchTeams();
  }, []);

  const fetchTeams = async () => {
    try {
      setLoading(true);
      const response = await teamApi.getAllTeams();
      if (response.success) {
        setTeams(response.data);
      }
    } catch (err) {
      setError("Failed to load teams. Please try again.");
      console.error("Error fetching teams:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    setError("");
    setSuccess("");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.team_id || !formData.post_url) {
      setError("Please fill out all fields.");
      return;
    }

    try {
      setLoading(true);
      const response = await checkinApi.createCheckin(formData);

      if (response.success) {
        setSuccess("Check-in successful!");
        setFormData({ team_id: "", post_url: "" });
      }
    } catch (err) {
      setError(err.message || "Error during check-in. Please try again.");
      console.error("Error during check-in:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box
      component="form"
      onSubmit={handleSubmit}
      sx={{
        maxWidth: 400,
        mx: "auto",
        p: 3,
        backgroundColor: "#f9f9f9",
        borderRadius: 2,
        boxShadow: 3,
      }}
    >
      <Typography variant="h5" gutterBottom>
        Check In
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError("")}>
          {error}
        </Alert>
      )}

      {success && (
        <Alert severity="success" sx={{ mb: 2 }} onClose={() => setSuccess("")}>
          {success}
        </Alert>
      )}

      <FormControl fullWidth margin="normal">
        <InputLabel id="team-select-label">Select Team</InputLabel>
        <Select
          labelId="team-select-label"
          name="team_id"
          value={formData.team_id}
          onChange={handleChange}
          required
          disabled={loading}
        >
          {teams.map((team) => (
            <MenuItem key={team.team_id} value={team.team_id}>
              {team.team_name}
            </MenuItem>
          ))}
        </Select>
      </FormControl>

      <TextField
        label="URL"
        name="post_url"
        type="url"
        value={formData.post_url}
        onChange={handleChange}
        fullWidth
        required
        margin="normal"
        disabled={loading}
      />

      <Button
        type="submit"
        variant="contained"
        color="primary"
        fullWidth
        sx={{ mt: 2 }}
        disabled={loading}
      >
        {loading ? (
          <CircularProgress size={24} color="inherit" />
        ) : (
          "Submit Check-In"
        )}
      </Button>
    </Box>
  );
};

export default CheckInForm;