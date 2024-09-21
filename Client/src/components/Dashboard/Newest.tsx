import React from "react";
import styles from "./Newest.module.css";

//import img1 from "../../../public/detected_vehicles_images/CK191192024-03-24_16-23-36.jpg";
import { useEntries } from "./lastEntries";

const Newest: React.FC = () => {
  const { newest } = useEntries();

  if (!newest) {
    return (
      <div className={styles.container}>
        <div className={styles.header}>
          <div className={styles.newestEntry}>Newest Entry</div>
        </div>
      </div>
    );
  }

  const { date, time, numberPlate, image_url, vehicleType, status } = newest;
  // const image = process.env.PUBLIC_URL + image_url;
  console.log(image_url);
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
            <img src={image_url} alt="Vehic" className={styles.vehicleImage} />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Newest;
