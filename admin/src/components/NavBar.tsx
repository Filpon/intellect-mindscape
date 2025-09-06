import React from 'react';
import { Navbar, Nav } from 'react-bootstrap';

interface AdminNavBarProps {
  onNavigate: (path: string) => void;
  isMainAdminPanel?: boolean;
}

const NavBar: React.FC<AdminNavBarProps> = ({ onNavigate, isMainAdminPanel }) => {
  return (
    <Navbar bg="light" expand="lg">
      <Navbar.Toggle aria-controls="basic-navbar-nav" />
      <Navbar.Collapse id="basic-navbar-nav">
        <Nav className="ml-auto justify-content-between w-100">
            {isMainAdminPanel ? (
            <>
              <Nav.Link onClick={() => onNavigate('/game')}>To Quiz</Nav.Link>
              <Nav.Link onClick={() => onNavigate('/login')}>Logout</Nav.Link>
            </>
          ) : (
            <>
              <Nav.Link onClick={() => onNavigate('/admin')}>Back</Nav.Link>
              <Nav.Link onClick={() => onNavigate('/game')}>To Quiz</Nav.Link>
              <Nav.Link onClick={() => onNavigate('/login')}>Logout</Nav.Link>
            </>
          )}
        </Nav>
      </Navbar.Collapse>
    </Navbar>
  );
};

export default NavBar;
