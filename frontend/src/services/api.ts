import axios, { AxiosInstance } from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle token refresh on 401
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refresh_token');
        const response = await axios.post(`${API_BASE_URL}/auth/refresh`, {
          refresh_token: refreshToken,
        });

        localStorage.setItem('access_token', response.data.access_token);
        api.defaults.headers.Authorization = `Bearer ${response.data.access_token}`;
        return api(originalRequest);
      } catch (refreshError) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default api;

// Auth APIs
export const authAPI = {
  register: (data: any) => api.post('/auth/register', data),
  login: (email: string, password: string) =>
    api.post('/auth/login', { email, password }),
  logout: () => api.post('/auth/logout'),
  me: () => api.get('/auth/me'),
  updateProfile: (data: any) => api.put('/auth/me', data),
};

// API Keys APIs
export const apiKeysAPI = {
  create: (data: any) => api.post('/keys', data),
  list: () => api.get('/keys'),
  delete: (keyId: string) => api.delete(`/keys/${keyId}`),
  getUsage: (keyId: string) => api.get(`/keys/${keyId}/usage`),
};

// Gateway APIs
export const gatewayAPI = {
  chat: (data: any) => api.post('/gateway/chat', data),
  chatStream: (data: any) =>
    api.post('/gateway/chat/stream', data, { responseType: 'stream' }),
  getProviders: () => api.get('/gateway/providers'),
  estimateCost: (data: any) => api.post('/gateway/estimate', data),
};
