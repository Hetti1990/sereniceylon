import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface Day {
  id: number;
  day_number: number;
  description: string;
}

interface Activity {
  id: number;
  sight_id: number | null;
  hotel_id: number | null;
  transport_id: number | null;
  entrance_fee: number | null;
  pax: number | null;
}

interface DayProps {
  day: Day;
  onDelete: (id: number) => void;
}

const DayComponent: React.FC<DayProps> = ({ day, onDelete }) => {
  const [activities, setActivities] = useState<Activity[]>([]);
  const [description, setDescription] = useState(day.description);

  useEffect(() => {
    // Fetch activities for the day from the backend
    axios.get(`http://localhost:5000/days/${day.id}/activities`)
      .then(response => {
        setActivities(response.data);
      })
      .catch(error => {
        console.error('Error fetching activities:', error);
      });
  }, [day.id]);

  const handleUpdateDescription = () => {
    // Update the day's description
    axios.put(`http://localhost:5000/itineraries/1/days/${day.id}`, { description })
      .catch(error => {
        console.error('Error updating description:', error);
      });
  };

  const handleAddActivity = () => {
    // Add a new activity to the day
    axios.post(`http://localhost:5000/days/${day.id}/activities`, {})
      .then(response => {
        setActivities([...activities, response.data]);
      })
      .catch(error => {
        console.error('Error adding activity:', error);
      });
  };

  const handleDeleteActivity = (id: number) => {
    // Delete an activity from the day
    axios.delete(`http://localhost:5000/days/${day.id}/activities/${id}`)
      .then(() => {
        setActivities(activities.filter(activity => activity.id !== id));
      })
      .catch(error => {
        console.error('Error deleting activity:', error);
      });
  };

  return (
    <div>
      <h2>Day {day.day_number}</h2>
      <input
        type="text"
        value={description}
        onChange={e => setDescription(e.target.value)}
        onBlur={handleUpdateDescription}
      />
      <button onClick={() => onDelete(day.id)}>Delete Day</button>
      <button onClick={handleAddActivity}>Add Activity</button>
      <ul>
        {activities.map(activity => (
          <li key={activity.id}>
            <p>Sight ID: {activity.sight_id}</p>
            <p>Hotel ID: {activity.hotel_id}</p>
            <p>Transport ID: {activity.transport_id}</p>
            <p>Entrance Fee: {activity.entrance_fee}</p>
            <p>Pax: {activity.pax}</p>
            <button onClick={() => handleDeleteActivity(activity.id)}>Delete Activity</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default DayComponent;
