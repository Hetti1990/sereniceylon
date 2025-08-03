import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import App from './App';

// Mock the global fetch function
global.fetch = jest.fn(() =>
  Promise.resolve({
    ok: true,
    json: () => Promise.resolve({
      id: 1,
      country: 'Maldives',
      city: 'Malé',
      description: 'A tropical nation in the Indian Ocean.',
      currency_code: 'USD',
      hotels: [
        { id: 1, name: 'Maldives Resort', rate: 500.0, currency: 'USD' }
      ],
      sightseeing: [
        { id: 1, name: 'Scuba Diving', is_paid: true, cost: 150.0 },
        { id: 2, name: 'Beach lounging', is_paid: false, cost: null }
      ]
    }),
  })
) as jest.Mock;

test('renders destination details after fetching', async () => {
  render(<App />);

  // Check for loading state first
  expect(screen.getByText(/Loading destination.../i)).toBeInTheDocument();

  // Wait for the component to update with the fetched data
  const countryElement = await screen.findByText(/Maldives - Malé/i);
  expect(countryElement).toBeInTheDocument();

  // Check for hotels
  const hotelElement = await screen.findByText(/Maldives Resort - 500.00 USD/i);
  expect(hotelElement).toBeInTheDocument();

  // Check for paid sightseeing
  const paidSightElement = await screen.findByText(/Scuba Diving - 150.00 USD/i);
  expect(paidSightElement).toBeInTheDocument();

  // Check for free sightseeing
  const freeSightElement = await screen.findByText(/Beach lounging - Free/i);
  expect(freeSightElement).toBeInTheDocument();
});
