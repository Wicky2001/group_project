import React, { useState, useEffect } from "react";
import axios from "axios";
import "./ManualEntry.css";
import API_CONFIG from "../API";

interface FormData {
  numberPlate: string;
  vehicleType: string;
  status: "IN" | "OUT";
}

const ManualEntry: React.FC = () => {
  const [formData, setFormData] = useState<FormData>({
    numberPlate: "",
    vehicleType: "Other",
    status: "IN",
  });
  const [currentTime, setCurrentTime] = useState(new Date());

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentTime(new Date());
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  const handleNumberPlateChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, numberPlate: e.target.value.toUpperCase() });
  };

  const handleVehicleTypeChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setFormData({ ...formData, vehicleType: e.target.value });
  };

  const handleStatusChange = (newStatus: "IN" | "OUT") => {
    setFormData({ ...formData, status: newStatus });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Check if number plate is empty
    if (formData.numberPlate.trim() === "") {
      alert("Please enter a number plate.");
      return;
    }

    try {
      const entryDate = currentTime.toISOString().split("T")[0]; // YYYY-MM-DD
      const entryTime = currentTime.toLocaleTimeString([], { hour12: false }); // HH:MM:SS
      const response = await axios.post(API_CONFIG.addEntry, {
        entryDate,
        entryTime,
        ...formData,
      });
      console.log(response.data.message); // Log the response message

      // Reset form fields
      setFormData({
        numberPlate: "",
        vehicleType: "OTHER",
        status: "IN",
      });
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <div className="manual-entry">
      <div className="header">
        <h2>Manual Entry</h2>
        <span className="timestamp">
          {currentTime.toISOString().split("T")[0]}{" "}
        </span>
        <span className="timestamp">
          {currentTime.toLocaleString("en-US", {
            hour12: false,
            hour: "numeric",
            minute: "numeric",
            second: "numeric",
          })}
        </span>
      </div>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="numberPlate">Number Plate</label>
          <input
            type="text"
            id="numberPlate"
            value={formData.numberPlate}
            onChange={handleNumberPlateChange}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="vehicleType">Vehicle Type</label>
          <select
            id="vehicleType"
            value={formData.vehicleType}
            onChange={handleVehicleTypeChange}
          >
            <option value="Other">Other</option>
            <option value="Car">Car</option>
            <option value="Motorcycle">Motorcycle</option>
            <option value="Truck">Truck</option>
            {/* Add more options as needed */}
          </select>
        </div>
        <div className="form-group status">
          <label>Status</label>
          <div className="status-buttons">
            <button
              type="button"
              className={`status-button ${
                formData.status === "IN" ? "activegre" : ""
              }`}
              onClick={() => handleStatusChange("IN")}
            >
              IN
            </button>
            <button
              type="button"
              className={`status-button ${
                formData.status === "OUT" ? "activred" : ""
              }`}
              onClick={() => handleStatusChange("OUT")}
            >
              OUT
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
