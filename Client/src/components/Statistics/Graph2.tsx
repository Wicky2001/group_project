import React, { useState, useEffect } from "react";
import BarGraph2 from "./BarGraph2"; // Updated component
import "./Graph2.css";

interface TrafficData {
  hour: number;
  status: string;
  total: number;
}

const Graph2: React.FC = () => {
  const [timePeriod, setTimePeriod] = useState<"hour" | "month" | "year">(
    "hour"
  );
  const [data, setData] = useState<TrafficData[]>([]);

  // Fetch data from the backend based on the selected time period
  const fetchTrafficData = async () => {
    try {
      let apiUrl = "http://localhost:5002/sortTraffic?";
      if (timePeriod === "hour") {
        apiUrl += "hour=true";
      } else if (timePeriod === "month") {
        apiUrl += "month=true";
      } else if (timePeriod === "year") {
        apiUrl += "year=true";
      }

      const response = await fetch(apiUrl);
      const result = await response.json();

      if (result.summary) {
        setData(result.summary);
      } else {
        console.error("Unexpected data format:", result);
      }
    } catch (error) {
      console.error("Error fetching traffic data:", error);
    }
  };

  useEffect(() => {
    fetchTrafficData();
  }, [timePeriod]);

  return (
    <div className="traffic-chart">
      <div className="sort-traffic">
        <button
          onClick={() => setTimePeriod("hour")}
          className={timePeriod === "hour" ? "active1" : ""}
        >
          Hours
        </button>
        <button
          onClick={() => setTimePeriod("month")}
          className={timePeriod === "month" ? "active1" : ""}
        >
          Months
        </button>
        <button
          onClick={() => setTimePeriod("year")}
          className={timePeriod === "year" ? "active1" : ""}
        >
          Years
        </button>
      </div>
      <BarGraph2 data={data} />
    </div>
  );
};

export default Graph2;
