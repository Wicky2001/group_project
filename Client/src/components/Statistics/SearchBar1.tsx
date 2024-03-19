// SearchBar.tsx
import React, { useState } from "react";
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
  const [endDate, setEndDate] = useState("2024-03-07");
  const [startTime, setStartTime] = useState("00:00 AM");
  const [endTime, setEndTime] = useState("24:00 PM");

  const handleSearch = () => {
    onSearch(startDate, endDate, startTime, endTime);
  };

  const handleClear = () => {
    setStartDate("2024-02-01");
    setEndDate("2024-03-07");
    setStartTime("00:00 AM");
    setEndTime("24:00 PM");
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
        onChange={(e) => setStartTime(e.target.value)}
      />
      <input
        type="time"
        value={endTime}
        onChange={(e) => setEndTime(e.target.value)}
      />
      <button onClick={handleSearch}>Search</button>
      <button onClick={handleClear}>Clear</button>
    </div>
  );
};

export default SearchBar1;
