import axios from 'axios';

const apiClient = axios.create({
  baseURL: process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/v1',
});

// Use a variable to prevent multiple refresh requests
let isRefreshing = false;
let failedQueue = [];

const processQueue = (error, token = null) => {
  failedQueue.forEach(prom => {
    if (error) {
      prom.reject(error);
    } else {
      prom.resolve(token);
    }
  });
  failedQueue = [];
};

export const setupInterceptors = (logout) => {
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

  apiClient.interceptors.response.use(
    (response) => response,
    async (error) => {
      const originalRequest = error.config;
      // If the error is 401 and it's not a retry or a refresh request
      if (error.response.status === 401 && !originalRequest._retry) {
        if (isRefreshing) {
          return new Promise(function(resolve, reject) {
            failedQueue.push({ resolve, reject });
          }).then(token => {
            originalRequest.headers['Authorization'] = 'Bearer ' + token;
            return apiClient(originalRequest);
          });
        }

        originalRequest._retry = true;
        isRefreshing = true;

        const refreshToken = localStorage.getItem('refreshToken');
        if (!refreshToken) {
          logout();
          return Promise.reject(error);
        }

        try {
          const formData = new URLSearchParams();
          formData.append('refresh_token', refreshToken);
          const response = await apiService.auth.refresh(formData);

          const { access_token, refresh_token } = response.data;
          localStorage.setItem('accessToken', access_token);
          localStorage.setItem('refreshToken', refresh_token);

          apiClient.defaults.headers.common['Authorization'] = 'Bearer ' + access_token;
          originalRequest.headers['Authorization'] = 'Bearer ' + access_token;

          processQueue(null, access_token);
          return apiClient(originalRequest);
        } catch (refreshError) {
          processQueue(refreshError, null);
          logout();
          return Promise.reject(refreshError);
        } finally {
          isRefreshing = false;
        }
      }
      return Promise.reject(error);
    }
  );
};


export const apiService = {
  auth: {
    register: (registrationData) => apiClient.post('/auth/register', registrationData),
    login: (loginData) => apiClient.post('/auth/login', loginData),
    refresh: (formData) => apiClient.post('/auth/refresh', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    }),
  },
  tasks: {
    getAll: (task_status = null) => {
      const params = task_status ? { task_status } : {};
      return apiClient.get('/tasks/', { params });
    },
    create: (taskData) => apiClient.post('/tasks/', taskData),
    update: (taskId, updateData) => apiClient.put(`/tasks/${taskId}`, updateData),
    delete: (taskId) => apiClient.delete(`/tasks/${taskId}`),
  },
};