"""
Unit tests for patient history endpoint.

Tests the GET /api/patients/{patient_id}/history endpoint.
"""

import os
# Set environment variable BEFORE importing app
TEST_SECRET_KEY = 'test-secret-key-for-unit-tests-only'
os.environ['SECRET_KEY'] = TEST_SECRET_KEY

import pytest
import json
import jwt
from datetime import datetime, timezone, timedelta
from app import app
from data_access import write_json_file


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def setup_test_data():
    """Set up test data for patient history tests."""
    # Create test patient
    patient_id = 'test-patient-123'
    patient_data = [{
        'patientID': patient_id,
        'firstName': 'John',
        'lastName': 'Doe',
        'email': 'john.doe@test.com',
        'passwordHash': '$2b$12$test',
        'registrationDate': '2024-01-01T00:00:00Z'
    }]
    write_json_file('patients.json', patient_data)
    
    # Create test assessments
    assessment1_id = 'assessment-1'
    assessment2_id = 'assessment-2'
    assessments_data = [
        {
            'assessmentID': assessment1_id,
            'patientID': patient_id,
            'weight': 70,
            'weightUnit': 'kg',
            'height': 175,
            'heightUnit': 'cm',
            'age': 30,
            'symptoms': ['headache', 'fever'],
            'followUpResponses': [
                {'questionID': 'q1', 'questionText': 'How long?', 'answer': '2 days'}
            ],
            'assessmentDate': '2024-01-15T10:00:00Z'
        },
        {
            'assessmentID': assessment2_id,
            'patientID': patient_id,
            'weight': 71,
            'weightUnit': 'kg',
            'height': 175,
            'heightUnit': 'cm',
            'age': 30,
            'symptoms': ['cough'],
            'followUpResponses': [],
            'assessmentDate': '2024-01-20T10:00:00Z'
        }
    ]
    write_json_file('assessments.json', assessments_data)
    
    # Create test prescriptions
    prescriptions_data = [
        {
            'prescriptionID': 'prescription-1',
            'assessmentID': assessment1_id,
            'patientID': patient_id,
            'medications': [
                {
                    'name': 'Ibuprofen',
                    'dosage': '200mg',
                    'frequency': 'Every 6 hours',
                    'duration': '3 days'
                }
            ],
            'instructions': 'Take with food',
            'generatedDate': '2024-01-15T10:30:00Z'
        },
        {
            'prescriptionID': 'prescription-2',
            'assessmentID': assessment2_id,
            'patientID': patient_id,
            'medications': [
                {
                    'name': 'Cough Syrup',
                    'dosage': '10ml',
                    'frequency': 'Every 4 hours',
                    'duration': '7 days'
                }
            ],
            'instructions': 'Shake well before use',
            'generatedDate': '2024-01-20T10:30:00Z'
        }
    ]
    write_json_file('prescriptions.json', prescriptions_data)
    
    yield patient_id
    
    # Cleanup
    write_json_file('patients.json', [])
    write_json_file('assessments.json', [])
    write_json_file('prescriptions.json', [])


def generate_test_token(patient_id):
    """Generate a test JWT token for authentication."""
    token_payload = {
        'userID': patient_id,
        'email': 'john.doe@test.com',
        'userType': 'patient',
        'exp': datetime.now(timezone.utc) + timedelta(hours=24)
    }
    return jwt.encode(token_payload, TEST_SECRET_KEY, algorithm='HS256')


def test_get_patient_history_success(client, setup_test_data):
    """Test successful retrieval of patient history."""
    patient_id = setup_test_data
    token = generate_test_token(patient_id)
    
    response = client.get(
        f'/api/patients/{patient_id}/history',
        headers={'Authorization': f'Bearer {token}'}
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    
    assert data['patientID'] == patient_id
    assert 'history' in data
    assert len(data['history']) == 2
    
    # Check that history is sorted by date (most recent first)
    assert data['history'][0]['assessmentDate'] == '2024-01-20T10:00:00Z'
    assert data['history'][1]['assessmentDate'] == '2024-01-15T10:00:00Z'
    
    # Check first history entry (most recent)
    first_entry = data['history'][0]
    assert first_entry['symptoms'] == ['cough']
    assert first_entry['weight'] == 71
    assert first_entry['weightUnit'] == 'kg'
    assert 'prescription' in first_entry
    assert first_entry['prescription']['medications'][0]['name'] == 'Cough Syrup'
    
    # Check second history entry
    second_entry = data['history'][1]
    assert second_entry['symptoms'] == ['headache', 'fever']
    assert len(second_entry['followUpResponses']) == 1
    assert 'prescription' in second_entry
    assert second_entry['prescription']['medications'][0]['name'] == 'Ibuprofen'


def test_get_patient_history_no_auth_header(client, setup_test_data):
    """Test patient history request without authorization header."""
    patient_id = setup_test_data
    
    response = client.get(f'/api/patients/{patient_id}/history')
    
    assert response.status_code == 401
    data = json.loads(response.data)
    assert data['error'] == 'Unauthorized'


def test_get_patient_history_invalid_token(client, setup_test_data):
    """Test patient history request with invalid token."""
    patient_id = setup_test_data
    
    response = client.get(
        f'/api/patients/{patient_id}/history',
        headers={'Authorization': 'Bearer invalid-token'}
    )
    
    assert response.status_code == 401
    data = json.loads(response.data)
    assert data['error'] == 'Unauthorized'


def test_get_patient_history_wrong_patient(client, setup_test_data):
    """Test patient trying to access another patient's history."""
    patient_id = setup_test_data
    token = generate_test_token('different-patient-id')
    
    response = client.get(
        f'/api/patients/{patient_id}/history',
        headers={'Authorization': f'Bearer {token}'}
    )
    
    assert response.status_code == 403
    data = json.loads(response.data)
    assert data['error'] == 'Forbidden'


def test_get_patient_history_patient_not_found(client, setup_test_data):
    """Test patient history for non-existent patient."""
    non_existent_id = 'non-existent-patient'
    token = generate_test_token(non_existent_id)
    
    response = client.get(
        f'/api/patients/{non_existent_id}/history',
        headers={'Authorization': f'Bearer {token}'}
    )
    
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['error'] == 'Not found'


def test_get_patient_history_empty(client):
    """Test patient history when patient has no assessments."""
    # Create patient with no assessments
    patient_id = 'test-patient-empty'
    patient_data = [{
        'patientID': patient_id,
        'firstName': 'Jane',
        'lastName': 'Smith',
        'email': 'jane.smith@test.com',
        'passwordHash': '$2b$12$test',
        'registrationDate': '2024-01-01T00:00:00Z'
    }]
    write_json_file('patients.json', patient_data)
    write_json_file('assessments.json', [])
    write_json_file('prescriptions.json', [])
    
    token = generate_test_token(patient_id)
    
    response = client.get(
        f'/api/patients/{patient_id}/history',
        headers={'Authorization': f'Bearer {token}'}
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['patientID'] == patient_id
    assert data['history'] == []
    
    # Cleanup
    write_json_file('patients.json', [])


def test_get_patient_history_assessment_without_prescription(client):
    """Test patient history when assessment has no prescription."""
    # Create patient and assessment without prescription
    patient_id = 'test-patient-no-rx'
    patient_data = [{
        'patientID': patient_id,
        'firstName': 'Bob',
        'lastName': 'Jones',
        'email': 'bob.jones@test.com',
        'passwordHash': '$2b$12$test',
        'registrationDate': '2024-01-01T00:00:00Z'
    }]
    write_json_file('patients.json', patient_data)
    
    assessment_id = 'assessment-no-rx'
    assessments_data = [{
        'assessmentID': assessment_id,
        'patientID': patient_id,
        'weight': 80,
        'weightUnit': 'kg',
        'height': 180,
        'heightUnit': 'cm',
        'age': 35,
        'symptoms': ['fatigue'],
        'followUpResponses': [],
        'assessmentDate': '2024-01-25T10:00:00Z'
    }]
    write_json_file('assessments.json', assessments_data)
    write_json_file('prescriptions.json', [])
    
    token = generate_test_token(patient_id)
    
    response = client.get(
        f'/api/patients/{patient_id}/history',
        headers={'Authorization': f'Bearer {token}'}
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data['history']) == 1
    assert 'prescription' not in data['history'][0]
    
    # Cleanup
    write_json_file('patients.json', [])
    write_json_file('assessments.json', [])
