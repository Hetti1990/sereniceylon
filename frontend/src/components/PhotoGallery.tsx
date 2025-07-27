import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Photo from './Photo';

const PhotoGallery: React.FC = () => {
    const [photos, setPhotos] = useState<any[]>([]);

    useEffect(() => {
        axios.get('http://localhost:5000/api/photos')
            .then(response => {
                setPhotos(response.data);
            })
            .catch(error => {
                console.error('Error fetching photos:', error);
            });
    }, []);

    return (
        <div>
            <h2>Photo Gallery</h2>
            <div className="photo-grid">
                {photos.map(photo => (
                    <Photo key={photo.id} photo={photo} />
                ))}
            </div>
        </div>
    );
};

export default PhotoGallery;
