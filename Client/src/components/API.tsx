const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

const API_CONFIG = {
  lastEntries: `${API_BASE_URL}/lastEntries`,
  addEntry: `${API_BASE_URL}/addEntry`,
  TodaySummary: `${API_BASE_URL}/TodaySummary`,
  sortTraffic: `${API_BASE_URL}/sortTraffic?`,
  searchByDate: `${API_BASE_URL}/searchByDate`,
};

export default API_CONFIG;
