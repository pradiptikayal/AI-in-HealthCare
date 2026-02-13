import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

function Assessment({ patient, token }) {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    weight: '',
    weightUnit: 'kg',
    height: '',
    heightUnit: 'cm',
    age: '',
    symptoms: ''
  });
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const symptomsArray = formData.symptoms.split(',').map(s => s.trim()).filter(s => s);
      
      const response = await axios.post('/api/assessments', {
        patientID: patient.userID,
        weight: parseFloat(formData.weight),
        weightUnit: formData.weightUnit,
        height: parseFloat(formData.height),
        heightUnit: formData.heightUnit,
        age: parseInt(formData.age),
        symptoms: symptomsArray
      }, {
        headers: { Authorization: `Bearer ${token}` }
      });

      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.message || 'Assessment submission failed');
    } finally {
      setLoading(false);
    }
  };

  if (result) {
    return (
      <div className="page-container">
        <div className="result-card">
          <h1>Assessment Complete!</h1>
          
          <div className="success-section">
            <h2>Your Prescription</h2>
            {result.prescription.medications.map((med, idx) => (
              <div key={idx} className="medication-result">
                <h3>{med.name}</h3>
                <p><strong>Dosage:</strong> {med.dosage}</p>
                <p><strong>Frequency:</strong> {med.frequency}</p>
                <p><strong>Duration:</strong> {med.duration}</p>
              </div>
            ))}
            <p className="instructions">{result.prescription.instructions}</p>
          </div>

          <div className="doctor-section">
            <h2>Doctor Assignment</h2>
            <p><strong>Doctor:</strong> {result.doctorAssignment.doctorName}</p>
            <p><strong>Specialization:</strong> {result.doctorAssignment.specialization}</p>
            <p><strong>Visit Token:</strong> <code>{result.doctorAssignment.tokenID}</code></p>
            <p className="note">Please bring this token ID when visiting the doctor.</p>
          </div>

          <button onClick={() => navigate('/dashboard')} className="btn-primary">
            Return to Dashboard
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="page-container">
      <div className="form-card">
        <h1>Health Assessment</h1>
        <p className="subtitle">Please provide your current health information</p>
        
        {error && <div className="error-message">{error}</div>}
        
        <form onSubmit={handleSubmit}>
          <div className="form-row">
            <div className="form-group">
              <label>Weight</label>
              <input
                type="number"
                name="weight"
                value={formData.weight}
                onChange={handleChange}
                step="0.1"
                required
              />
            </div>
            <div className="form-group">
              <label>Unit</label>
              <select name="weightUnit" value={formData.weightUnit} onChange={handleChange}>
                <option value="kg">kg</option>
                <option value="lbs">lbs</option>
              </select>
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Height</label>
              <input
                type="number"
                name="height"
                value={formData.height}
                onChange={handleChange}
                step="0.1"
                required
              />
            </div>
            <div className="form-group">
              <label>Unit</label>
              <select name="heightUnit" value={formData.heightUnit} onChange={handleChange}>
                <option value="cm">cm</option>
                <option value="inches">inches</option>
              </select>
            </div>
          </div>

          <div className="form-group">
            <label>Age</label>
            <input
              type="number"
              name="age"
              value={formData.age}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label>Symptoms (comma-separated)</label>
            <textarea
              name="symptoms"
              value={formData.symptoms}
              onChange={handleChange}
              placeholder="e.g., headache, fever, cough"
              rows="3"
              required
            />
            <small>Common symptoms: headache, fever, cough, sore throat, fatigue, nausea</small>
          </div>

          <div className="button-group">
            <button type="button" onClick={() => navigate('/dashboard')} className="btn-secondary">
              Cancel
            </button>
            <button type="submit" className="btn-primary" disabled={loading}>
              {loading ? 'Submitting...' : 'Submit Assessment'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default Assessment;
