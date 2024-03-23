import React, { useState, useEffect } from "react";
import axios from "axios";
import styles from "./Previous.module.css";

interface Entry {
  date: string;
  time: string;
  numberPlate: string;
  vehicleType: string;
  status: "in" | "out";
}

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

const Previous: React.FC = () => {
  const [entries, setEntries] = useState<Entry[]>([]);

  useEffect(() => {
    const fetchEntries = async () => {
      try {
        const response = await axios.get<ApiResponse>(
          "http://127.0.0.1:5002/lastEntry"
        );
        const { result } = response.data;
        const entries: Entry[] = result.map((item) => ({
          date: `${item.day.year}/${item.day.month}/${item.day.date}`,
          time: `${item.day.hour}:${item.day.minute}:${item.day.second}`,
          numberPlate: item.number_plate,
          vehicleType:
            item.vehicle_type.toLowerCase() === ""
              ? "Other"
              : item.vehicle_type,
          status: item.status.toLowerCase() === "in" ? "in" : "out",
        }));
        setEntries(entries);
      } catch (error) {
        console.error("Error fetching entries:", error);
      }
    };

    fetchEntries();
  }, []);

  return (
    <div className={styles.container}>
      <div className={styles.header}>Previous Entries</div>
      <div className={styles.entriesContainer}>
        {entries.map((entry, index) => (
          <div key={index} className={styles.entryContainer}>
            <div className={styles.entryDetails}>
              <div className={styles.date}>{entry.date}</div>
              <div className={styles.time}>{entry.time}</div>
              <div className={styles.numberPlate}>{entry.numberPlate}</div>
              <div className={styles.vehicleType}>{entry.vehicleType}</div>
            </div>
            <div
              className={`${styles.statusIndicator} ${
                entry.status === "in" ? styles.statusIn : styles.statusOut
              }`}
            />
          </div>
        ))}
      </div>
    </div>
  );
};

export default Previous;
