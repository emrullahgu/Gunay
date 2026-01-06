// API Base URL
const API_URL = import.meta.env.VITE_API_URL || '/api';
const USE_MOCK_DATA = !import.meta.env.VITE_API_URL; // API URL yoksa mock data kullan

export const config = {
  apiUrl: API_URL,
  useMockData: USE_MOCK_DATA,
  endpoints: {
    olcumler: `${API_URL}/olcumler`,
    cihazlar: `${API_URL}/cihazlar`,
    dashboard: `${API_URL}/dashboard`,
    raporlar: `${API_URL}/raporlar`
  }
};

export default config;
