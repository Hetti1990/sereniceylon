import React from 'react';
import { render, screen } from '@testing-library/react';
import App from './App';

test('renders photo gallery and upload components', () => {
  render(<App />);
  const galleryElement = screen.getByText(/Photo Gallery/i);
  const uploadElement = screen.getByText(/Upload Photo/i);
  expect(galleryElement).toBeInTheDocument();
  expect(uploadElement).toBeInTheDocument();
});
