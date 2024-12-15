import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { authApi } from "../services";
import { Box, TextField, Button, Typography } from "@mui/material";

const RegisterForm = () => {
    const [userData, setUserData] = useState({ username: "", password: "", name: "" });
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

    const handleRegister = async (e) => {
      e.preventDefault();
      setLoading(true);
      try {
        const response = await authApi.register(userData);
        if (response.success) {
          window.location.href = "/dashboard";
        }
      } catch (err) {
        setError(err.message || "Registration failed");
      } finally {
        setLoading(false);
      }
    };
    const navigate = useNavigate();

    const handleChange = (e) => {
        const { name, value } = e.target;
        setUserData((prevData) => ({
          ...prevData,
          [name]: value,
        }));
      };

  return (
    <Box
      component="form"
      onSubmit={handleRegister}
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
        Register
      </Typography>
      <TextField
        label="Username"
        name="username"
        fullWidth
        required
        margin="normal"
        onChange={handleChange}
      />
      <TextField
        label="Name"
        name="name"
        fullWidth
        required
        margin="normal"
        onChange={handleChange}
      />
      <TextField
        label="Password"
        name="password"
        type="password"
        fullWidth
        required
        margin="normal"
        onChange={handleChange}
      />
      <Button type="submit" variant="contained" color="primary" fullWidth sx={{ mt: 2 }}>
        Register
      </Button>
      <Button
        onClick={() => navigate("/login")}
        variant="outlined"
        color="secondary"
        fullWidth
        sx={{ mt: 1 }}
      >
        Back to Login
      </Button>
    </Box>
  );
};

export default RegisterForm;
