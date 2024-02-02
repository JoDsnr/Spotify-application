import React from 'react';
import './renderTimelineCards.css';


const RenderTimelineCards = ({ apiData }) => {
    return apiData.most_listened_artists_by_month.map((artist, index) => (
      <div key={index} className="timeline-card">
        <img className="artist-image" src={artist.artist_image_url} alt={artist.artistName} />
        <div className="artist-info">
          <p className="year-month">{artist.year_month}</p>
          <p className="monthartist-name">{artist.artistName}</p>
        </div>
      </div>
    ));
  };
  
  export default RenderTimelineCards;