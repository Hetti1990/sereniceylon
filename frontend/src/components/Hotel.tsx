import React, { useState, useEffect } from 'react';

const Hotel = () => {
    const [hotels, setHotels] = useState([]);
    const [name, setName] = useState('');
    const [location, setLocation] = useState('');
    const [mealBasis, setMealBasis] = useState('');
    const [roomBasis, setRoomBasis] = useState('');
    const [roomTypeValidity, setRoomTypeValidity] = useState('');
    const [rates, setRates] = useState([{ pax: 1, rate: 0 }]);

    useEffect(() => {
        fetchHotels();
    }, []);

    const fetchHotels = async () => {
        const response = await fetch('http://localhost:5000/hotels');
        const data = await response.json();
        setHotels(data);
    };

    const handleAddHotel = async () => {
        await fetch('http://localhost:5000/hotels', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name,
                location,
                meal_basis: mealBasis,
                room_basis: roomBasis,
                room_type_validity: roomTypeValidity,
                rates,
            }),
        });
        fetchHotels();
    };

    const handleRateChange = (index, field, value) => {
        const newRates = [...rates];
        newRates[index][field] = value;
        setRates(newRates);
    };

    const addRate = () => {
        setRates([...rates, { pax: 1, rate: 0 }]);
    };

    return (
        <div>
            <h1>Hotel Management</h1>
            <div>
                <h2>Add Hotel</h2>
                <input type="text" placeholder="Name" value={name} onChange={(e) => setName(e.target.value)} />
                <input type="text" placeholder="Location" value={location} onChange={(e) => setLocation(e.target.value)} />
                <input type="text" placeholder="Meal Basis" value={mealBasis} onChange={(e) => setMealBasis(e.target.value)} />
                <input type="text" placeholder="Room Basis" value={roomBasis} onChange={(e) => setRoomBasis(e.target.value)} />
                <input type="text" placeholder="Room Type Validity" value={roomTypeValidity} onChange={(e) => setRoomTypeValidity(e.target.value)} />
                <h3>Rates</h3>
                {rates.map((rate, index) => (
                    <div key={index}>
                        <input
                            type="number"
                            placeholder="Pax"
                            value={rate.pax}
                            onChange={(e) => handleRateChange(index, 'pax', parseInt(e.target.value))}
                        />
                        <input
                            type="number"
                            placeholder="Rate"
                            value={rate.rate}
                            onChange={(e) => handleRateChange(index, 'rate', parseFloat(e.target.value))}
                        />
                    </div>
                ))}
                <button onClick={addRate}>Add Rate</button>
                <button onClick={handleAddHotel}>Add Hotel</button>
            </div>
            <div>
                <h2>Hotels</h2>
                <ul>
                    {hotels.map((hotel) => (
                        <li key={hotel.id}>
                            {hotel.name} - {hotel.location}
                            <ul>
                                {hotel.rates.map((rate, index) => (
                                    <li key={index}>
                                        {rate.pax} Pax: {rate.rate}
                                    </li>
                                ))}
                            </ul>
                        </li>
                    ))}
                </ul>
            </div>
        </div>
    );
};

export default Hotel;
