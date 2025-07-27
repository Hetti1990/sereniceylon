import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Day from './Day';

interface Itinerary {
  id: number;
  user_id: number;
  destination_id: number;
  start_date: string;
  end_date: string;
  total_cost: number;
}

const ItineraryComponent: React.FC = () => {
  const [itinerary, setItinerary] = useState<Itinerary | null>(null);
  const [days, setDays] = useState<any[]>([]);

  useEffect(() => {
    // Fetch itinerary data from the backend
    axios.get('http://localhost:5000/itineraries/1')
      .then(response => {
        setItinerary(response.data);
        return axios.get(`http://localhost:5000/itineraries/${response.data.id}/days`);
      })
      .then(response => {
        setDays(response.data);
      })
      .catch(error => {
        console.error('Error fetching data:', error);
      });
  }, []);

  const handleAddDay = () => {
    // Add a new day to the itinerary
    axios.post(`http://localhost:5000/itineraries/${itinerary?.id}/days`, {
      day_number: days.length + 1,
      description: 'New day',
    })
      .then(response => {
        setDays([...days, response.data]);
      })
      .catch(error => {
        console.error('Error adding day:', error);
      });
  };

  const handleDeleteDay = (id: number) => {
    // Delete a day from the itinerary
    axios.delete(`http://localhost:5000/itineraries/${itinerary?.id}/days/${id}`)
      .then(() => {
        setDays(days.filter(day => day.id !== id));
      })
      .catch(error => {
        console.error('Error deleting day:', error);
      });
  };

  if (!itinerary) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h1>Itinerary</h1>
      <p>Start Date: {itinerary.start_date}</p>
      <p>End Date: {itinerary.end_date}</p>
      <p>Total Cost: {itinerary.total_cost}</p>
      <button onClick={handleAddDay}>Add Day</button>
      {days.map(day => (
        <Day key={day.id} day={day} onDelete={handleDeleteDay} />
      ))}
    </div>
  );
};

export default ItineraryComponent;
