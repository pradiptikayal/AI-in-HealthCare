"""
Manual test script for patient history endpoint.

This script demonstrates the patient history endpoint by:
1. Registering a patient
2. Logging in to get a token
3. Creating sample assessments and prescriptions
4. Retrieving patient history

Run the Flask server first: python app.py
Then run this script: python test_history_manual.py
"""

import requests
import json
from datetime import datetime, timezone

BASE_URL = 'http://localhost:5000/api'


def print_response(title, response):
    """Print formatted response."""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def main():
    print("Patient History Endpoint Manual Test")
    print("=" * 60)
    
    # Step 1: Register a patient
    print("\n1. Registering a new patient...")
    register_data = {
        "firstName": "Alice",
        "lastName": "Johnson",
        "email": f"alice.johnson.{datetime.now().timestamp()}@test.com",
        "password": "securepassword123"
    }
    
    response = requests.post(f"{BASE_URL}/patients/register", json=register_data)
    print_response("Registration Response", response)
    
    if response.status_code != 201:
        print("Registration failed. Exiting.")
        return
    
    patient_id = response.json()['patientID']
    print(f"\nPatient ID: {patient_id}")
    
    # Step 2: Login to get token
    print("\n2. Logging in to get authentication token...")
    login_data = {
        "email": register_data['email'],
        "password": register_data['password']
    }
    
    response = requests.post(f"{BASE_URL}/patients/login", json=login_data)
    print_response("Login Response", response)
    
    if response.status_code != 200:
        print("Login failed. Exiting.")
        return
    
    token = response.json()['token']
    headers = {'Authorization': f'Bearer {token}'}
    print(f"\nToken: {token[:50]}...")
    
    # Step 3: Create sample data manually (simulating assessments and prescriptions)
    print("\n3. Creating sample assessments and prescriptions...")
    print("(In a real scenario, these would be created through assessment endpoints)")
    
    # For this demo, we'll manually add data to the JSON files
    from data_access import add_record, generate_id
    
    # Create first assessment
    assessment1_id = generate_id()
    assessment1 = {
        'assessmentID': assessment1_id,
        'patientID': patient_id,
        'weight': 68,
        'weightUnit': 'kg',
        'height': 165,
        'heightUnit': 'cm',
        'age': 28,
        'symptoms': ['headache', 'fever'],
        'followUpResponses': [
            {
                'questionID': 'q1',
                'questionText': 'How long have you had the headache?',
                'answer': '3 days'
            },
            {
                'questionID': 'q2',
                'questionText': 'Rate the pain from 1-10',
                'answer': '7'
            }
        ],
        'assessmentDate': '2024-01-10T09:30:00Z'
    }
    add_record('assessments.json', assessment1)
    print(f"Created assessment 1: {assessment1_id}")
    
    # Create prescription for first assessment
    prescription1_id = generate_id()
    prescription1 = {
        'prescriptionID': prescription1_id,
        'assessmentID': assessment1_id,
        'patientID': patient_id,
        'medications': [
            {
                'name': 'Ibuprofen',
                'dosage': '400mg',
                'frequency': 'Every 6 hours',
                'duration': '5 days'
            },
            {
                'name': 'Acetaminophen',
                'dosage': '500mg',
                'frequency': 'Every 4-6 hours',
                'duration': '5 days'
            }
        ],
        'instructions': 'Take with food. Stay hydrated. Rest as needed.',
        'generatedDate': '2024-01-10T10:00:00Z'
    }
    add_record('prescriptions.json', prescription1)
    print(f"Created prescription 1: {prescription1_id}")
    
    # Create second assessment
    assessment2_id = generate_id()
    assessment2 = {
        'assessmentID': assessment2_id,
        'patientID': patient_id,
        'weight': 67.5,
        'weightUnit': 'kg',
        'height': 165,
        'heightUnit': 'cm',
        'age': 28,
        'symptoms': ['cough', 'sore throat'],
        'followUpResponses': [
            {
                'questionID': 'q3',
                'questionText': 'Is it a dry or wet cough?',
                'answer': 'Dry cough'
            }
        ],
        'assessmentDate': '2024-01-18T14:15:00Z'
    }
    add_record('assessments.json', assessment2)
    print(f"Created assessment 2: {assessment2_id}")
    
    # Create prescription for second assessment
    prescription2_id = generate_id()
    prescription2 = {
        'prescriptionID': prescription2_id,
        'assessmentID': assessment2_id,
        'patientID': patient_id,
        'medications': [
            {
                'name': 'Dextromethorphan',
                'dosage': '10mg',
                'frequency': 'Every 4 hours',
                'duration': '7 days'
            },
            {
                'name': 'Throat Lozenges',
                'dosage': '1 lozenge',
                'frequency': 'As needed',
                'duration': '7 days'
            }
        ],
        'instructions': 'Avoid irritants. Drink warm liquids. Use humidifier.',
        'generatedDate': '2024-01-18T14:45:00Z'
    }
    add_record('prescriptions.json', prescription2)
    print(f"Created prescription 2: {prescription2_id}")
    
    # Create third assessment without prescription
    assessment3_id = generate_id()
    assessment3 = {
        'assessmentID': assessment3_id,
        'patientID': patient_id,
        'weight': 68,
        'weightUnit': 'kg',
        'height': 165,
        'heightUnit': 'cm',
        'age': 28,
        'symptoms': ['fatigue'],
        'followUpResponses': [],
        'assessmentDate': '2024-01-25T11:00:00Z'
    }
    add_record('assessments.json', assessment3)
    print(f"Created assessment 3 (no prescription): {assessment3_id}")
    
    # Step 4: Retrieve patient history
    print("\n4. Retrieving patient history...")
    response = requests.get(f"{BASE_URL}/patients/{patient_id}/history", headers=headers)
    print_response("Patient History Response", response)
    
    if response.status_code == 200:
        history = response.json()['history']
        print(f"\n{'='*60}")
        print(f"Patient History Summary")
        print(f"{'='*60}")
        print(f"Total assessments: {len(history)}")
        
        for i, entry in enumerate(history, 1):
            print(f"\n--- Assessment {i} ---")
            print(f"Date: {entry['assessmentDate']}")
            print(f"Symptoms: {', '.join(entry['symptoms'])}")
            print(f"Weight: {entry['weight']} {entry['weightUnit']}")
            print(f"Height: {entry['height']} {entry['heightUnit']}")
            print(f"Age: {entry['age']}")
            
            if entry.get('followUpResponses'):
                print(f"Follow-up responses: {len(entry['followUpResponses'])}")
                for resp in entry['followUpResponses']:
                    print(f"  Q: {resp['questionText']}")
                    print(f"  A: {resp['answer']}")
            
            if 'prescription' in entry:
                print(f"Prescription:")
                for med in entry['prescription']['medications']:
                    print(f"  - {med['name']}: {med['dosage']}, {med['frequency']}, {med['duration']}")
                print(f"  Instructions: {entry['prescription']['instructions']}")
            else:
                print("No prescription")
    
    # Step 5: Test error cases
    print("\n\n5. Testing error cases...")
    
    # Test without token
    print("\n5a. Request without authentication token...")
    response = requests.get(f"{BASE_URL}/patients/{patient_id}/history")
    print(f"Status Code: {response.status_code} (Expected: 401)")
    print(f"Error: {response.json()['error']}")
    
    # Test with invalid token
    print("\n5b. Request with invalid token...")
    invalid_headers = {'Authorization': 'Bearer invalid-token-12345'}
    response = requests.get(f"{BASE_URL}/patients/{patient_id}/history", headers=invalid_headers)
    print(f"Status Code: {response.status_code} (Expected: 401)")
    print(f"Error: {response.json()['error']}")
    
    # Test accessing another patient's history
    print("\n5c. Request for different patient's history...")
    different_patient_id = 'different-patient-id-123'
    response = requests.get(f"{BASE_URL}/patients/{different_patient_id}/history", headers=headers)
    print(f"Status Code: {response.status_code} (Expected: 403)")
    print(f"Error: {response.json()['error']}")
    
    print("\n\n" + "="*60)
    print("Manual test completed successfully!")
    print("="*60)


if __name__ == '__main__':
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\nError: Could not connect to the server.")
        print("Please make sure the Flask server is running:")
        print("  python app.py")
    except Exception as e:
        print(f"\nError: {e}")
