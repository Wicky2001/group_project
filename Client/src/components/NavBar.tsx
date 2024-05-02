// src/Components/NavBar/NavBar.tsx
import Container from "react-bootstrap/Container";
import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";
import dsh from "../assets/dashico.png";
import log from "../assets/logico.png";
import stat from "../assets/Statico.png";
import { useLocation } from "react-router-dom";
import "./NavBar.css";

function NavBar() {
  const location = useLocation();
  return (
    <Navbar
      bg="light"
      expand="lg"
      className="flex-column flex-shrink-0 h-100 navbar shadow-sm mb-4"
    >
      <Container fluid>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="me-auto flex-column font text-dark">
            <Nav.Link
              href="/"
              className={location.pathname === "/" ? "active" : ""}
            >
              <img
                src={dsh}
                alt="Dashboard"
                className="holder py-3 px-4 text-dark fw-bold"
              />
            </Nav.Link>
            <Nav.Link
              href="/statistics"
              className={location.pathname === "/statistics" ? "active" : ""}
            >
              <img
                src={stat}
                alt="Statistics"
                className="holder py-3 px-4 text-dark fw-bold"
              />
            </Nav.Link>
            <Nav.Link
              href="/logs"
              className={location.pathname === "/logs" ? "active" : ""}
            >
              <img
                src={log}
                alt="Logs"
                className="holder py-3 px-4 text-dark fw-bold"
              />
            </Nav.Link>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}

export default NavBar;
