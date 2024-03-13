import React from "react";
import NavBar from "../NavBar";
import StatStyle from "./Statistics.module.css";
import SearchBar1 from "./SearchBar1";
import Summery from "./Summery";
import Graph1 from "./Graph1";
import Graph2 from "./Graph2";

const Statistics: React.FC = () => {
  const handleSearch = (
    startDate: string,
    endDate: string,
    startTime: string,
    endTime: string
  ) => {
    console.log("Search:", startDate, endDate, startTime, endTime);
    // Perform your search logic here
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
          <Summery
            totalEntered={850}
            totalLeft={700}
            stillInPremise={150}
            anomalies={5}
          />
        </div>
        <div className={StatStyle.chart2}>
          <Graph1 />
        </div>
        <div className={StatStyle.chart3}>
          <Graph2 />
        </div>
      </div>
    </>
  );
};

export default Statistics;
