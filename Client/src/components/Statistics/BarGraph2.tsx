import React from "react";
import "./BarGraph.css";

// Define TrafficData type based on the API response
interface TrafficData {
  hour?: number; // Optional, present for hour-based data
  month?: number; // Optional, present for month-based data
  year?: number; // Optional, present for year-based data
  status: string;
  total: number;
}

// Define props for BarGraph2 component
interface BarGraph2Props {
  data: TrafficData[];
}

// Month names array
const monthNames = [
  "January",
  "February",
  "March",
  "April",
  "May",
  "June",
  "July",
  "August",
  "September",
  "October",
  "November",
  "December",
];

const BarGraph2: React.FC<BarGraph2Props> = ({ data }) => {
  // Process the data to get counts for each period
  const processedData = data.reduce(
    (acc: { [key: string]: { inCount: number; outCount: number } }, item) => {
      const { hour, month, year, status, total } = item;
      const periodKey =
        hour !== undefined
          ? `${hour}:00`
          : month !== undefined
          ? monthNames[month - 1]
          : year !== undefined
          ? year
          : "";

      if (!acc[periodKey]) {
        acc[periodKey] = { inCount: 0, outCount: 0 };
      }

      if (status.toUpperCase() === "IN") {
        acc[periodKey].inCount += total;
      } else if (status.toUpperCase() === "OUT") {
        acc[periodKey].outCount += total;
      }

      return acc;
    },
    {}
  );

  // Convert the processed data to an array
  const trafficData = Object.entries(processedData).map(([period, counts]) => ({
    type: period,
    inCount: counts.inCount,
    outCount: counts.outCount,
  }));

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

export default BarGraph2;
