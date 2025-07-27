import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
    const [locations, setLocations] = useState([]);
    const [sightseeing, setSightseeing] = useState([]);
    const [form, setForm] = useState({ city: '', country: '' });
    const [sightseeingForm, setSightseeingForm] = useState({ location_id: '', name: '', description: '', category: '' });

    useEffect(() => {
        fetchLocations();
        fetchSightseeing();
    }, []);

    const fetchLocations = async () => {
        const response = await fetch('http://localhost:5000/locations');
        const data = await response.json();
        setLocations(data);
    };

    const fetchSightseeing = async () => {
        const response = await fetch('http://localhost:5000/sightseeing');
        const data = await response.json();
        setSightseeing(data);
    };

    const handleFormChange = (e) => {
        setForm({ ...form, [e.target.name]: e.target.value });
    };

    const handleSightseeingFormChange = (e) => {
        setSightseeingForm({ ...sightseeingForm, [e.target.name]: e.target.value });
    };

    const addLocation = async (e) => {
        e.preventDefault();
        await fetch('http://localhost:5000/locations', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(form),
        });
        fetchLocations();
    };

    const addSightseeing = async (e) => {
        e.preventDefault();
        await fetch('http://localhost:5000/sightseeing', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(sightseeingForm),
        });
        fetchSightseeing();
    };

    const deleteLocation = async (id) => {
        await fetch(`http://localhost:5000/locations/${id}`, { method: 'DELETE' });
        fetchLocations();
    };

    const deleteSightseeing = async (id) => {
        await fetch(`http://localhost:5000/sightseeing/${id}`, { method: 'DELETE' });
        fetchSightseeing();
    };

    return (
        <div className="App">
            <h1>Locations</h1>
            <form onSubmit={addLocation}>
                <input name="city" placeholder="City" onChange={handleFormChange} />
                <input name="country" placeholder="Country" onChange={handleFormChange} />
                <button type="submit">Add Location</button>
            </form>
            <ul>
                {locations.map((loc) => (
                    <li key={loc.id}>
                        {loc.city}, {loc.country}
                        <button onClick={() => deleteLocation(loc.id)}>Delete</button>
                    </li>
                ))}
            </ul>

            <h1>Sightseeing</h1>
            <form onSubmit={addSightseeing}>
                <select name="location_id" onChange={handleSightseeingFormChange}>
                    <option value="">Select Location</option>
                    {locations.map((loc) => (
                        <option key={loc.id} value={loc.id}>{loc.city}</option>
                    ))}
                </select>
                <input name="name" placeholder="Name" onChange={handleSightseeingFormChange} />
                <input name="description" placeholder="Description" onChange={handleSightseeingFormChange} />
                <input name="category" placeholder="Category" onChange={handleSightseeingFormChange} />
                <button type="submit">Add Sightseeing</button>
            </form>
            <ul>
                {sightseeing.map((s) => (
                    <li key={s.id}>
                        {s.name} ({s.category})
                        <button onClick={() => deleteSightseeing(s.id)}>Delete</button>
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default App;
