// SearchBar.tsx
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
  const [startDate, setStartDate] = useState("2024-02-01");
  const [endDate, setEndDate] = useState(getCurrentDate());
  const [startTime, setStartTime] = useState("00:00:00");
  const [endTime, setEndTime] = useState("23:59:00");

  useEffect(() => {
    // Invoke onSearch with initial search parameters when component mounts
    onSearch(startDate, endDate, startTime, endTime);
  }, []); // Empty dependency array to run once on component mount

  const handleSearch = () => {
    onSearch(startDate, endDate, startTime, endTime);
  };

  // Function to handle setting start time
  const handleSetStartTime = (value: string) => {
    setStartTime(value + ":00"); // Append ":00" for seconds
  };

  // Function to handle setting end time
  const handleSetEndTime = (value: string) => {
    setEndTime(value + ":00"); // Append ":00" for seconds
  };

  const handleClear = () => {
    setStartDate("2024-02-01");
    setEndDate(getCurrentDate());
    setStartTime("00:00");
    setEndTime("11:59");
  };

  // Function to get the current date in the yyyy-mm-dd format
  function getCurrentDate(): string {
    const currentDate = new Date();
    const year = currentDate.getFullYear();
    const month = String(currentDate.getMonth() + 1).padStart(2, "0"); // January is 0!
    const day = String(currentDate.getDate()).padStart(2, "0");

    return `${year}-${month}-${day}`;
  }
  // Function to get the current time in the hh-mm-ss format
  // function getCurrentTime(): string {
  //   const currentTime = new Date();
  //   const hours = String(currentTime.getHours()).padStart(2, "0");
  //   const minutes = String(currentTime.getMinutes()).padStart(2, "0");
  //   return `${hours}:${minutes}:00`;
  // }

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
      <button onClick={handleSearch}>Search</button>
      <button onClick={handleClear}>Clear</button>
    </div>
  );
};

export default SearchBar1;
