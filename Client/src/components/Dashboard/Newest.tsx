/*Newest.tsx*/
import React, { useState, useEffect } from "react";
import styles from "./Newest.module.css";
import img1 from "../../assets/r1.png";

interface Newest {
  numberPlate: string;
  vehicleType: string;
  status: string;
  imageUrl: string;
}

const Newest: React.FC = () => {
  const [vehicleData, setVehicleData] = useState<Newest>({
    numberPlate: "xxx0000",
    vehicleType: "Model",
    status: "In/Out",
    imageUrl: img1,
  });

  useEffect(() => {
    // Fetch vehicle data from the backend
    fetch("/api/vehicle-data")
      .then((response) => response.json())
      .then((data) => setVehicleData(data))
      .catch((error) => console.error("Error fetching vehicle data:", error));
  }, []);

  const { numberPlate, vehicleType, status, imageUrl } = vehicleData;

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <div className={styles.newestEntry}>Newest Entry</div>
        <div className={styles.timestamp}>2024-03-07 12:26:30 PM</div>
      </div>
      <div className={styles.container2}>
        <div className={styles.detailsContainer}>
          <div className={styles.detailRow}>
            <div className={styles.label}>Number Plate</div>
            <div className={`${styles.value} ${styles.valueRounded}`}>
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
            {imageUrl && (
              <img
                src={imageUrl}
                alt="Vehicle"
                className={styles.vehicleImage}
              />
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Newest;
