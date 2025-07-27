import React from 'react';

interface PhotoProps {
    photo: {
        id: number;
        image_url: string;
        description: string;
        category: string;
    };
}

const Photo: React.FC<PhotoProps> = ({ photo }) => {
    return (
        <div className="photo-item">
            <img src={`http://localhost:5000/${photo.image_url}`} alt={photo.description} />
            <p>{photo.description}</p>
            <p>Category: {photo.category}</p>
            <input type="checkbox" />
        </div>
    );
};

export default Photo;
