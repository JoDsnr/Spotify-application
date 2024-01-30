
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Dashboard.css';
import LogoutButton from './elements/LogoutButton';

function App() {
  const [apiData, setApiData] = useState({ top_artists: [], recently_played: [] });


  useEffect(() => {
    // Make a GET request to your Flask API endpoint
    axios.get('/dashboard', { maxRedirects: 5 })
      .then(response => {
      // Log the received data to the console
      console.log('Data from Flask API:', response.data);
        // Handle the API response and update state
        setApiData(response.data); // Adjust this based on your API response structure
      })
      .catch(error => {
        console.error('Error fetching data from API:', error);
      });
  }, []); // Empty dependency array to run the effect only once on component mount



  const handleLogout = () => {
    // Implement logout logic here
    // For example, you can redirect the user to the logout endpoint
    window.location.href = '/';
  };

  
  return (
    <div className="App">
      <div className="left-sidebar">
      <div className='sidebarheader-content'>Recently Played</div>
        {apiData.recently_played.map(album => (
          <div className="recently-played-card" key={album.album_name}>
            {album.image && <img src={album.image} alt={album.album_name} />}
            <div className="recently-played-card-info">
              <p className="album-name">{album.album_name}</p>
              <p className="artist-name">{album.artist_name}</p>
            </div>
          </div>
        ))}
      </div>
      <div className="main-content">
        <div className="header-section">
            <LogoutButton onLogout={handleLogout} />
        </div>
        <header className="App-header">
          <div className='banner-content'>
            Your favorite artists
          </div>
          <div className="artist-cards">
            {apiData.top_artists.map(artist => (
              <div className="artist-card" key={artist.name}>
                {artist.image && <img src={artist.image} alt={artist.name} />}
                <p>{artist.name}</p>
              </div>
            ))}
          </div>
        </header>
      </div>
    </div>
  );
}

export default App;