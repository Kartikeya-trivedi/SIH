import React from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css';

const Navbar = ({ currentRoute }) => {
  return (
    <nav className="navbar-container">
      <ul className="navbar-links">
        <li>
          <Link
            to="/"
            className={`nav-link ${currentRoute === '/' ? 'active' : ''}`}
          >
            Home
          </Link>
        </li>
        <li>
          <Link
            to="/knowledge"
            className={`nav-link ${currentRoute === '/knowledge' ? 'active' : ''}`}
          >
            Knowledge
          </Link>
        </li>
        <li>
          <Link
            to="/recognize"
            className={`nav-link ${currentRoute === '/recognize' ? 'active' : ''}`}
          >
            Recognize
          </Link>
        </li>
        <li>
          <Link
            to="/recreate"
            className={`nav-link ${currentRoute === '/recreate' ? 'active' : ''}`}
          >
            Recreate
          </Link>
        </li>
      </ul>
    </nav>
  );
};

export default Navbar;

