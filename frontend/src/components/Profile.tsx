import React, { useState, useEffect } from 'react';
import authService from '../services/authService';
import axios from 'axios';

const API_URL = 'http://localhost:5000/auth/';

const Profile: React.FC = () => {
    const [user, setUser] = useState<any>(null);
    const [name, setName] = useState('');
    const [message, setMessage] = useState('');

    useEffect(() => {
        const currentUser = authService.getCurrentUser();
        if (currentUser && currentUser.access_token) {
            axios.get(API_URL + 'profile', {
                headers: {
                    Authorization: 'Bearer ' + currentUser.access_token
                }
            }).then(response => {
                setUser(response.data);
                setName(response.data.name);
            }).catch(error => {
                setMessage("Could not fetch profile");
            });
        }
    }, []);

    const handleUpdateProfile = async (e: React.FormEvent) => {
        e.preventDefault();
        setMessage('');
        try {
            const currentUser = authService.getCurrentUser();
            if (currentUser && currentUser.access_token) {
                await axios.put(API_URL + 'profile', { name }, {
                    headers: {
                        Authorization: 'Bearer ' + currentUser.access_token
                    }
                });
                setMessage('Profile updated successfully');
            }
        } catch (error: any) {
            setMessage('Could not update profile');
        }
    };

    if (!user) {
        return <div>Loading...</div>;
    }

    return (
        <div>
            <h1>Profile</h1>
            <p><strong>Email:</strong> {user.email}</p>
            <p><strong>Role:</strong> {user.role}</p>
            <form onSubmit={handleUpdateProfile}>
                <div>
                    <label htmlFor="name">Name</label>
                    <input
                        type="text"
                        id="name"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                        required
                    />
                </div>
                <button type="submit">Update Profile</button>
            </form>
            {message && <p>{message}</p>}
        </div>
    );
};

export default Profile;
