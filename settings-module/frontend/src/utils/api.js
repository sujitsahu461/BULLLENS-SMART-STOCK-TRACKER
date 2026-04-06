import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('accessToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle token refresh or redirect to login
      localStorage.removeItem('accessToken');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth endpoints
export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', data),
  refreshToken: (data) => api.post('/auth/refresh-token', data),
  logout: () => api.post('/auth/logout'),
  enable2FA: (data) => api.post('/auth/2fa/enable', data),
  disable2FA: () => api.post('/auth/2fa/disable'),
};

// User endpoints
export const userAPI = {
  getProfile: () => api.get('/users/profile'),
  updateProfile: (data) => api.put('/users/profile', data),
  changePassword: (data) => api.post('/users/change-password', data),
  getLoginHistory: () => api.get('/users/login-history'),
  deleteAccount: (data) => api.delete('/users/account', { data }),
};

// Settings endpoints
export const settingsAPI = {
  getSettings: () => api.get('/settings'),
  updateSettings: (data) => api.patch('/settings', data),
  updateProfileSettings: (data) => api.put('/settings/profile', data),
  updatePredictionSettings: (data) => api.put('/settings/predictions', data),
  updateNotificationSettings: (data) => api.put('/settings/notifications', data),
  updateDashboardSettings: (data) => api.put('/settings/dashboard', data),
  updateAIBehavior: (data) => api.put('/settings/ai-behavior', data),
  updateLocalization: (data) => api.put('/settings/localization', data),
  resetToDefaults: () => api.post('/settings/reset'),
  getAuditLog: (params) => api.get('/settings/audit-log', { params }),
};

export default api;
