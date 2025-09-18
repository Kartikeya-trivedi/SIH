import React from 'react';
import './Navbar.css';

const Navbar = () => {
  return (
    <nav className="navbar-container">
      <ul className="navbar-links">
        <li><a href="#home" className="nav-link active">Home</a></li>
        <li><a href="#about" className="nav-link">About Us</a></li>
        <li><a href="#contact" className="nav-link">Contact</a></li>
        <li><a href="#community" className="nav-link">Community</a></li>
      </ul>
    </nav>
  );
};

export default Navbar;