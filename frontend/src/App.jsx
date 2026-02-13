import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import Register from './pages/Register';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import DoctorDashboard from './pages/DoctorDashboard';
import Assessment from './pages/Assessment';
import './App.css';

function App() {
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [user, setUser] = useState(JSON.parse(localStorage.getItem('user') || 'null'));
  const [userType, setUserType] = useState(localStorage.getItem('userType'));

  useEffect(() => {
    if (token) {
      localStorage.setItem('token', token);
    } else {
      localStorage.removeItem('token');
    }
  }, [token]);

  useEffect(() => {
    if (user) {
      localStorage.setItem('user', JSON.stringify(user));
    } else {
      localStorage.removeItem('user');
    }
  }, [user]);

  useEffect(() => {
    if (userType) {
      localStorage.setItem('userType', userType);
    } else {
      localStorage.removeItem('userType');
    }
  }, [userType]);

  const handleLogin = (newToken, userData, type) => {
    setToken(newToken);
    setUser(userData);
    setUserType(type);
  };

  const handleLogout = () => {
    setToken(null);
    setUser(null);
    setUserType(null);
  };

  return (
    <Router>
      <div className="app">
        <Routes>
          <Route path="/register" element={<Register />} />
          <Route path="/login" element={<Login onLogin={handleLogin} />} />
          <Route 
            path="/dashboard" 
            element={
              token && userType === 'patient' ? 
                <Dashboard patient={user} token={token} onLogout={handleLogout} /> : 
                <Navigate to="/login" />
            } 
          />
          <Route 
            path="/doctor-dashboard" 
            element={
              token && userType === 'doctor' ? 
                <DoctorDashboard user={user} token={token} onLogout={handleLogout} /> : 
                <Navigate to="/login" />
            } 
          />
          <Route 
            path="/assessment" 
            element={
              token && userType === 'patient' ? 
                <Assessment patient={user} token={token} /> : 
                <Navigate to="/login" />
            } 
          />
          <Route 
            path="/" 
            element={
              <Navigate to={
                token ? (userType === 'doctor' ? "/doctor-dashboard" : "/dashboard") : "/login"
              } />
            } 
          />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
