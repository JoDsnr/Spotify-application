// LogoutButton.js

import React, { useState, useEffect } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faUser, faSignOutAlt } from '@fortawesome/free-solid-svg-icons';
import httpClient from '../../httpClient';

import './LogoutButton.css';

function LogoutButton() {
  const [showDropdown, setShowDropdown] = useState(false);
  const [user, setUser] = useState(null);

  useEffect(() => {
    (async () => {
      try {
        const resp = await httpClient.get('//localhost:5000/@me');
        setUser(resp.data);
      } catch (error) {
        console.log('Not authenticated');
      }
    })();
  }, []);

  const handleButtonClick = () => {
    setShowDropdown(!showDropdown);
  };

  const handleLogout = async () => {
    await httpClient.post('//localhost:5000/logout');
    window.location.href = '/';
  };


  return (
    <div className="logout-button-container">
      <button className="user-button" onClick={handleButtonClick}>
        <FontAwesomeIcon icon={faUser} />
      </button>
      {showDropdown && (
        <div className="dropdown">
          <p className="user-email">User : {user.email}</p>
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
