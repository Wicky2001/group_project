import React, { useEffect, useState } from "react";
import { detection, useData } from "./Hooks/useData";

const App = () => {
  const [toggle, setToggle] = useState(true);
  // useEffect(() => {
  // const fetchData = async () => {
  //   try {
  //     const response = await fetch("http://127.0.0.1:5001/lastEntry", {
  //       method: "GET",
  //       headers: {
  //         "Content-Type": "application/json",
  //         // Add any other required headers
  //       },
  //       // Add body if needed
  //     });

  //     if (!response.ok) {
  //       throw new Error("Network response was not ok");
  //     }
  //     console.log("hhhh");
  //     // Handle the response data
  //     const data = await response.json();
  //     console.log(data);
  //   } catch (error) {
  //     console.error("Error fetching data:", error);
  //   }
  // };

  // fetchData();
  // }, []);

  const { Data } = useData<detection>("/lastEntry", toggle);

  return (
    <div>
      {/* <button
        onClick={() => {
          setToggle(!toggle);
        }}
        style={{ backgroundColor: "red" }}
      >
        click
      </button> */}
      {Data && (
        <div>
          <h2>API Response:</h2>
          <pre>{Data.number_plate}</pre>
        </div>
      )}
    </div>
  );
};

export default App;
