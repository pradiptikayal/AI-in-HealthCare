"""
Manual integration test for patient login endpoint.
This script tests the complete registration -> login flow.
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_registration_and_login():
    """Test complete registration and login flow."""
    
    # Step 1: Register a new patient
    print("Step 1: Registering a new patient...")
    register_data = {
        "firstName": "Jane",
        "lastName": "Smith",
        "email": "jane.smith@example.com",
        "password": "securepass456"
    }
    
    register_response = requests.post(
        f"{BASE_URL}/api/patients/register",
        json=register_data
    )
    
    print(f"Registration Status: {register_response.status_code}")
    print(f"Registration Response: {json.dumps(register_response.json(), indent=2)}")
    
    if register_response.status_code != 201:
        print("Registration failed!")
        return
    
    patient_id = register_response.json()['patientID']
    print(f"\nPatient registered with ID: {patient_id}")
    
    # Step 2: Login with the registered credentials
    print("\nStep 2: Logging in with registered credentials...")
    login_data = {
        "email": "jane.smith@example.com",
        "password": "securepass456"
    }
    
    login_response = requests.post(
        f"{BASE_URL}/api/login",
        json=login_data
    )
    
    print(f"Login Status: {login_response.status_code}")
    print(f"Login Response: {json.dumps(login_response.json(), indent=2)}")
    
    if login_response.status_code == 200:
        token = login_response.json()['token']
        print(f"\n✓ Login successful! Token received: {token[:50]}...")
    else:
        print("\n✗ Login failed!")
        return
    
    # Step 3: Test invalid password
    print("\nStep 3: Testing login with invalid password...")
    invalid_login_data = {
        "email": "jane.smith@example.com",
        "password": "wrongpassword"
    }
    
    invalid_response = requests.post(
        f"{BASE_URL}/api/login",
        json=invalid_login_data
    )
    
    print(f"Invalid Login Status: {invalid_response.status_code}")
    print(f"Invalid Login Response: {json.dumps(invalid_response.json(), indent=2)}")
    
    if invalid_response.status_code == 401:
        print("\n✓ Invalid credentials correctly rejected!")
    else:
        print("\n✗ Expected 401 status code for invalid credentials")
    
    # Step 4: Test non-existent email
    print("\nStep 4: Testing login with non-existent email...")
    nonexistent_login_data = {
        "email": "nonexistent@example.com",
        "password": "somepassword"
    }
    
    nonexistent_response = requests.post(
        f"{BASE_URL}/api/login",
        json=nonexistent_login_data
    )
    
    print(f"Non-existent Email Status: {nonexistent_response.status_code}")
    print(f"Non-existent Email Response: {json.dumps(nonexistent_response.json(), indent=2)}")
    
    if nonexistent_response.status_code == 401:
        print("\n✓ Non-existent email correctly rejected!")
    else:
        print("\n✗ Expected 401 status code for non-existent email")
    
    print("\n" + "="*60)
    print("Integration test completed successfully!")
    print("="*60)


if __name__ == "__main__":
    print("="*60)
    print("Patient Login Endpoint Integration Test")
    print("="*60)
    print("\nMake sure the Flask server is running on http://localhost:5000")
    print("Start it with: cd backend && python app.py\n")
    
    try:
        # Check if server is running
        health_response = requests.get(f"{BASE_URL}/api/health")
        if health_response.status_code == 200:
            print("✓ Server is running!\n")
            test_registration_and_login()
        else:
            print("✗ Server health check failed")
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to server. Please start the Flask server first.")
        print("Run: cd backend && python app.py")
