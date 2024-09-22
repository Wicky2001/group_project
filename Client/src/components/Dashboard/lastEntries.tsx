import useSWR from "swr";
import axios from "axios";
import API_CONFIG from "../API";

// Define the response structure
interface ApiResponse {
  length: number;
  result: Array<{
    day: {
      year: number;
      month: number;
      date: number;
      hour: number;
      minute: number;
      second: number;
    };
    number_plate: string;
    image_url: string;
    vehicle_type: string;
    status: string;
  }>;
}

// Define the entry structure
interface Entry {
  date: string;
  time: string;
  numberPlate: string;
  image_url: string;
  vehicleType: string;
  status: "in" | "out";
}

// Fetch data using axios
const fetcher = async (url: string): Promise<ApiResponse> => {
  const response = await axios.get<ApiResponse>(url);
  return response.data;
};

// Hook to use entries
export const useEntries = () => {
  // Use SWR for data fetching
  const { data, error, isLoading } = useSWR<ApiResponse>(
    API_CONFIG.lastEntries,
    fetcher
  );

  // Handle cases with error, loading, or no data
  if (error) {
    // console.error("Error fetching data:", error);
  }

  if (!data || !data.result) {
    return {
      newest: null,
      previous: [],
      loading: isLoading,
      error: error ? "Failed to load data" : null,
    };
  }

  // Destructure result array
  const { result } = data;

  // Format and structure the newest entry
  const formatEntry = (item: ApiResponse["result"][number]): Entry => {
    const { year, month, date, hour, minute, second } = item.day;
    return {
      date: `${year}/${String(month).padStart(2, "0")}/${String(date).padStart(
        2,
        "0"
      )}`,
      time: `${String(hour).padStart(2, "0")}:${String(minute).padStart(
        2,
        "0"
      )}:${String(second).padStart(2, "0")}`,
      numberPlate: item.number_plate,
      vehicleType:
        item.vehicle_type.toLowerCase() === "" ? "Other" : item.vehicle_type,
      status: item.status.toLowerCase() === "in" ? "in" : "out",
      image_url: item.image_url,
    };
  };

  // Find the newest entry
  const newest: Entry | null = result[0] ? formatEntry(result[0]) : null;

  // Map the previous entries
  const previous: Entry[] = result.slice(0, 4).map(formatEntry);

  return {
    newest,
    previous,
    loading: isLoading,
    error: error ? "Failed to load data" : null,
  };
};
