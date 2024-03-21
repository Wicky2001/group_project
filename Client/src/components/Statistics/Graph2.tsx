import React, { useState } from "react";
import "./Graph2.css";

interface TrafficData {
  label: string; // This can be day, hour, month, or year
  inCount: number;
  outCount: number;
}

const Graph2: React.FC = () => {
  const [timePeriod, setTimePeriod] = useState<
    "hours" | "days" | "months" | "years"
  >("days");
  const [trafficData, setTrafficData] = useState<TrafficData[]>([]);

  // Fetch data from the backend based on the selected time period
  const fetchTrafficData = async () => {
    try {
      // Replace with your actual API call or data fetching logic
      const response = await fetch(`/api/traffic-data?period=${timePeriod}`);
      const data = await response.json();
      setTrafficData(data);
    } catch (error) {
      console.error("Error fetching traffic data:", error);
    }
  };

  React.useEffect(() => {
    fetchTrafficData();
  }, [timePeriod]);

  const maxCount = Math.max(
    ...trafficData.map((data) => Math.max(data.inCount, data.outCount))
  );

  const getXAxisLabel = (data: TrafficData) => {
    if (timePeriod === "hours") {
      return `${data.label}:00`;
    } else if (timePeriod === "days") {
      const weekdays = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
      ];
      return weekdays[parseInt(data.label)];
    } else if (timePeriod === "months") {
      const months = [
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
      return months[parseInt(data.label) - 1];
    } else if (timePeriod === "years") {
      return data.label;
    }
    return data.label;
  };

  return (
    <div className="traffic-chart">
      <div className="sort-traffic">
        <button
          onClick={() => setTimePeriod("hours")}
          className={timePeriod === "hours" ? "active1" : ""}
        >
          Hours
        </button>
        <button
          onClick={() => setTimePeriod("days")}
          className={timePeriod === "days" ? "active1" : ""}
        >
          Days
        </button>
        <button
          onClick={() => setTimePeriod("months")}
          className={timePeriod === "months" ? "active1" : ""}
        >
          Months
        </button>
        <button
          onClick={() => setTimePeriod("years")}
          className={timePeriod === "years" ? "active1" : ""}
        >
          Years
        </button>
      </div>
      <div className="chart-container">
        <div className="y-axis">
          {Array.from({ length: 6 }, (_, i) => (
            <div key={i} className="y-axis-label">
              {(maxCount * (i / 5)).toFixed(0)}
            </div>
          ))}
        </div>
        <div className="bars">
          {trafficData.map((data) => (
            <div key={data.label} className="bar-group">
              <div
                className="bar in"
                style={{ height: `${(data.inCount / maxCount) * 100}%` }}
              ></div>
              <div
                className="bar out"
                style={{ height: `${(data.outCount / maxCount) * 100}%` }}
              ></div>
              <div className="bar-label">{getXAxisLabel(data)}</div>
            </div>
          ))}
        </div>
      </div>
      <div className="legend">
        <div className="legend-item">
          <div className="legend-color in"></div>
          <span>In</span>
        </div>
        <div className="legend-item">
          <div className="legend-color out"></div>
          <span>Out</span>
        </div>
      </div>
    </div>
  );
};

export default Graph2;
