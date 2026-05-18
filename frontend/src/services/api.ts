import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const metricsAPI = {
  getCurrent: () => api.get('/api/metrics/current'),
  getHistorical: (params?: any) => api.get('/api/metrics/historical', { params }),
  getSummary: (hours = 1) => api.get('/api/metrics/summary', { params: { hours } }),
};

export const equipmentAPI = {
  getStatus: (params?: any) => api.get('/api/equipment/status', { params }),
  getSummary: () => api.get('/api/equipment/summary'),
  getDetail: (id: string) => api.get(`/api/equipment/${id}`),
};

export const incidentsAPI = {
  getActive: () => api.get('/api/incidents/active'),
  getAll: (params?: any) => api.get('/api/incidents/all', { params }),
};

export default api;
