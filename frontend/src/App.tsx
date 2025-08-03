import React from 'react';
import './App.css';
import PricingCalculator from './PricingCalculator';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Travel Itinerary Pricer</h1>
      </header>
      <main>
        <PricingCalculator />
      </main>
    </div>
  );
}

export default App;
