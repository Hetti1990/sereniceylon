import React, { useState, useEffect } from 'react';
import userService from '../services/userService';

interface User {
    id: number;
    name: string;
    email: string;
    role: string;
}

const AdminDashboard: React.FC = () => {
    const [users, setUsers] = useState<User[]>([]);
    const [message, setMessage] = useState('');

    useEffect(() => {
        fetchUsers();
    }, []);

    const fetchUsers = async () => {
        try {
            const response = await userService.getUsers();
            setUsers(response.data);
        } catch (error) {
            setMessage('Could not fetch users');
        }
    };

    const handleDeleteUser = async (id: number) => {
        try {
            await userService.deleteUser(id);
            fetchUsers(); // Refresh the list
        } catch (error) {
            setMessage('Could not delete user');
        }
    };

    // A simple edit prompt. In a real app, this would be a modal or a separate page.
    const handleEditUser = async (user: User) => {
        const newName = prompt("Enter new name:", user.name);
        const newRole = prompt("Enter new role (Admin, Agent, Customer):", user.role);
        if (newName && newRole) {
            try {
                await userService.updateUser(user.id, { name: newName, role: newRole });
                fetchUsers(); // Refresh the list
            } catch (error) {
                setMessage('Could not update user');
            }
        }
    };

    return (
        <div>
            <h1>Admin Dashboard</h1>
            {message && <p>{message}</p>}
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Email</th>
                        <th>Role</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {users.map(user => (
                        <tr key={user.id}>
                            <td>{user.id}</td>
                            <td>{user.name}</td>
                            <td>{user.email}</td>
                            <td>{user.role}</td>
                            <td>
                                <button onClick={() => handleEditUser(user)}>Edit</button>
                                <button onClick={() => handleDeleteUser(user.id)}>Delete</button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default AdminDashboard;
