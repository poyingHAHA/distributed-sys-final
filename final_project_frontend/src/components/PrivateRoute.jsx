import React from 'react';
import { Navigate } from 'react-router-dom';

const PrivateRoute = ({ children }) => {
  const isAuthenticated = !!localStorage.getItem('token'); // 檢查 token 是否存在

  return isAuthenticated ? children : <Navigate to="/login" />;
};

export default PrivateRoute;
