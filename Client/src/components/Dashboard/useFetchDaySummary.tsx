//useFetchDaySummary
import axios from "axios";
import useSWR from "swr";

interface DaySummary {
  total_entered: number;
  total_left: number;
  still_in_premise: number;
  anomalies: number;
}

const fetcher = async (url: string) => {
  const response = await axios.get(url);
  return response.data;
};

const useFetchDaySummary = () => {
  const { data, error } = useSWR<DaySummary>(
    "http://127.0.0.1:5002/daysummary",
    fetcher,
    {
      revalidateOnFocus: true,
      revalidateOnReconnect: true,
      refreshInterval: 5000, // Revalidate every 5 seconds
    }
  );

  return {
    daySummary: data,
    isLoading: !error && !data,
    isError: error,
  };
};

export default useFetchDaySummary;
