import React from "react";
import "./Summery.css";

interface SummeryProps {
  totalEntered: number;
  totalLeft: number;
  stillInPremise: number;
  anomalies: number;
}

const Summery: React.FC<SummeryProps> = ({
  totalEntered,
  totalLeft,
  stillInPremise,
  anomalies,
}) => {
  return (
    <div className="summery">
      <h2>Summery</h2>
      <div className="summery-item">
        <span className="label">Total Entered</span>
        <div className="value entered">{totalEntered}</div>
      </div>
      <div className="summery-item">
        <span className="label">Total Left</span>
        <div className="value left">{totalLeft}</div>
      </div>
      <div className="summery-item">
        <span className="label">Still In Premise</span>
        <div className="value in-premise">{stillInPremise}</div>
      </div>
      <div className="summery-item">
        <span className="label">Anomalies</span>
        <div className="value anomalies">{anomalies}</div>
      </div>
    </div>
  );
};

export default Summery;
