/**
 * React Context for global authentication state management.
 */
import React, { createContext, useState, useEffect, useCallback } from 'react';
import { apiService } from '../services/api';
import { jwtDecode } from 'jwt-decode';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [accessToken, setAccessToken] = useState(localStorage.getItem('accessToken'));
  const [loading, setLoading] = useState(true);

  const handleAuthResponse = useCallback((response) => {
    const { access_token } = response.data;
    localStorage.setItem('accessToken', access_token);
    setAccessToken(access_token);
    const decoded = jwtDecode(access_token);
    setUser({ id: decoded.sub });
  }, []);

  useEffect(() => {
    if (accessToken) {
      try {
        const decoded = jwtDecode(accessToken);
        const isExpired = decoded.exp * 1000 < Date.now();
        if (isExpired) {
          throw new Error("Token expired");
        }
        setUser({ id: decoded.sub });
      } catch (error) {
        console.error("Invalid or expired token:", error);
        localStorage.removeItem('accessToken');
        setAccessToken(null);
        setUser(null);
      }
    }
    setLoading(false);
  }, [accessToken]);

  const login = useCallback(async (loginData) => {
    const response = await apiService.auth.login(loginData);
    handleAuthResponse(response);
  }, [handleAuthResponse]);

  const register = useCallback(async (registrationData) => {
    const response = await apiService.auth.register(registrationData);
    handleAuthResponse(response);
  }, [handleAuthResponse]);

  const logout = useCallback(() => {
    setUser(null);
    setAccessToken(null);
    localStorage.removeItem('accessToken');
  }, []);

  const value = { user, accessToken, loading, login, logout, register };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export default AuthContext;