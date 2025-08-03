import React, { useState, useEffect } from 'react';

// Hardcoded data for now. In a real app, this would be fetched from the API.
const destinations = [
    { id: 1, name: 'Colombo, Sri Lanka' },
    { id: 2, name: 'Bangkok, Thailand' },
];

const hotels = [
    { id: 1, name: 'Galle Face Hotel', destination_id: 1 },
    { id: 2, name: 'Mandarin Oriental', destination_id: 2 },
];

const transports = [
    { id: 1, name: 'Airport Transfer (Car)', destination_id: 1 },
    { id: 2, name: 'Tuk Tuk Ride', destination_id: 2 },
];

const sightseeingActivities = [
    { id: 1, name: 'Gangaramaya Temple', destination_id: 1, is_paid: true },
    { id: 2, name: 'Vimanmek Mansion', destination_id: 2, is_paid: true },
    { id: 3, name: 'Lumpini Park', destination_id: 2, is_paid: false },
];

const currencies = ['USD', 'LKR', 'THB'];

const PricingCalculator = () => {
    const [selectedDestination, setSelectedDestination] = useState(1);
    const [selectedHotels, setSelectedHotels] = useState<number[]>([]);
    const [selectedTransports, setSelectedTransports] = useState<number[]>([]);
    const [selectedSightseeing, setSelectedSightseeing] = useState<number[]>([]);
    const [pax, setPax] = useState(1);
    const [targetCurrency, setTargetCurrency] = useState('USD');
    const [totalCost, setTotalCost] = useState(null);
    const [error, setError] = useState('');

    const handleCalculateCost = async () => {
        setTotalCost(null);
        setError('');

        const itinerary_details = {
            hotels: selectedHotels.map(id => ({ id, nights: 1 })), // Assuming 1 night for simplicity
            transports: selectedTransports.map(id => ({ id })),
            sightseeing: selectedSightseeing.map(id => ({ id, pax, include_entrance_fee: true })),
            pax: pax,
        };

        try {
            const response = await fetch('http://127.0.0.1:5000/itinerary/calculate-cost', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    itinerary_details,
                    target_currency_code: targetCurrency,
                }),
            });

            const data = await response.json();

            if (response.ok) {
                setTotalCost(data.total_cost);
            } else {
                setError(data.error || 'An error occurred');
            }
        } catch (err) {
            setError('Failed to connect to the server.');
        }
    };

    return (
        <div>
            <h2>Pricing Calculator</h2>

            <div>
                <label>Destination: </label>
                <select value={selectedDestination} onChange={(e) => setSelectedDestination(parseInt(e.target.value))}>
                    {destinations.map(d => <option key={d.id} value={d.id}>{d.name}</option>)}
                </select>
            </div>

            <div>
                <label>Hotels: </label>
                {/* A real app would have a more sophisticated multi-select component */}
                <select multiple onChange={(e) => setSelectedHotels(Array.from(e.target.selectedOptions, option => parseInt(option.value)))}>
                    {hotels.filter(h => h.destination_id === selectedDestination).map(h => <option key={h.id} value={h.id}>{h.name}</option>)}
                </select>
            </div>

            <div>
                <label>Transport: </label>
                <select multiple onChange={(e) => setSelectedTransports(Array.from(e.target.selectedOptions, option => parseInt(option.value)))}>
                    {transports.filter(t => t.destination_id === selectedDestination).map(t => <option key={t.id} value={t.id}>{t.name}</option>)}
                </select>
            </div>

            <div>
                <label>Sightseeing: </label>
                <select multiple onChange={(e) => setSelectedSightseeing(Array.from(e.target.selectedOptions, option => parseInt(option.value)))}>
                    {sightseeingActivities.filter(s => s.destination_id === selectedDestination).map(s => <option key={s.id} value={s.id}>{s.name} {s.is_paid ? '(Paid)' : '(Free)'}</option>)}
                </select>
            </div>

            <div>
                <label>Number of People (Pax): </label>
                <input type="number" value={pax} onChange={(e) => setPax(parseInt(e.target.value))} min="1" />
            </div>

            <div>
                <label>Currency: </label>
                <select value={targetCurrency} onChange={(e) => setTargetCurrency(e.target.value)}>
                    {currencies.map(c => <option key={c} value={c}>{c}</option>)}
                </select>
            </div>

            <button onClick={handleCalculateCost}>Calculate Cost</button>

            {totalCost !== null && (
                <div>
                    <h3>Total Cost: {totalCost} {targetCurrency}</h3>
                </div>
            )}

            {error && <p style={{ color: 'red' }}>{error}</p>}
        </div>
    );
};

export default PricingCalculator;
