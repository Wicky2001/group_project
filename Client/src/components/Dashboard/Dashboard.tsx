import NavBar from "../NavBar";
import Newest from "./Newest";
import Previous from "./Previous";
import CameraFeeds from "./CameraFeeds";
import ManualEntry from "./ManualEntry";
import TodaysSummery from "./TodaysSummery";

import styles from "./Dashboard.module.css";

function Dashboard() {
  return (
    <div className={styles.container}>
      <div className={styles.navbar}>
        <NavBar />
      </div>
      <div className={styles.previousEntries}>
        <Previous />
      </div>
      <div className={styles.cameraFeeds}>
        <CameraFeeds />
      </div>
      <div className={styles.newestEntry}>
        <Newest />
      </div>
      <div className={styles.manualEntry}>
        <ManualEntry />
      </div>
      <div className={styles.todaysSummary}>
        <div>
          <TodaysSummery
            // totalEntered={850}
            // totalLeft={700}
            // stillInPremise={150}
            // anomalies={5}
          />
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
