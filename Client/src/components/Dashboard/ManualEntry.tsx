import React, { useState } from "react";
import "./ManualEntry.css";

const ManualEntry: React.FC = () => {
  const [numberPlate, setNumberPlate] = useState("");
  const [vehicleType, setVehicleType] = useState("");
  const [status, setStatus] = useState<"IN" | "Out">("IN");

  const handleNumberPlateChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setNumberPlate(e.target.value);
  };

  const handleVehicleTypeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setVehicleType(e.target.value);
  };

  const handleStatusChange = (newStatus: "IN" | "Out") => {
    setStatus(newStatus);
  };

  // const handleClear = () => {
  //   setNumberPlate("");
  //   setVehicleType("");
  //   setStatus("IN");
  // };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Submit logic goes here
    console.log("Number Plate:", numberPlate);
    console.log("Vehicle Type:", vehicleType);
    console.log("Status:", status);
  };

  return (
    <div className="manual-entry">
      <div className="header">
        <h2>Manual Entry</h2>
        <span className="timestamp">2024-03-07 12:26:30 PM</span>
      </div>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="numberPlate">Number Plate</label>
          <input
            type="text"
            id="numberPlate"
            value={numberPlate}
            onChange={handleNumberPlateChange}
          />
        </div>
        <div className="form-group">
          <label htmlFor="vehicleType">Vehicle Type</label>
          <input
            type="text"
            id="vehicleType"
            value={vehicleType}
            onChange={handleVehicleTypeChange}
          />
        </div>

        <div className="form-group status">
          <label>Status</label>
          <div className="status-buttons">
            <button
              type="button"
              className={`status-button ${status === "IN" ? "active" : ""}`}
              onClick={() => handleStatusChange("IN")}
            >
              IN
            </button>
            <button
              type="button"
              className={`status-button ${status === "Out" ? "activered" : ""}`}
              onClick={() => handleStatusChange("Out")}
            >
              Out
            </button>
          </div>

          <div className="form-actions">
            <button type="submit" className="submit-button">
              Submit
            </button>
          </div>
        </div>
      </form>
    </div>
  );
};

export default ManualEntry;
