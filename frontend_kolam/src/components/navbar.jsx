import React from 'react';
import { NavLink } from 'react-router-dom';
import './navbar.css';

const Navbar = () => {
  return (
    <nav className="navbar-container">
      <ul className="navbar-links">
        <li><NavLink to="/home" className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}>Home</NavLink></li>
        <li><NavLink to="/knowledge" className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}>Knowledge</NavLink></li>
        <li><NavLink to="/recognize" className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}>Recognize</NavLink></li>
        <li><NavLink to="/recreate" className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}>Recreate</NavLink></li>
      </ul>
    </nav>
  );
};

export default Navbar;