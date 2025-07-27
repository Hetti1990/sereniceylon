import React, { useState, useEffect } from 'react';

const Itinerary = () => {
  const [itineraries, setItineraries] = useState([]);
  const [excludeReligious, setExcludeReligious] = useState(false);
  const [newItinerary, setNewItinerary] = useState({
    title: '',
    description: '',
    duration_days: 0,
    destinations: [],
    activities: [],
    accommodations: [],
    meals: [],
    is_group_package: false,
  });

  useEffect(() => {
    fetch('http://localhost:5000/itineraries')
      .then(response => response.json())
      .then(data => setItineraries(data))
      .catch(error => console.error('Error fetching itineraries:', error));
  }, []);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setNewItinerary({ ...newItinerary, [name]: value });
  };

  const handleFormSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    fetch('http://localhost:5000/itineraries', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(newItinerary),
    })
      .then(response => response.json())
      .then(data => {
        console.log(data);
        // Refresh itineraries
        fetch('http://localhost:5000/itineraries')
          .then(response => response.json())
          .then(data => setItineraries(data));
      })
      .catch(error => console.error('Error creating itinerary:', error));
  };

  return (
    <div>
      <h1>Itinerary Management</h1>
      <form onSubmit={handleFormSubmit}>
        <input name="title" placeholder="Title" onChange={handleInputChange} />
        <textarea name="description" placeholder="Description" onChange={handleInputChange}></textarea>
        <input name="duration_days" type="number" placeholder="Duration (days)" onChange={handleInputChange} />
        <button type="submit">Create Itinerary</button>
      </form>

      <hr />

      <div>
        <label>
          <input type="checkbox" onChange={e => setExcludeReligious(e.target.checked)} />
          Exclude religious sites
        </label>
      </div>

      {itineraries
        .filter(itinerary => {
          if (!excludeReligious) {
            return true;
          }
          const religiousActivities = itinerary.activities.filter(activity =>
            activity.description.toLowerCase().includes('temple') ||
            activity.description.toLowerCase().includes('church')
          );
          return religiousActivities.length === 0;
        })
        .map(itinerary => (
          <div key={itinerary.id}>
            <h2>{itinerary.title}</h2>
            <p>{itinerary.description}</p>
            <p>Duration: {itinerary.duration_days} days</p>
            {/* Further details here */}
          </div>
        ))}
    </div>
  );
};

export default Itinerary;
