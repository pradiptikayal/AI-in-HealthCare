import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import Register from './pages/Register';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Assessment from './pages/Assessment';
import './App.css';

function App() {
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [patient, setPatient] = useState(JSON.parse(localStorage.getItem('patient') || 'null'));

  useEffect(() => {
    if (token) {
      localStorage.setItem('token', token);
    } else {
      localStorage.removeItem('token');
    }
  }, [token]);

  useEffect(() => {
    if (patient) {
      localStorage.setItem('patient', JSON.stringify(patient));
    } else {
      localStorage.removeItem('patient');
    }
  }, [patient]);

  const handleLogin = (newToken, patientData) => {
    setToken(newToken);
    setPatient(patientData);
  };

  const handleLogout = () => {
    setToken(null);
    setPatient(null);
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
              token ? <Dashboard patient={patient} token={token} onLogout={handleLogout} /> : <Navigate to="/login" />
            } 
          />
          <Route 
            path="/assessment" 
            element={
              token ? <Assessment patient={patient} token={token} /> : <Navigate to="/login" />
            } 
          />
          <Route path="/" element={<Navigate to={token ? "/dashboard" : "/login"} />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
