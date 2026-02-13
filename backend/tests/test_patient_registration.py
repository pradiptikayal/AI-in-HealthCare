"""
Unit tests for patient registration endpoint.
"""

import os
# Set environment variable BEFORE importing app
os.environ['SECRET_KEY'] = 'test-secret-key-for-unit-tests-only'

import pytest
import json
import sys
from datetime import datetime

# Add parent directory to path to import app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from data_access import read_json_file, write_json_file


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def reset_patients_data():
    """Reset patients.json before each test."""
    write_json_file('patients.json', [])
    yield
    # Cleanup after test
    write_json_file('patients.json', [])


def test_register_patient_success(client):
    """Test successful patient registration."""
    response = client.post('/api/patients/register', 
        json={
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'john.doe@example.com',
            'password': 'securepassword123'
        })
    
    assert response.status_code == 201
    data = response.get_json()
    
    assert data['message'] == 'Patient registered successfully'
    assert 'patientID' in data
    assert data['firstName'] == 'John'
    assert data['lastName'] == 'Doe'
    assert data['email'] == 'john.doe@example.com'
    assert 'passwordHash' not in data  # Should not return password hash
    
    # Verify patient was stored in database
    patients = read_json_file('patients.json')
    assert len(patients) == 1
    assert patients[0]['patientID'] == data['patientID']
    assert patients[0]['email'] == 'john.doe@example.com'
    assert 'passwordHash' in patients[0]


def test_register_patient_missing_first_name(client):
    """Test registration fails when firstName is missing."""
    response = client.post('/api/patients/register',
        json={
            'lastName': 'Doe',
            'email': 'john.doe@example.com',
            'password': 'securepassword123'
        })
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert 'firstName' in data['message']


def test_register_patient_missing_last_name(client):
    """Test registration fails when lastName is missing."""
    response = client.post('/api/patients/register',
        json={
            'firstName': 'John',
            'email': 'john.doe@example.com',
            'password': 'securepassword123'
        })
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert 'lastName' in data['message']


def test_register_patient_missing_email(client):
    """Test registration fails when email is missing."""
    response = client.post('/api/patients/register',
        json={
            'firstName': 'John',
            'lastName': 'Doe',
            'password': 'securepassword123'
        })
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert 'email' in data['message']


def test_register_patient_missing_password(client):
    """Test registration fails when password is missing."""
    response = client.post('/api/patients/register',
        json={
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'john.doe@example.com'
        })
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert 'password' in data['message']


def test_register_patient_empty_fields(client):
    """Test registration fails when fields are empty strings."""
    response = client.post('/api/patients/register',
        json={
            'firstName': '',
            'lastName': 'Doe',
            'email': 'john.doe@example.com',
            'password': 'securepassword123'
        })
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert 'non-empty' in data['message']


def test_register_patient_invalid_email_format(client):
    """Test registration fails with invalid email format."""
    invalid_emails = [
        'notanemail',
        'missing@domain',
        '@nodomain.com',
        'no@domain',
        'spaces in@email.com'
    ]
    
    for invalid_email in invalid_emails:
        response = client.post('/api/patients/register',
            json={
                'firstName': 'John',
                'lastName': 'Doe',
                'email': invalid_email,
                'password': 'securepassword123'
            })
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'email' in data['message'].lower()


def test_register_patient_duplicate_email(client):
    """Test registration fails when email is already registered."""
    # Register first patient
    client.post('/api/patients/register',
        json={
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'john.doe@example.com',
            'password': 'password123'
        })
    
    # Try to register second patient with same email
    response = client.post('/api/patients/register',
        json={
            'firstName': 'Jane',
            'lastName': 'Smith',
            'email': 'john.doe@example.com',
            'password': 'differentpassword'
        })
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert 'already registered' in data['message']
    
    # Verify only one patient was stored
    patients = read_json_file('patients.json')
    assert len(patients) == 1


def test_register_patient_email_case_insensitive(client):
    """Test that email comparison is case-insensitive."""
    # Register with lowercase email
    client.post('/api/patients/register',
        json={
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'john.doe@example.com',
            'password': 'password123'
        })
    
    # Try to register with uppercase email
    response = client.post('/api/patients/register',
        json={
            'firstName': 'Jane',
            'lastName': 'Smith',
            'email': 'JOHN.DOE@EXAMPLE.COM',
            'password': 'differentpassword'
        })
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'already registered' in data['message']


def test_register_patient_unique_ids(client):
    """Test that each registered patient gets a unique ID."""
    # Register multiple patients
    response1 = client.post('/api/patients/register',
        json={
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'john@example.com',
            'password': 'password123'
        })
    
    response2 = client.post('/api/patients/register',
        json={
            'firstName': 'Jane',
            'lastName': 'Smith',
            'email': 'jane@example.com',
            'password': 'password456'
        })
    
    data1 = response1.get_json()
    data2 = response2.get_json()
    
    assert data1['patientID'] != data2['patientID']


def test_register_patient_password_hashed(client):
    """Test that password is hashed before storage."""
    password = 'mysecretpassword'
    response = client.post('/api/patients/register',
        json={
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'john@example.com',
            'password': password
        })
    
    assert response.status_code == 201
    
    # Check stored password is hashed
    patients = read_json_file('patients.json')
    assert len(patients) == 1
    assert patients[0]['passwordHash'] != password
    assert patients[0]['passwordHash'].startswith('$2b$')  # bcrypt hash format


def test_register_patient_whitespace_trimmed(client):
    """Test that whitespace is trimmed from input fields."""
    response = client.post('/api/patients/register',
        json={
            'firstName': '  John  ',
            'lastName': '  Doe  ',
            'email': '  john@example.com  ',
            'password': 'password123'
        })
    
    assert response.status_code == 201
    data = response.get_json()
    
    assert data['firstName'] == 'John'
    assert data['lastName'] == 'Doe'
    assert data['email'] == 'john@example.com'
