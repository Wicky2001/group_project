import React, { useState, useEffect } from "react";
import NavBar from "../NavBar";
import StatStyle from "./Statistics.module.css";
import SearchBar1 from "./SearchBar1";
import Summery from "./Summery";
import Graph1 from "./Graph1";
import axios from "axios";
import Graph2 from "./Graph2";
import API_CONFIG from "../API";

const Statistics: React.FC = () => {
  const [summaryData, setSummaryData] = useState<any>({
    totalIn: 0,
    totalOut: 0,
  });
  const [graph1Data, setGraph1Data] = useState<any[]>([]);

  useEffect(() => {
    // Initial search to load data on component mount
    handleSearch(getCurrentDate(), getCurrentDate(), "00:00:00", "23:59:00");
  }, []);

  const handleSearch = async (
    startDate: string,
    endDate: string,
    startTime: string,
    endTime: string
  ) => {
    try {
      const response = await axios.get(API_CONFIG.searchByDate, {
        params: { startDate, endDate, startTime, endTime, statics: true },
      });
      setSummaryData(response.data.summary);
      setGraph1Data(response.data.result);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  function getCurrentDate(): string {
    const currentDate = new Date();
    const year = currentDate.getFullYear();
    const month = String(currentDate.getMonth() + 1).padStart(2, "0");
    const day = String(currentDate.getDate()).padStart(2, "0");
    return `${year}-${month}-${day}`;
  }

  return (
    <>
      <div className={StatStyle.container}>
        <div className={StatStyle.navbar}>
          <NavBar />
        </div>
        <div className={StatStyle.searchbar}>
          <SearchBar1 onSearch={handleSearch} />
        </div>
        <div className={StatStyle.chart1}>
          <Summery summaryData={summaryData} />
        </div>
        <div className={StatStyle.chart2}>
          <Graph1 responseData={graph1Data} />
        </div>
        <div className={StatStyle.chart3}>
          <Graph2 />
        </div>
      </div>
    </>
  );
};

export default Statistics;
