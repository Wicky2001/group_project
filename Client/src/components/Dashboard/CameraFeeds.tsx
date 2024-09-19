import API_CONFIG from "../API";
import "./CameraFeeds.css";
import React, { useState } from "react";

const CameraFeeds: React.FC = () => {
  const [hasError, setHasError] = useState(false);

  const handleError = () => {
    setHasError(true);
  };

  return (
    <div>
      {hasError ? (
        <div className="container">
          <h1>Camera Feed</h1>
          <h1>Camera Feed</h1>
        </div>
      ) : (
        <div className="stram-container">
          <img
            src={API_CONFIG.videoFeed}
            alt="Stream"
            style={{ width: "auto", maxHeight: "360px", overflow: "hidden" }}
            onError={handleError}
          />
          <img
            src={API_CONFIG.videoFeed}
            alt="Stream"
            style={{ width: "auto", maxHeight: "360px", overflow: "hidden" }}
            onError={handleError}
          />
        </div>
      )}
    </div>
  );
};

export default CameraFeeds;
