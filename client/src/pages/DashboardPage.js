
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Slider from 'react-slick';
import 'slick-carousel/slick/slick.css';
import 'slick-carousel/slick/slick-theme.css';
import './Dashboard.css';
import LogoutButton from './elements/LogoutButton';

function App() {
  const [apiData, setApiData] = useState({ top_artists: [], recently_played: [], most_listened_albums: [] });


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

  const renderCarouselItems = () => {
    return apiData.most_listened_albums.map(album => (
      <div key={album.album_name}>
        <img src={album.image} alt={album.album_name} />
      </div>
    ));
  };

  const settings = {
    dots: false,
    infinite: true,
    autoplay: true,
    autoplaySpeed: 0,
    speed:2000,
    slidesToShow: 7,
    slidesToScroll: 1,
    arrows: false,
  };

  
  return (
    <div className="App">
      <div className="left-sidebar">
        <div className='sidebarheader-content'>Home</div>
        <div className='sidebarheader-content'>Recently Played</div>
        <div className='recently-played'>
            {apiData.recently_played.map(song => (
            <div className="recently-played-card" key={song.song_name}>
              {song.image && <img src={song.image} alt={song.song_name} />}
              <div className="recently-played-card-info">
                <p className="song-name">{song.song_name}</p>
                <p className="artist-name">{song.artist_name}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
        <div className="main-content">
          <div className="header-section">
              <LogoutButton onLogout={handleLogout} />
          </div>
          <div className='carousel-container'>
            <Slider {...settings}>
              {renderCarouselItems()}
            </Slider>
          </div>
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
        </div>
      </div>
  );
}

export default App;