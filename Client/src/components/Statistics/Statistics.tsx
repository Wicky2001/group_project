import React, { useEffect, useState } from "react";
import NavBar from "../NavBar";
import StatStyle from "./Statistics.module.css";
import SearchBar1 from "./SearchBar1";
import Summery from "./Summery";
import Graph1 from "./Graph1";
import Graph2 from "./Graph2";
import axios from "axios";

// Statistics component
const Statistics: React.FC = () => {
  const [summaryData, setSummaryData] = useState<any>({
    totalIn: 0,
    totalOut: 0,
  }); // State to store summary data

  const [graph1Data, setGraph1Data] = useState<any[]>([]); // State to store graph1 data

  const handleSearch = async (
    startDate: string,
    endDate: string,
    startTime: string,
    endTime: string
  ) => {
    console.log("Search:", startDate, endDate, startTime, endTime);
    try {
      // Make the API request using Axios or any other HTTP client library
      const response = await axios.get(`http://localhost:5002/searchByDate`, {
        params: {
          startDate,
          endDate,
          startTime,
          endTime,
          statics: true,
        },
      });

      // Handle the API response
      //console.log(response.data);
      setSummaryData(response.data.summary); // Store summary data in state
      setGraph1Data(response.data.result); // Store graph1 data in state
    } catch (error) {
      console.error("Error:", error);
    }
  };

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
