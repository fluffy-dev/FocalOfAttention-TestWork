import React, { createContext, useState, useEffect, useCallback } from 'react';
import { apiService, setupInterceptors } from '../services/api';
import { jwtDecode } from 'jwt-decode';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [tokens, setTokens] = useState({
    access: localStorage.getItem('accessToken'),
    refresh: localStorage.getItem('refreshToken'),
  });
  const [loading, setLoading] = useState(true);

  const logout = useCallback(() => {
    setUser(null);
    setTokens({ access: null, refresh: null });
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
  }, []);

  const handleAuthResponse = useCallback((response) => {
    const { access_token, refresh_token } = response.data;
    localStorage.setItem('accessToken', access_token);
    localStorage.setItem('refreshToken', refresh_token);
    setTokens({ access: access_token, refresh: refresh_token });
    const decoded = jwtDecode(access_token);
    setUser({ id: decoded.sub });
  }, []);

  useEffect(() => {
    if (tokens.access) {
      try {
        const decoded = jwtDecode(tokens.access);
        const isExpired = decoded.exp * 1000 < Date.now();
        if (isExpired) {
          throw new Error("Token expired");
        }
        setUser({ id: decoded.sub });
      } catch (error) {
        console.error("Invalid or expired token, logging out:", error);
        logout();
      }
    }
    setLoading(false);
  }, [tokens.access, logout]);

  useEffect(() => {
    setupInterceptors(logout);
  }, [logout]);


  const login = useCallback(async (loginData) => {
    const response = await apiService.auth.login(loginData);
    handleAuthResponse(response);
  }, [handleAuthResponse]);

  const register = useCallback(async (registrationData) => {
    const response = await apiService.auth.register(registrationData);
    handleAuthResponse(response);
  }, [handleAuthResponse]);

  const value = { user, accessToken: tokens.access, loading, login, logout, register };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export default AuthContext;