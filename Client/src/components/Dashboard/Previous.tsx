import React from "react";
import styles from "./Previous.module.css";

interface Entry {
  date: string;
  numberPlate: string;
  vehicleType: string;
  status: "in" | "out";
}

const Previous: React.FC = () => {
  const entries: Entry[] = [
    {
      date: "2024-03-07 12:26:30 PM",
      numberPlate: "ABC 7842",
      vehicleType: "CAR",
      status: "in",
    },
    {
      date: "2024-03-07 12:26:30 PM",
      numberPlate: "ABC 7842",
      vehicleType: "CAR",
      status: "in",
    },
    {
      date: "2024-03-07 12:26:30 PM",
      numberPlate: "ABC 7842",
      vehicleType: "CAR",
      status: "out",
    },
    {
      date: "2024-03-07 12:26:30 PM",
      numberPlate: "ABC 7842",
      vehicleType: "CAR",
      status: "in",
    },
    {
      date: "2024-03-07 12:26:30 PM",
      numberPlate: "ABC 7842",
      vehicleType: "CAR",
      status: "in",
    },
  ];

  return (
    <div className={styles.container}>
      <div className={styles.header}>Previous Entries</div>
      <div className={styles.entriesContainer}>
        {entries.map((entry, index) => (
          <div key={index} className={styles.entryContainer}>
            <div className={styles.entryDetails}>
              <div className={styles.date}>{entry.date}</div>
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
