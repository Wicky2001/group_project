// useFetchDaySummary.ts

import axios from "axios";
import useSWR from "swr";
import API_CONFIG from "../API";

interface DaySummary {
  total_entered: number;
  total_left: number;
  still_in_premise: number;
  anomalies: number;
}

// Fetcher function using Axios
const fetcher = async (url: string) => {
  const response = await axios.get(url);
  return response.data;
};

// Custom hook using SWR
const useFetchDaySummary = () => {
  const { data, error } = useSWR<DaySummary>(API_CONFIG.TodaySummary, fetcher, {
    revalidateOnFocus: true,
    revalidateOnReconnect: true,
    refreshInterval: 4000, // Revalidate every 5 seconds
  });

  return {
    daySummary: data,
    isLoading: !error && !data,
    isError: error,
  };
};

export default useFetchDaySummary;
