import React, { useState } from 'react';
import axios from 'axios';

const PhotoUpload: React.FC = () => {
    const [file, setFile] = useState<File | null>(null);
    const [description, setDescription] = useState('');
    const [category, setCategory] = useState('');

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files) {
            setFile(e.target.files[0]);
        }
    };

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (!file) {
            return;
        }
        const formData = new FormData();
        formData.append('file', file);
        formData.append('description', description);
        formData.append('category', category);

        axios.post('http://localhost:5000/api/photos', formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        })
        .then(response => {
            console.log('Photo uploaded:', response.data);
            // Optionally, refresh the photo gallery
        })
        .catch(error => {
            console.error('Error uploading photo:', error);
        });
    };

    return (
        <div>
            <h2>Upload Photo</h2>
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Photo:</label>
                    <input type="file" onChange={handleFileChange} />
                </div>
                <div>
                    <label>Description:</label>
                    <input type="text" value={description} onChange={e => setDescription(e.target.value)} />
                </div>
                <div>
                    <label>Category:</label>
                    <input type="text" value={category} onChange={e => setCategory(e.target.value)} />
                </div>
                <button type="submit">Upload</button>
            </form>
        </div>
    );
};

export default PhotoUpload;
