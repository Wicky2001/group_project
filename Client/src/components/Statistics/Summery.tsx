import React from "react";
import "./Summery.css";

// Summery component
interface SummeryProps {
  summaryData: { totalIn: number; totalOut: number };
}

const Summery: React.FC<SummeryProps> = ({ summaryData }) => {
  const { totalIn, totalOut } = summaryData;
  const stillInPremise = totalIn - totalOut;

  return (
    <div className="summery">
      <h2>Summary</h2>
      <div className="summery-item">
        <span className="label">Total Entered</span>
        <div className="value entered">{totalIn}</div>
      </div>
      <div className="summery-item">
        <span className="label">Total Left</span>
        <div className="value left">{totalOut}</div>
      </div>
    </div>
  );
};

export default Summery;
