//TodaysSummery.tsx
import React from "react";
import "./TodaysSummery.css";
import useFetchDaySummary from "./useFetchDaySummary";

const TodaysSummery: React.FC = () => {
  const { daySummary, isLoading, isError } = useFetchDaySummary();

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (isError) {
    return <div>No Data to Fetch.</div>;
  }

  const { total_entered, total_left, still_in_premise, anomalies } =
    daySummary || {};

  return (
    <div className="today-summery">
      <h2>Today's Summery</h2>
      <div className="summery-item">
        <span className="label">Total Entered</span>
        <div className="value entered">{total_entered}</div>
      </div>
      <div className="summery-item">
        <span className="label">Total Left</span>
        <div className="value left">{total_left}</div>
      </div>
      <div className="summery-item">
        <span className="label">Still In Premise</span>
        <div className="value in-premise">{still_in_premise}</div>
      </div>
    </div>
  );
};

export default TodaysSummery;
