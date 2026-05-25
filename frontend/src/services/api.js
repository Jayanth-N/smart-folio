import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth
export const login = async (username, password) => {
  const response = await api.post('/auth/login', { username, password });
  return response.data;
};

// Portfolio
export const getHoldings = async () => {
  const response = await api.get('/portfolio/holdings');
  return response.data;
};

export const addHolding = async (holding) => {
  const response = await api.post('/portfolio/holdings', holding);
  return response.data;
};

export const updateHolding = async (id, holding) => {
  const response = await api.put(`/portfolio/holdings/${id}`, holding);
  return response.data;
};

export const deleteHolding = async (id) => {
  await api.delete(`/portfolio/holdings/${id}`);
};

export const getDistribution = async () => {
  const response = await api.get('/portfolio/distribution');
  return response.data;
};

// Stocks
export const getStockInfo = async (symbol) => {
  const response = await api.get(`/stocks/${symbol}`);
  return response.data;
};

export const getRiskSuggestion = async (symbol) => {
  const response = await api.get(`/stocks/${symbol}/risk-suggestion`);
  return response.data;
};

// Recommendations
export const getRecommendations = async () => {
  const response = await api.get('/recommendations');
  return response.data;
};

export default api;
