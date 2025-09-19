import React from 'react';
import './Navbar.css';

const Navbar = ({ onNavigate, currentRoute }) => {
  // Helper function to prevent default link behavior and navigate
  const handleNavClick = (e, path) => {
    e.preventDefault();
    onNavigate(path);
  };

  return (
    <nav className="navbar-container">
      <ul className="navbar-links">
        <li>
          <a
            href="/"
            onClick={(e) => handleNavClick(e, '/')}
            className={`nav-link ${currentRoute === '/' ? 'active' : ''}`}
          >
            Home
          </a>
        </li>
        <li>
          <a
            href="/knowledge"
            onClick={(e) => handleNavClick(e, '/knowledge')}
            className={`nav-link ${currentRoute === '/knowledge' ? 'active' : ''}`}
          >
            Knowledge
          </a>
        </li>
        <li>
          <a
            href="/recognize"
            onClick={(e) => handleNavClick(e, '/recognize')}
            className={`nav-link ${currentRoute === '/recognize' ? 'active' : ''}`}
          >
            Recognize
          </a>
        </li>
        <li>
          <a
            href="/recreate"
            onClick={(e) => handleNavClick(e, '/recreate')}
            className={`nav-link ${currentRoute === '/recreate' ? 'active' : ''}`}
          >
            Recreate
          </a>
        </li>
      </ul>
    </nav>
  );
};

export default Navbar;

