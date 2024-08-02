import React from "react";
import styles from "./Container.module.css";

interface Entry {
  id: number;
  day: {
    year: number;
    month: number;
    date: number;
    hour: number;
    minute: number;
  };
  number_plate: string;
  vehicle_type: string;
  status: string;
}

interface ContainerProps {
  responseData: Entry[];
}

const Container: React.FC<ContainerProps> = ({ responseData }) => {
  // Reverse the array to display the entries in the 'last entries first' order
  const reversedEntries = responseData.slice().reverse();
  return (
    <div className={styles.test1}>
      <div className={styles.header}>Logs</div>
      <div className={styles.entriesContainer}>
        {reversedEntries.map((entry, index) => (
          <div key={index} className={styles.entryContainer}>
            <div className={styles.entryDetails}>
              <div className={styles.date}>
                {`${entry.day.year}-${entry.day.month}-${entry.day.date} ${entry.day.hour}:${entry.day.minute}`}
              </div>
              <div className={styles.numberPlate}>{entry.number_plate}</div>
              <div className={styles.vehicleType}>{entry.vehicle_type}</div>
            </div>
            <div
              className={`${styles.statusIndicator} ${
                entry.status === "IN" ? styles.statusIn : styles.statusOut
              }`}
            />
          </div>
        ))}
      </div>
    </div>
  );
};

export default Container;
