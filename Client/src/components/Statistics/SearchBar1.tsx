import React, { useEffect, useState } from "react";
import "./SearchBar1.css";

interface SearchBarProps {
  onSearch: (
    startDate: string,
    endDate: string,
    startTime: string,
    endTime: string
  ) => void;
}

const SearchBar1: React.FC<SearchBarProps> = ({ onSearch }) => {
  const [startDate, setStartDate] = useState(getCurrentDate());
  const [endDate, setEndDate] = useState(getCurrentDate());
  const [startTime, setStartTime] = useState("00:00:00");
  const [endTime, setEndTime] = useState("23:59:00");
  const [isClear, setIsClear] = useState(false);

  useEffect(() => {
    // Perform initial search when the component mounts
    onSearch(startDate, endDate, startTime, endTime);
  }, []);

  useEffect(() => {
    if (isClear) {
      // Perform search with default values when clear is triggered
      onSearch(startDate, endDate, startTime, endTime);
      setIsClear(false);
    }
  }, [isClear, startDate, endDate, startTime, endTime, onSearch]);

  const handleSearch = () => {
    onSearch(startDate, endDate, startTime, endTime);
  };

  const handleSetStartTime = (value: string) => {
    setStartTime(value + ":00");
  };

  const handleSetEndTime = (value: string) => {
    setEndTime(value + ":00");
  };

  const handleClear = () => {
    setStartDate(getCurrentDate());
    setEndDate(getCurrentDate());
    setStartTime("00:00:00");
    setEndTime("23:59:00");
    setIsClear(true);
  };

  function getCurrentDate(): string {
    const currentDate = new Date();
    const year = currentDate.getFullYear();
    const month = String(currentDate.getMonth() + 1).padStart(2, "0");
    const day = String(currentDate.getDate()).padStart(2, "0");
    return `${year}-${month}-${day}`;
  }

  return (
    <div className="search-bar">
      <label>From: </label>
      <input
        type="date"
        value={startDate}
        onChange={(e) => setStartDate(e.target.value)}
      />
      <label>To: </label>
      <input
        type="date"
        value={endDate}
        onChange={(e) => setEndDate(e.target.value)}
      />
      <label>From: </label>
      <input
        type="time"
        value={startTime.slice(0, 5)} // Adjust to "hh:mm" format for the input
        onChange={(e) => handleSetStartTime(e.target.value)}
      />
      <label>To: </label>
      <input
        type="time"
        value={endTime.slice(0, 5)} // Adjust to "hh:mm" format for the input
        onChange={(e) => handleSetEndTime(e.target.value)}
      />
      <button onClick={handleSearch}>Search</button>
      <button onClick={handleClear}>Clear</button>
    </div>
  );
};

export default SearchBar1;
