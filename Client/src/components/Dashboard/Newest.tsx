import React from "react";
import styles from "./Newest.module.css";

interface Newest {}

const Newest: React.FC<Newest> = () => {
  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <div className={styles.newestEntry}>Newest Entry</div>
        <div className={styles.timestamp}>2024-03-07 12:26:30 PM</div>
      </div>

      <div className={styles.detailsContainer}>
        <div className={styles.detailRow}>
          <div className={styles.label}>Number Plate</div>
          <div className={`${styles.value} ${styles.valueRounded}`}>
            CV 7845
          </div>
        </div>
        <div className={styles.detailRow}>
          <div className={styles.label}>Vehicle Type</div>
          <div className={`${styles.value} ${styles.valueRounded}`}>VAN</div>
        </div>
        <div className={styles.detailRow}>
          <div className={styles.label}>Status</div>
          <div className={`${styles.value} ${styles.valueGreen}`}>IN</div>
        </div>
      </div>
    </div>
  );
};

export default Newest;
//<div className={styles.newestEntryContainer}>wwsssssssssss</div>
