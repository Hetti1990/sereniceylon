import axios from 'axios';
import authService from './authService';

const API_URL = 'http://localhost:5000/admin/';

const getAuthHeader = () => {
    const user = authService.getCurrentUser();
    if (user && user.access_token) {
        return { Authorization: 'Bearer ' + user.access_token };
    } else {
        return {};
    }
};

const getUsers = () => {
    return axios.get(API_URL + 'users', { headers: getAuthHeader() });
};

const getUser = (id: number) => {
    return axios.get(API_URL + `users/${id}`, { headers: getAuthHeader() });
};

const updateUser = (id: number, data: any) => {
    return axios.put(API_URL + `users/${id}`, data, { headers: getAuthHeader() });
};

const deleteUser = (id: number) => {
    return axios.delete(API_URL + `users/${id}`, { headers: getAuthHeader() });
};

const userService = {
    getUsers,
    getUser,
    updateUser,
    deleteUser,
};

export default userService;
