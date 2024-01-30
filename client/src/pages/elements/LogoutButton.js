// LogoutButton.js

import React, { useState } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faUser, faSignOutAlt } from '@fortawesome/free-solid-svg-icons';

import './LogoutButton.css';

function LogoutButton({ onLogout, userEmail }) {
  const [showDropdown, setShowDropdown] = useState(false);

  const handleButtonClick = () => {
    setShowDropdown(!showDropdown);
  };

  const handleLogout = () => {
    onLogout();
    setShowDropdown(false);
  };

  return (
    <div className="logout-button-container">
      <button className="user-button" onClick={handleButtonClick}>
        <FontAwesomeIcon icon={faUser} />
      </button>
      {showDropdown && (
        <div className="dropdown">
          <p className="user-email">{userEmail}</p>
          <button onClick={handleLogout}>
            <FontAwesomeIcon icon={faSignOutAlt} />
            Logout
          </button>
        </div>
      )}
    </div>
  );
}

export default LogoutButton;
