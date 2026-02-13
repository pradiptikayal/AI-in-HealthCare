import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

function DoctorDashboard({ user, token, onLogout }) {
  const navigate = useNavigate();
  const [patients, setPatients] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [selectedPatient, setSelectedPatient] = useState(null);
  const [editingPrescription, setEditingPrescription] = useState(null);

  useEffect(() => {
    fetchPatients();
  }, []);

  const fetchPatients = async () => {
    try {
      const response = await axios.get('/api/doctors/patients', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setPatients(response.data.patients);
    } catch (err) {
      setError('Failed to load patients');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    onLogout();
    navigate('/login');
  };

  const handleEditPrescription = (prescription) => {
    setEditingPrescription({
      ...prescription,
      medications: JSON.parse(JSON.stringify(prescription.medications))
    });
  };

  const handleSavePrescription = async () => {
    try {
      await axios.put(`/api/prescriptions/${editingPrescription.prescriptionID}`, {
        medications: editingPrescription.medications,
        instructions: editingPrescription.instructions
      }, {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      alert('Prescription updated successfully!');
      setEditingPrescription(null);
      fetchPatients(); // Refresh data
    } catch (err) {
      alert('Failed to update prescription');
    }
  };

  const updateMedication = (index, field, value) => {
    const newMedications = [...editingPrescription.medications];
    newMedications[index][field] = value;
    setEditingPrescription({
      ...editingPrescription,
      medications: newMedications
    });
  };

  const addMedication = () => {
    setEditingPrescription({
      ...editingPrescription,
      medications: [
        ...editingPrescription.medications,
        { name: '', dosage: '', frequency: '', duration: '' }
      ]
    });
  };

  const removeMedication = (index) => {
    const newMedications = editingPrescription.medications.filter((_, i) => i !== index);
    setEditingPrescription({
      ...editingPrescription,
      medications: newMedications
    });
  };

  if (editingPrescription) {
    return (
      <div className="page-container">
        <div className="form-card" style={{maxWidth: '800px'}}>
          <h1>Edit Prescription</h1>
          
          <div className="medications-editor">
            {editingPrescription.medications.map((med, index) => (
              <div key={index} className="medication-edit-card">
                <div className="medication-edit-header">
                  <h3>Medication {index + 1}</h3>
                  <button 
                    onClick={() => removeMedication(index)}
                    className="btn-danger-small"
                  >
                    Remove
                  </button>
                </div>
                
                <div className="form-group">
                  <label>Medication Name</label>
                  <input
                    type="text"
                    value={med.name}
                    onChange={(e) => updateMedication(index, 'name', e.target.value)}
                  />
                </div>
                
                <div className="form-row">
                  <div className="form-group">
                    <label>Dosage</label>
                    <input
                      type="text"
                      value={med.dosage}
                      onChange={(e) => updateMedication(index, 'dosage', e.target.value)}
                    />
                  </div>
                  
                  <div className="form-group">
                    <label>Frequency</label>
                    <input
                      type="text"
                      value={med.frequency}
                      onChange={(e) => updateMedication(index, 'frequency', e.target.value)}
                    />
                  </div>
                </div>
                
                <div className="form-group">
                  <label>Duration</label>
                  <input
                    type="text"
                    value={med.duration}
                    onChange={(e) => updateMedication(index, 'duration', e.target.value)}
                  />
                </div>
              </div>
            ))}
            
            <button onClick={addMedication} className="btn-secondary">
              + Add Medication
            </button>
          </div>

          <div className="form-group">
            <label>Instructions</label>
            <textarea
              value={editingPrescription.instructions}
              onChange={(e) => setEditingPrescription({
                ...editingPrescription,
                instructions: e.target.value
              })}
              rows="3"
            />
          </div>

          <div className="button-group">
            <button onClick={() => setEditingPrescription(null)} className="btn-secondary">
              Cancel
            </button>
            <button onClick={handleSavePrescription} className="btn-primary">
              Save Changes
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="page-container">
      <div className="dashboard">
        <div className="dashboard-header">
          <div>
            <h1>Dr. {user.firstName} {user.lastName}</h1>
            <p className="subtitle">{user.specialization}</p>
            <p className="subtitle">Managing {patients.length} patient{patients.length !== 1 ? 's' : ''}</p>
          </div>
          <button onClick={handleLogout} className="btn-secondary">Logout</button>
        </div>

        {loading && <p>Loading patients...</p>}
        {error && <div className="error-message">{error}</div>}

        <div className="patients-section">
          {patients.map((patient) => (
            <div key={patient.patientID} className="patient-card">
              <div 
                className="patient-header"
                onClick={() => setSelectedPatient(
                  selectedPatient === patient.patientID ? null : patient.patientID
                )}
                style={{cursor: 'pointer'}}
              >
                <div>
                  <h2>{patient.firstName} {patient.lastName}</h2>
                  <p>{patient.email}</p>
                  <p className="assessment-count">
                    {patient.assessmentCount} assessment{patient.assessmentCount !== 1 ? 's' : ''}
                  </p>
                </div>
                <span className="expand-icon">
                  {selectedPatient === patient.patientID ? '▼' : '▶'}
                </span>
              </div>

              {selectedPatient === patient.patientID && (
                <div className="patient-history">
                  {patient.history.map((item) => (
                    <div key={item.assessmentID} className="history-card">
                      <div className="history-header">
                        <h3>{new Date(item.assessmentDate).toLocaleDateString()}</h3>
                        <span className="history-time">
                          {new Date(item.assessmentDate).toLocaleTimeString()}
                        </span>
                      </div>
                      
                      <div className="history-details">
                        <p><strong>Symptoms:</strong> {item.symptoms.join(', ')}</p>
                        <p><strong>Weight:</strong> {item.weight} {item.weightUnit}</p>
                        <p><strong>Height:</strong> {item.height} {item.heightUnit}</p>
                        <p><strong>Age:</strong> {item.age}</p>
                      </div>

                      {item.prescription && (
                        <div className="prescription-section">
                          <div className="prescription-header-with-edit">
                            <h4>Prescription</h4>
                            <button 
                              onClick={() => handleEditPrescription(item.prescription)}
                              className="btn-edit"
                            >
                              Edit Prescription
                            </button>
                          </div>
                          
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
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default DoctorDashboard;
