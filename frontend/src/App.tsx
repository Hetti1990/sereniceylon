import React, { useState, useEffect } from 'react';
import './App.css';

interface Hotel {
  id: number;
  name: string;
  rate: number;
  currency: string;
}

interface Sightseeing {
  id: number;
  name: string;
  is_paid: boolean;
  cost: number | null;
}

interface Destination {
  id: number;
  country: string;
  city: string;
  description: string;
  currency_code: string;
  hotels: Hotel[];
  sightseeing: Sightseeing[];
}

function App() {
  const [destination, setDestination] = useState<Destination | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // We'll run the backend server first, then the frontend.
    // The backend runs on port 5001.
    fetch('http://127.0.0.1:5001/destinations/1')
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => setDestination(data))
      .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
        setError('Failed to fetch destination data. Make sure the backend server is running.');
      });
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Travel Destinations</h1>
      </header>
      <main>
        {error && <p className="error">{error}</p>}
        {destination ? (
          <div>
            <h2>{destination.country} - {destination.city}</h2>
            <p>{destination.description}</p>
            <p><strong>Currency: {destination.currency_code}</strong></p>

            <h3>Hotels</h3>
            <ul>
              {destination.hotels.map(hotel => (
                <li key={hotel.id}>
                  {hotel.name} - {hotel.rate.toFixed(2)} {hotel.currency}
                </li>
              ))}
            </ul>

            <h3>Sightseeing</h3>
            <ul>
              {destination.sightseeing.map(sight => (
                <li key={sight.id}>
                  {sight.name} - {sight.is_paid ? `${sight.cost?.toFixed(2)} ${destination.currency_code}` : 'Free'}
                </li>
              ))}
            </ul>
          </div>
        ) : (
          !error && <p>Loading destination...</p>
        )}
      </main>
    </div>
  );
}

export default App;
