import React from "react";
import styles from "./Newest.module.css";
import img1 from "../../../public/detected_vehicles_images/AKL60362024-03-25_12-36-23.jpg";
import { useEntries } from "./lastEntries";

const Newest: React.FC = () => {
  const { newest } = useEntries();

  if (!newest) {
    return <div>No data available</div>;
  }

  const { date, time, numberPlate, vehicleType, status } = newest;
  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <div className={styles.newestEntry}>Newest Entry</div>
        <div className={styles.timestamp}>{date}</div>
        <div className={styles.timestamp}>{time}</div>
      </div>
      <div className={styles.container2}>
        <div className={styles.detailsContainer}>
          <div className={styles.detailRow}>
            <div className={styles.label}>Number Plate</div>
            <div
              className={`${styles.value} ${styles.valueRounded} ${styles.vtype}`}
            >
              {numberPlate}
            </div>
          </div>
          <div className={styles.detailRow}>
            <div className={styles.label}>Vehicle Type</div>
            <div className={`${styles.value} ${styles.valueRounded}`}>
              {vehicleType}
            </div>
          </div>
          <div className={styles.detailRow}>
            <div className={styles.label}>Status</div>
            <div
              className={`${styles.value} ${
                status.toLowerCase() === "out"
                  ? styles.valueRed
                  : styles.valueGreen
              }`}
            >
              {status}
            </div>
          </div>
        </div>
        <div className={styles.img}>
          <div className={styles.vehicleImageContainer}>
            <img src={img1} alt="Vehicle" className={styles.vehicleImage} />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Newest;
