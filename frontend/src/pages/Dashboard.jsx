import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

function Dashboard({ patient, token, onLogout }) {
  const navigate = useNavigate();
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      const response = await axios.get(`/api/patients/${patient.patientID}/history`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setHistory(response.data.history);
    } catch (err) {
      setError('Failed to load history');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    onLogout();
    navigate('/login');
  };

  return (
    <div className="page-container">
      <div className="dashboard">
        <div className="dashboard-header">
          <div>
            <h1>Welcome, {patient.firstName} {patient.lastName}</h1>
            <p className="subtitle">Patient ID: {patient.patientID}</p>
          </div>
          <button onClick={handleLogout} className="btn-secondary">Logout</button>
        </div>

        <div className="action-section">
          <button onClick={() => navigate('/assessment')} className="btn-primary btn-large">
            Start New Assessment
          </button>
        </div>

        <div className="history-section">
          <h2>Your Assessment History</h2>
          
          {loading && <p>Loading history...</p>}
          {error && <div className="error-message">{error}</div>}
          
          {!loading && history.length === 0 && (
            <p className="empty-message">No assessments yet. Start your first assessment above!</p>
          )}

          {history.map((item) => (
            <div key={item.assessmentID} className="history-card">
              <div className="history-header">
                <h3>{new Date(item.assessmentDate).toLocaleDateString()}</h3>
                <span className="history-time">{new Date(item.assessmentDate).toLocaleTimeString()}</span>
              </div>
              
              <div className="history-details">
                <p><strong>Symptoms:</strong> {item.symptoms.join(', ')}</p>
                <p><strong>Weight:</strong> {item.weight} {item.weightUnit}</p>
                <p><strong>Height:</strong> {item.height} {item.heightUnit}</p>
                <p><strong>Age:</strong> {item.age}</p>
              </div>

              {item.prescription && (
                <div className="prescription-section">
                  <h4>Prescription</h4>
                  {item.prescription.medications.map((med, idx) => (
                    <div key={idx} className="medication">
                      <p><strong>{med.name}</strong></p>
                      <p>Dosage: {med.dosage} | Frequency: {med.frequency} | Duration: {med.duration}</p>
                    </div>
                  ))}
                  <p className="instructions">{item.prescription.instructions}</p>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
