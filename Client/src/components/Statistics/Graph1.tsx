import React from "react";
import "./Graph1.css";
import BarGraph from "./BarGraph";

interface TrafficData {
  type: string;
  inCount: number;
  outCount: number;
}

interface ResponseData {
  status: string;
  total: number;
  vehicle_type: string;
}

const Graph1: React.FC<{ responseData: ResponseData[] }> = ({
  responseData,
}) => {
  // Transform the response data into the format expected by Graph1
  const trafficData: TrafficData[] = responseData.reduce(
    (acc: TrafficData[], item) => {
      const vehicleType = item.vehicle_type.trim() || "Other";
      const existingIndex = acc.findIndex((data) => data.type === vehicleType);
      if (existingIndex !== -1) {
        if (item.status === "IN") {
          acc[existingIndex].inCount += item.total;
        } else if (item.status === "OUT") {
          acc[existingIndex].outCount += item.total;
        }
      } else {
        const newItem: TrafficData = {
          type: vehicleType,
          inCount: item.status === "IN" ? item.total : 0,
          outCount: item.status === "OUT" ? item.total : 0,
        };
        acc.push(newItem);
      }
      return acc;
    },
    []
  );

  return (
    <>
      <div className="traffic-throughput">
        <div className="types">
          <div className="head">Types</div>
          {trafficData.map((data) => (
            <div key={data.type} className="type">
              <span>{data.type}</span>
              <span className="count in">
                <span>{data.inCount}</span>
              </span>
              <span className="count out">
                <span>{data.outCount}</span>
              </span>
            </div>
          ))}
        </div>
        <div className="bar-graph-container">
          {/* Render the BarGraph component with trafficData */}
          <BarGraph trafficData={trafficData} />
        </div>
      </div>
    </>
  );
};

export default Graph1;
