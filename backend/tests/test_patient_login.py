"""
Unit tests for patient authentication endpoint.
Tests Requirements 2.1 and 2.2.
"""

import pytest
import json
import bcrypt
import jwt
from datetime import datetime, timezone
from app import app, SECRET_KEY
from data_access import write_json_file, read_json_file


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def setup_test_patient():
    """Set up a test patient in the database."""
    # Create a test patient
    password = "testpassword123"
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    test_patient = {
        'patientID': 'test-patient-id-123',
        'firstName': 'Test',
        'lastName': 'Patient',
        'email': 'test@example.com',
        'passwordHash': password_hash.decode('utf-8'),
        'registrationDate': datetime.now(timezone.utc).isoformat()
    }
    
    # Write to patients.json
    write_json_file('patients.json', [test_patient])
    
    yield {
        'patient': test_patient,
        'password': password
    }
    
    # Cleanup: reset patients.json
    write_json_file('patients.json', [])


def test_login_success(client, setup_test_patient):
    """Test successful patient login with valid credentials."""
    response = client.post('/api/patients/login', 
                           json={
                               'email': 'test@example.com',
                               'password': 'testpassword123'
                           })
    
    assert response.status_code == 200
    data = json.loads(response.data)
    
    assert 'message' in data
    assert data['message'] == 'Authentication successful'
    assert 'token' in data
    assert 'patient' in data
    
    # Verify patient info
    patient_info = data['patient']
    assert patient_info['patientID'] == 'test-patient-id-123'
    assert patient_info['firstName'] == 'Test'
    assert patient_info['lastName'] == 'Patient'
    assert patient_info['email'] == 'test@example.com'
    
    # Verify token is valid JWT
    token = data['token']
    decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    assert decoded['patientID'] == 'test-patient-id-123'
    assert decoded['email'] == 'test@example.com'


def test_login_invalid_password(client, setup_test_patient):
    """Test login with invalid password."""
    response = client.post('/api/patients/login',
                           json={
                               'email': 'test@example.com',
                               'password': 'wrongpassword'
                           })
    
    assert response.status_code == 401
    data = json.loads(response.data)
    
    assert 'error' in data
    assert data['error'] == 'Invalid credentials'
    assert 'message' in data


def test_login_nonexistent_email(client, setup_test_patient):
    """Test login with non-existent email."""
    response = client.post('/api/patients/login',
                           json={
                               'email': 'nonexistent@example.com',
                               'password': 'somepassword'
                           })
    
    assert response.status_code == 401
    data = json.loads(response.data)
    
    assert 'error' in data
    assert data['error'] == 'Invalid credentials'


def test_login_missing_email(client):
    """Test login with missing email field."""
    response = client.post('/api/patients/login',
                           json={
                               'password': 'somepassword'
                           })
    
    assert response.status_code == 400
    data = json.loads(response.data)
    
    assert 'error' in data
    assert data['error'] == 'Validation error'
    assert 'email' in data['message']


def test_login_missing_password(client):
    """Test login with missing password field."""
    response = client.post('/api/patients/login',
                           json={
                               'email': 'test@example.com'
                           })
    
    assert response.status_code == 400
    data = json.loads(response.data)
    
    assert 'error' in data
    assert data['error'] == 'Validation error'
    assert 'password' in data['message']


def test_login_empty_email(client):
    """Test login with empty email."""
    response = client.post('/api/patients/login',
                           json={
                               'email': '',
                               'password': 'somepassword'
                           })
    
    assert response.status_code == 400
    data = json.loads(response.data)
    
    assert 'error' in data
    assert data['error'] == 'Validation error'


def test_login_empty_password(client):
    """Test login with empty password."""
    response = client.post('/api/patients/login',
                           json={
                               'email': 'test@example.com',
                               'password': ''
                           })
    
    assert response.status_code == 400
    data = json.loads(response.data)
    
    assert 'error' in data
    assert data['error'] == 'Validation error'


def test_login_case_insensitive_email(client, setup_test_patient):
    """Test that email matching is case-insensitive."""
    response = client.post('/api/patients/login',
                           json={
                               'email': 'TEST@EXAMPLE.COM',
                               'password': 'testpassword123'
                           })
    
    assert response.status_code == 200
    data = json.loads(response.data)
    
    assert data['message'] == 'Authentication successful'
    assert 'token' in data
