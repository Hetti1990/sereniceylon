import React from 'react';
import { render, screen } from '@testing-library/react';
import App from './App';

test('renders itinerary management heading', () => {
  render(<App />);
  const headingElement = screen.getByText(/itinerary management/i);
  expect(headingElement).toBeInTheDocument();
});
