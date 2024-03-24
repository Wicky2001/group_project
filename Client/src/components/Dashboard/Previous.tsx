import React from "react";
import styles from "./Previous.module.css";
import { useEntries } from "./lastEntries";

const Previous: React.FC = () => {
  const { previous } = useEntries();

  return (
    <div className={styles.container}>
      <div className={styles.header}>Previous Entries</div>
      <div className={styles.scrollContainer}>
        <div className={styles.entriesContainer}>
          {previous.map((entry, index) => (
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
    </div>
  );
};

export default Previous;
