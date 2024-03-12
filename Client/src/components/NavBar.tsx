// src/Components/NavBar/NavBar.tsx
import Container from "react-bootstrap/Container";
import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";
import "./NavBar.css";

function NavBar() {
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
            <Nav.Link href="/" className="nav-link py-3 px-4 text-dark fw-bold">
              Dashboard
            </Nav.Link>
            <Nav.Link
              href="/statistics"
              className="nav-link py-3 px-4 text-dark fw-bold"
            >
              Statistics
            </Nav.Link>
            <Nav.Link
              href="/logs"
              className="nav-link py-3 px-4 text-dark fw-bold"
            >
              Logs
            </Nav.Link>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}

export default NavBar;
