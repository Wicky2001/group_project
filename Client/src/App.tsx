import { BrowserRouter, Routes, Route } from "react-router-dom";
//import NavBar from "./components/NavBar";
import Dashboard from "./components/Dashboard/Dashboard";
import Statistics from "./components/Statistics/Statistics";
import Logs from "./components/Logs/Logs";
import "./App.css";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Dashboard />} />{" "}
        <Route path="/statistics" element={<Statistics />} />{" "}
        <Route path="/logs" element={<Logs />} />{" "}
      </Routes>
    </BrowserRouter>
  );
}

export default App;
