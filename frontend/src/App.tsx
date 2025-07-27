import React from 'react';
import './App.css';
import PhotoGallery from './components/PhotoGallery';
import PhotoUpload from './components/PhotoUpload';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Travel Agency Photo Gallery</h1>
      </header>
      <main>
        <PhotoUpload />
        <PhotoGallery />
      </main>
    </div>
  );
}

export default App;
