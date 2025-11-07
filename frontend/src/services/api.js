/**
 * Centralized API service module using Axios.
 */
import axios from 'axios';

const apiClient = axios.create({
  // baseURL: process.env.REACT_APP_API_BASE_URL,
    baseURL: "http://localhost:8000/v1"
});


apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('accessToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

export const apiService = {
  auth: {
    register: (registrationData) => apiClient.post('/auth/register', registrationData),
    login: (loginData) => apiClient.post('/auth/login', loginData),
  },
  tasks: {
    getAll: (status = null) => {
      const params = status ? { status } : {};
      return apiClient.get('/tasks', { params });
    },
    create: (taskData) => apiClient.post('/tasks', taskData),
    update: (taskId, updateData) => apiClient.put(`/tasks/${taskId}`, updateData),
    delete: (taskId) => apiClient.delete(`/tasks/${taskId}`),
  },
};