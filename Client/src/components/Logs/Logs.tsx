import React, { useState } from "react";
import NavBar from "../NavBar";
import StatStyle from "./Statistics.module.css";
import SearchBar2 from "./SearchBar2";
import Container from "./Container";
import axios from "axios";

const Logs: React.FC = () => {
  const [responseData, setResponseData] = useState<any[]>([]); // State to store response data

  const handleSearch = async (
    startDate: string,
    endDate: string,
    startTime: string,
    endTime: string,
    numberPlate: string,
    vehicleType: string
  ) => {
    // For testing purpose for checking the parameter values
    console.log(
      "Search:",
      startDate,
      endDate,
      startTime,
      endTime,
      numberPlate,
      vehicleType
    );
    try {
      // Make the API request using Axios or any other HTTP client library
      const response = await axios.get(`http://localhost:5002/searchByDate`, {
        params: {
          startDate,
          endDate,
          startTime,
          endTime,
          numberPlate,
          vehicleType,
          statics: false,
        },
      });

      // Handle the API response
      console.log(response.data);
      setResponseData(response.data.result); // Store response data in state
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
          <SearchBar2 onSearch={handleSearch} />
        </div>
        <Container responseData={responseData} />{" "}
      </div>
    </>
  );
};

export default Logs;
