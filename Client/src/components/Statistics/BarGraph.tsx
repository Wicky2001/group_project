import React from "react";
import "./BarGraph.css";

// Define TrafficData type
interface TrafficData {
  type: string;
  inCount: number;
  outCount: number;
}

// Define props for BarGraph component
interface BarGraphProps {
  trafficData: TrafficData[];
}

// const maxCount = Math.max(
//   TrafficData[].map((data: { inCount: number; outCount: number; }) => Math.max(data.inCount, data.outCount))
// );

const BarGraph: React.FC<BarGraphProps> = ({ trafficData }) => {
  const maxCount = Math.max(
    ...trafficData.map((data) => Math.max(data.inCount, data.outCount))
  );

  return (
    <div className="bar-graph">
      {trafficData.map((data) => (
        <div key={data.type} className="bar">
          <span className="label">{data.type}</span>
          <div className="bar-container">
            <div
              className="bar-in"
              style={{
                width: `${(data.inCount / maxCount) * 100}%`,
                // height: "10px",
              }}
            >
              {data.inCount}
            </div>
            <div
              className="bar-out"
              style={{
                width: `${(data.outCount / maxCount) * 100}%`,
                // height: "10px",
              }}
            >
              {data.outCount}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default BarGraph;
