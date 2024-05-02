import useSWR from "swr";
import axios from "axios";

interface ApiResponse {
  length: number;
  result: {
    day: {
      year: number;
      month: number;
      date: number;
      hour: number;
      minute: number;
      second: number;
    };
    number_plate: string;
    vehicle_type: string;
    status: string;
  }[];
}

interface Entry {
  date: string;
  time: string;
  numberPlate: string;
  vehicleType: string;
  status: "in" | "out";
}

const fetcher = (url: string) => axios.get(url).then((res) => res.data);

export const useEntries = () => {
  const { data, error } = useSWR<ApiResponse>(
    "http://127.0.0.1:5002/lastEntry",
    fetcher,
    {
      refreshInterval: 1000, // Refresh every 5 seconds
    }
  );

  if (error) {
    console.error("Error fetching data:", error);
    return { newest: null, previous: [] };
  }

  if (!data || !data.result) {
    return { newest: null, previous: [] };
  }

  const result = data.result;
  const newest = result[0]
    ? {
        date: `${result[0].day.year}/${result[0].day.month}/${result[0].day.date}`,
        time: `${result[0].day.hour}:${result[0].day.minute}:${result[0].day.second}`,
        numberPlate: result[0].number_plate,
        vehicleType:
          result[0].vehicle_type.toLowerCase() === ""
            ? "Other"
            : result[0].vehicle_type,
        status: result[0].status.toLowerCase() === "in" ? "in" : "out",
      }
    : null;

  const previous: Entry[] = result.slice(0, 4).map((item) => ({
    date: `${item.day.year}/${item.day.month}/${item.day.date}`,
    time: `${item.day.hour}:${item.day.minute}:${item.day.second}`,
    numberPlate: item.number_plate,
    vehicleType:
      item.vehicle_type.toLowerCase() === "" ? "Other" : item.vehicle_type,
    status: item.status.toLowerCase() === "in" ? "in" : "out",
  }));

  return { newest, previous };
};
