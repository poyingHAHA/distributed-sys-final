import React from "react";
import { Link } from "react-router-dom";
import { AppBar, Toolbar, Button, Box } from "@mui/material";

const Navbar = () => {
  return (
    <AppBar position="static" color="primary">
      <Toolbar>
        <Box sx={{ flexGrow: 1, display: "flex", gap: 2 }}>
          <Button component={Link} to="/dashboard" color="inherit">
            Leaderboard
          </Button>
          <Button component={Link} to="/team" color="inherit">
            Team
          </Button>
          <Button component={Link} to="/checkin" color="inherit">
            Check In
          </Button>
          <Button component={Link} to="/login" color="inherit">
            Logout
          </Button>
          <Button component={Link} to="/register" color="inherit">
            Register
          </Button>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;
