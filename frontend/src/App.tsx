import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Link, useNavigate } from 'react-router-dom';
import Home from './components/Home';
import Login from './components/Login';
import Register from './components/Register';
import Profile from './components/Profile';
import AdminDashboard from './components/AdminDashboard';
import PrivateRoute from './components/PrivateRoute';
import authService from './services/authService';
import './App.css';

const App: React.FC = () => {
    const [currentUser, setCurrentUser] = useState<any>(undefined);

    useEffect(() => {
        const user = authService.getCurrentUser();
        if (user) {
            setCurrentUser(user);
        }
    }, []);

    const logOut = () => {
        authService.logout();
        setCurrentUser(undefined);
    };

    return (
        <Router>
            <div>
                <nav>
                    <ul>
                        <li>
                            <Link to="/">Home</Link>
                        </li>
                        {currentUser ? (
                            <>
                                <li>
                                    <Link to="/profile">Profile</Link>
                                </li>
                                {currentUser.role === 'Admin' && (
                                    <li>
                                        <Link to="/admin">Admin</Link>
                                    </li>
                                )}
                                <li>
                                    <a href="/login" onClick={logOut}>
                                        Logout
                                    </a>
                                </li>
                            </>
                        ) : (
                            <>
                                <li>
                                    <Link to="/login">Login</Link>
                                </li>
                                <li>
                                    <Link to="/register">Register</Link>
                                </li>
                            </>
                        )}
                    </ul>
                </nav>

                <hr />

                <Routes>
                    <Route path="/" element={<Home />} />
                    <Route path="/login" element={<Login />} />
                    <Route path="/register" element={<Register />} />
                    <Route element={<PrivateRoute />}>
                        <Route path="/profile" element={<Profile />} />
                        <Route path="/admin" element={<AdminDashboard />} />
                    </Route>
                </Routes>
            </div>
        </Router>
    );
};

export default App;
