import React from "react";
import "./Graph1.css";

interface TrafficData {
  type: string;
  inCount: number;
  outCount: number;
}

const Graph1: React.FC = () => {
  const trafficData: TrafficData[] = [
    { type: "Cars", inCount: 880, outCount: 850 },
    { type: "Vans", inCount: 700, outCount: 700 },
    { type: "Trucks", inCount: 150, outCount: 150 },
    { type: "Bikes", inCount: 80, outCount: 80 },
    { type: "Other", inCount: 200, outCount: 200 },
  ];

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
        <div className="chart">
          <div className="axis">
            <span>0</span>
            <span>200</span>
            <span>400</span>
            <span>600</span>
            <span>800</span>
            <span>1000</span>
          </div>
          <div className="bars">
            {trafficData.map((data) => (
              <div key={data.type} className="bar-group">
                <div
                  className="bar out"
                  style={{ height: `${(data.outCount / 1000) * 100}%` }}
                ></div>
                <div
                  className="bar in"
                  style={{ height: `${(data.inCount / 1000) * 100}%` }}
                ></div>
              </div>
            ))}
          </div>
          <div className="legend">
            <span className="in-legend"></span>
            <span>In</span>
            <span className="out-legend"></span>
            <span>Out</span>
          </div>
        </div>
      </div>
    </>
  );
};

export default Graph1;
