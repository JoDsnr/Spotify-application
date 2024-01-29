
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Dashboard.css';

function App() {
  const [apiData, setApiData] = useState([]);

  useEffect(() => {
    // Make a GET request to your Flask API endpoint
    axios.get('/dashboard', { maxRedirects: 5 })
      .then(response => {
      // Log the received data to the console
      console.log('Data from Flask API:', response.data);
        // Handle the API response and update state
        setApiData(response.data.top_artists); // Adjust this based on your API response structure
      })
      .catch(error => {
        console.error('Error fetching data from API:', error);
      });
  }, []); // Empty dependency array to run the effect only once on component mount

  return (
    <div className="App">
      <div className="left-sidebar">
        {/* Add your content for the left sidebar here */}
        <p>Left Sidebar Content</p>
        {/* Add any additional components or links for the left sidebar */}
      </div>
      <div className="main-content">
        <header className="App-header">
          <p>
            Data from Flask API:
          </p>
          <ul>
            {apiData.map(item => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </header>
      </div>
    </div>
  );
}

export default App;