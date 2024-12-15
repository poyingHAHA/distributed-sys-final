import React, { useEffect, useState } from "react";
import { teamApi } from "../services";

import {
  Box,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  List,
  ListItem,
  ListItemText,
  Pagination,
  Chip,
  CircularProgress,
  Alert,
  TextField,
  InputAdornment
} from "@mui/material";
import { Search, EmojiEvents } from "@mui/icons-material";

const Leaderboard = () => {
  const [rankings, setRankings] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [minScore, setMinScore] = useState("");

  const fetchRankings = async () => {
    try {
      setLoading(true);
      const response = await teamApi.getTeamRankings({
        page,
        size: 10,
        minScore: minScore ? parseFloat(minScore) : null
      });

      if (response.success) {
        setRankings(response.data || []);
        setTotalPages(Math.ceil(response.total / 10));
      }
    } catch (err) {
      setError(err.message);
      setRankings([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRankings();
  }, [page, minScore]);

  const getRankColor = (rank) => {
    if (rank === 1) return "#FFD700"; // Gold
    if (rank === 2) return "#C0C0C0"; // Silver
    if (rank === 3) return "#CD7F32"; // Bronze
    return "#FFFFFF"; // White
  };

  const formatScore = (score) => {
    return Number(score).toFixed(2);
  };

  if (loading) {
    return (
      <Box sx={{ display: "flex", justifyContent: "center", mt: 4 }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box sx={{ maxWidth: 1200, mx: "auto", mt: 4, p: 3 }}>
      <Box sx={{ display: "flex", alignItems: "center", mb: 3 }}>
        <EmojiEvents sx={{ mr: 1, color: "#FFD700" }} />
        <Typography variant="h5">Team Rankings</Typography>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError("")}>
          {error}
        </Alert>
      )}

      <Box sx={{ mb: 3 }}>
        <TextField
          label="Minimum Score Filter"
          type="number"
          value={minScore}
          onChange={(e) => setMinScore(e.target.value)}
          size="small"
          InputProps={{
            startAdornment: (
              <InputAdornment position="start">
                <Search />
              </InputAdornment>
            ),
          }}
        />
      </Box>

      {rankings.length === 0 ? (
        <Paper sx={{ p: 3, textAlign: "center" }}>
          <Typography color="textSecondary">No rankings available.</Typography>
        </Paper>
      ) : (
        <TableContainer component={Paper} sx={{ mb: 3 }}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Rank</TableCell>
                <TableCell>Team</TableCell>
                <TableCell align="center">Score</TableCell>
                <TableCell>Members</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {rankings.map((team, index) => (
                <TableRow
                  key={team.team_id}
                  sx={{
                    backgroundColor: getRankColor(index + 1),
                    '&:hover': { backgroundColor: '#f5f5f5' }
                  }}
                >
                  <TableCell>
                    <Chip
                      label={`#${index + 1}`}
                      color={index < 3 ? "primary" : "default"}
                      variant={index < 3 ? "filled" : "outlined"}
                    />
                  </TableCell>
                  <TableCell>
                    <Typography variant="subtitle1">
                      {team.team_name}
                    </Typography>
                  </TableCell>
                  <TableCell align="center">
                    <Typography
                      variant="h6"
                      color="primary"
                      sx={{ fontWeight: 'bold' }}
                    >
                      {formatScore(team.current_score)}
                    </Typography>
                  </TableCell>
                  <TableCell>
                    <List dense>
                      {team.members?.map((member) => (
                        <ListItem key={member.user_id} disableGutters>
                          <ListItemText
                            primary={member.name}
                            secondary={`Last checkin: ${
                              member.last_checkin_time
                                ? new Date(member.last_checkin_time).toLocaleDateString()
                                : 'Never'
                            }`}
                          />
                        </ListItem>
                      ))}
                    </List>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}

      <Box sx={{ display: "flex", justifyContent: "center" }}>
        <Pagination
          count={totalPages}
          page={page}
          onChange={(e, value) => setPage(value)}
          color="primary"
          size="large"
        />
      </Box>
    </Box>
  );
};

export default Leaderboard;