import React, { useState, useEffect } from "react";
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
  Pagination,
  IconButton,
  InputAdornment,
} from "@mui/material";
import { Search, Sort } from "@mui/icons-material";
import { teamApi } from "../services";

const TeamForm = () => {
  const [teamName, setTeamName] = useState("");
  const [teams, setTeams] = useState([]);
  const [selectedTeamId, setSelectedTeamId] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(false);

  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [searchTerm, setSearchTerm] = useState("");
  const [sortBy, setSortBy] = useState("name");
  const [sortDesc, setSortDesc] = useState(true);

  const fetchTeams = async () => {
    try {
      setLoading(true);
      const response = await teamApi.getAllTeams({
        page,
        size: 10,
        search: searchTerm,
        sortBy,
        sortDesc
      });
      if (response.success) {
        setTeams(response.data);
        setTotalPages(Math.ceil(response.total / 10));
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTeams();
  }, [page, searchTerm, sortBy, sortDesc]);

  const handleCreate = async () => {
    try {
      setLoading(true);
      const response = await teamApi.createTeam({ team_name: teamName });
      if (response.success) {
        setSuccess("Team created successfully!");
        fetchTeams();
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleJoin = async () => {
    try {
      setLoading(true);
      const response = await teamApi.joinTeam(selectedTeamId);
      if (response.success) {
        setSuccess("Successfully joined team!");
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };


  return (
    <Box sx={{ maxWidth: 800, mx: "auto", p: 3 }}>
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

      <Box sx={{ mb: 4, backgroundColor: "white", p: 3, borderRadius: 2 }}>
        <Typography variant="h6" gutterBottom>
          Create New Team
        </Typography>
        <TextField
          label="Team Name"
          fullWidth
          value={teamName}
          onChange={(e) => setTeamName(e.target.value)}
          sx={{ mb: 2 }}
        />
        <Button
          variant="contained"
          onClick={handleCreate}
          disabled={loading}
          fullWidth
        >
          {loading ? "Creating..." : "Create Team"}
        </Button>
      </Box>

      <Box sx={{ backgroundColor: "white", p: 3, borderRadius: 2 }}>
        <Typography variant="h6" gutterBottom>
          Join Existing Team
        </Typography>

        <Box sx={{ mb: 2, display: "flex", gap: 2 }}>
          <TextField
            label="Search Teams"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            InputProps={{
              endAdornment: (
                <InputAdornment position="end">
                  <Search />
                </InputAdornment>
              ),
            }}
            fullWidth
          />
          <FormControl sx={{ minWidth: 120 }}>
            <InputLabel>Sort By</InputLabel>
            <Select
              value={sortBy}
              label="Sort By"
              onChange={(e) => setSortBy(e.target.value)}
            >
              <MenuItem value="name">Name</MenuItem>
              <MenuItem value="members">Members</MenuItem>
              <MenuItem value="score">Score</MenuItem>
            </Select>
          </FormControl>
          <IconButton onClick={() => setSortDesc(!sortDesc)}>
            <Sort sx={{ transform: sortDesc ? "none" : "scaleY(-1)" }} />
          </IconButton>
        </Box>

        {teams.length === 0 ? (
          <Typography color="textSecondary" sx={{ my: 2 }}>
            No teams available
          </Typography>
        ) : (
          <FormControl fullWidth sx={{ mb: 2 }}>
            <InputLabel>Select Team</InputLabel>
            <Select
              value={selectedTeamId}
              label="Select Team"
              onChange={(e) => setSelectedTeamId(e.target.value)}
            >
              {teams.map((team) => (
                <MenuItem key={team.team_id} value={team.team_id}>
                  {team.team_name} ({team.member_count} members)
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        )}

        <Button
          variant="contained"
          onClick={handleJoin}
          disabled={loading || !selectedTeamId}
          fullWidth
          sx={{ mb: 2 }}
        >
          {loading ? "Joining..." : "Join Team"}
        </Button>

        <Box sx={{ display: "flex", justifyContent: "center", mt: 2 }}>
          <Pagination
            count={totalPages}
            page={page}
            onChange={(e, value) => setPage(value)}
            color="primary"
          />
        </Box>
      </Box>
    </Box>
  );
};

export default TeamForm;