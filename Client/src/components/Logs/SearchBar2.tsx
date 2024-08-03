// SearchBar.tsx
import React, { useEffect, useState } from "react";
import "./SearchBar2.css";

interface SearchBarProps {
  onSearch: (
    startDate: string,
    endDate: string,
    startTime: string,
    endTime: string,
    numberPlate: string,
    vehicleType: string
  ) => void;
}

const SearchBar2: React.FC<SearchBarProps> = ({ onSearch }) => {
  const [startDate, setStartDate] = useState("2024-02-01");
  const [endDate, setEndDate] = useState(getCurrentDate());
  const [startTime, setStartTime] = useState("00:00:00");
  const [endTime, setEndTime] = useState("23:59:00");
  const [numberPlate, setNumberPlate] = useState("");
  const [vehicleType, setVehicleType] = useState("All");

  useEffect(() => {
    // Invoke onSearch with initial search parameters when component mounts
    onSearch(startDate, endDate, startTime, endTime, numberPlate, vehicleType);
  }, []); // Empty dependency array to run once on component mount

  // Function to get the current date in the yyyy-mm-dd format
  function getCurrentDate(): string {
    const currentDate = new Date();
    const year = currentDate.getFullYear();
    const month = String(currentDate.getMonth() + 1).padStart(2, "0"); // January is 0!
    const day = String(currentDate.getDate()).padStart(2, "0");

    return `${year}-${month}-${day}`;
  }

  // Function to handle setting start time
  const handleSetStartTime = (value: string) => {
    setStartTime(value + ":00"); // Append ":00" for seconds
  };

  // Function to handle setting end time
  const handleSetEndTime = (value: string) => {
    setEndTime(value + ":00"); // Append ":00" for seconds
  };

  const handleSearch = () => {
    onSearch(startDate, endDate, startTime, endTime, numberPlate, vehicleType);
  };

  const handleClear = () => {
    setStartDate("2024-02-01");
    setEndDate(getCurrentDate());
    handleSetStartTime("00:00");
    handleSetEndTime("23:59");
    setNumberPlate("");
    setVehicleType("All");
  };

  return (
    <div className="search-bar">
      <input
        type="date"
        value={startDate}
        onChange={(e) => setStartDate(e.target.value)}
      />
      <input
        type="date"
        value={endDate}
        onChange={(e) => setEndDate(e.target.value)}
      />
      <input
        type="time"
        value={startTime}
        onChange={(e) => handleSetStartTime(e.target.value)}
      />
      <input
        type="time"
        value={endTime}
        onChange={(e) => handleSetEndTime(e.target.value)}
      />
      <input
        type="text"
        placeholder="Vehicle number"
        value={numberPlate}
        onChange={(e) => setNumberPlate(e.target.value)}
      />
      <select
        value={vehicleType}
        onChange={(e) => setVehicleType(e.target.value)}
      >
        <option value="All">Vehicle Type</option>
        <option value="Car">Car</option>
        <option value="van">Van</option>
        <option value="lorry">Lorry</option>
        <option value="Other">Other</option>
        <option value="Truck">Truck</option>
        <option value="Motorcycle">Motorcycle</option>
        {/* Add more options as needed */}
      </select>
      <button onClick={handleSearch}>Search</button>
      <button onClick={handleClear}>Clear</button>
    </div>
  );
};

export default SearchBar2;
