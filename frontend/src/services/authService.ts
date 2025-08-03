import axios from 'axios';

const API_URL = 'http://localhost:5000/auth/';

const register = (name: string, email: string, password: string) => {
    return axios.post(API_URL + 'register', {
        name,
        email,
        password,
    });
};

const login = (email: string, password: string) => {
    return axios.post(API_URL + 'login', {
        email,
        password,
    }).then(response => {
        if (response.data.access_token) {
            localStorage.setItem('user', JSON.stringify(response.data));
        }
        return response.data;
    });
};

const logout = () => {
    localStorage.removeItem('user');
};

const getCurrentUser = () => {
    const userStr = localStorage.getItem('user');
    if (userStr) {
        return JSON.parse(userStr);
    }
    return null;
};

const authService = {
    register,
    login,
    logout,
    getCurrentUser,
};

export default authService;
