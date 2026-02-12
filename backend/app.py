from flask import Flask, request, jsonify
from flask_cors import CORS
import bcrypt
import re
import jwt
from datetime import datetime, timezone, timedelta
from data_access import generate_id, add_record, find_by_id, find_all_by_field

app = Flask(__name__)
CORS(app)

# Secret key for JWT token generation (in production, use environment variable)
SECRET_KEY = 'your-secret-key-change-in-production'

@app.route('/api/health', methods=['GET'])
def health_check():
    return {'status': 'ok', 'message': 'Patient Assessment System API is running'}

@app.route('/api/patients/register', methods=['POST'])
def register_patient():
    """
    Register a new patient.
    
    Expected JSON body:
    {
        "firstName": "John",
        "lastName": "Doe",
        "email": "john.doe@example.com",
        "password": "securepassword"
    }
    
    Returns:
        201: Patient registered successfully with Patient_ID
        400: Validation error (missing fields, invalid email, duplicate email)
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['firstName', 'lastName', 'email', 'password']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({
                'error': 'Validation error',
                'message': f'Missing required fields: {", ".join(missing_fields)}'
            }), 400
        
        # Extract and validate data
        first_name = data['firstName'].strip() if isinstance(data['firstName'], str) else ''
        last_name = data['lastName'].strip() if isinstance(data['lastName'], str) else ''
        email = data['email'].strip().lower() if isinstance(data['email'], str) else ''
        password = data['password'] if isinstance(data['password'], str) else ''
        
        # Validate non-empty fields
        if not first_name or not last_name or not email or not password:
            return jsonify({
                'error': 'Validation error',
                'message': 'All fields must be non-empty'
            }), 400
        
        # Validate email format
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            return jsonify({
                'error': 'Validation error',
                'message': 'Invalid email format'
            }), 400
        
        # Check for duplicate email
        existing_patients = find_all_by_field('patients.json', 'email', email)
        if existing_patients:
            return jsonify({
                'error': 'Validation error',
                'message': 'Email already registered'
            }), 400
        
        # Hash password using bcrypt
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # Generate unique Patient_ID
        patient_id = generate_id()
        
        # Create patient record
        patient_record = {
            'patientID': patient_id,
            'firstName': first_name,
            'lastName': last_name,
            'email': email,
            'passwordHash': password_hash.decode('utf-8'),
            'registrationDate': datetime.now(timezone.utc).isoformat()
        }
        
        # Store patient record
        add_record('patients.json', patient_record)
        
        # Return success response (don't include password hash)
        return jsonify({
            'message': 'Patient registered successfully',
            'patientID': patient_id,
            'firstName': first_name,
            'lastName': last_name,
            'email': email
        }), 201
        
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500

@app.route('/api/patients/login', methods=['POST'])
def login_patient():
    """
    Authenticate a patient and generate session token.
    
    Expected JSON body:
    {
        "email": "john.doe@example.com",
        "password": "securepassword"
    }
    
    Returns:
        200: Authentication successful with session token and patient info
        400: Validation error (missing fields)
        401: Invalid credentials
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['email', 'password']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({
                'error': 'Validation error',
                'message': f'Missing required fields: {", ".join(missing_fields)}'
            }), 400
        
        # Extract credentials
        email = data['email'].strip().lower() if isinstance(data['email'], str) else ''
        password = data['password'] if isinstance(data['password'], str) else ''
        
        # Validate non-empty fields
        if not email or not password:
            return jsonify({
                'error': 'Validation error',
                'message': 'Email and password must be non-empty'
            }), 400
        
        # Find patient by email
        patients = find_all_by_field('patients.json', 'email', email)
        
        if not patients:
            return jsonify({
                'error': 'Invalid credentials',
                'message': 'Invalid email or password'
            }), 401
        
        patient = patients[0]
        
        # Verify password
        password_hash = patient.get('passwordHash', '')
        if not bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8')):
            return jsonify({
                'error': 'Invalid credentials',
                'message': 'Invalid email or password'
            }), 401
        
        # Generate JWT token
        token_payload = {
            'patientID': patient['patientID'],
            'email': patient['email'],
            'exp': datetime.now(timezone.utc) + timedelta(hours=24)  # Token expires in 24 hours
        }
        
        token = jwt.encode(token_payload, SECRET_KEY, algorithm='HS256')
        
        # Return success response with token and patient info
        return jsonify({
            'message': 'Authentication successful',
            'token': token,
            'patient': {
                'patientID': patient['patientID'],
                'firstName': patient['firstName'],
                'lastName': patient['lastName'],
                'email': patient['email']
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500
def validate_token(token):
    """
    Validate JWT token and return patient ID.

    Args:
        token: JWT token string

    Returns:
        Patient ID if valid, None otherwise
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload.get('patientID')
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

@app.route('/api/patients/<patient_id>/history', methods=['GET'])
def get_patient_history(patient_id):
    """
    Retrieve patient history including assessments and prescriptions.

    Requires authentication via Bearer token in Authorization header.

    Returns:
        200: Patient history with assessments and prescriptions
        401: Unauthorized (missing or invalid token)
        403: Forbidden (token patient_id doesn't match requested patient_id)
        404: Patient not found
    """
    try:
        # Validate authentication
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({
                'error': 'Unauthorized',
                'message': 'Missing or invalid authorization header'
            }), 401

        token = auth_header.split(' ')[1]
        authenticated_patient_id = validate_token(token)

        if not authenticated_patient_id:
            return jsonify({
                'error': 'Unauthorized',
                'message': 'Invalid or expired token'
            }), 401

        # Verify the authenticated patient is requesting their own history
        if authenticated_patient_id != patient_id:
            return jsonify({
                'error': 'Forbidden',
                'message': 'You can only access your own patient history'
            }), 403

        # Verify patient exists
        patient = find_by_id('patients.json', 'patientID', patient_id)
        if not patient:
            return jsonify({
                'error': 'Not found',
                'message': 'Patient not found'
            }), 404

        # Read assessments for this patient
        assessments = find_all_by_field('assessments.json', 'patientID', patient_id)

        # Read all prescriptions for this patient
        prescriptions = find_all_by_field('prescriptions.json', 'patientID', patient_id)

        # Create a map of assessment_id to prescription for quick lookup
        prescription_map = {}
        for prescription in prescriptions:
            assessment_id = prescription.get('assessmentID')
            if assessment_id:
                prescription_map[assessment_id] = prescription

        # Format history data
        history = []
        for assessment in assessments:
            assessment_id = assessment.get('assessmentID')

            # Build history entry
            history_entry = {
                'assessmentID': assessment_id,
                'assessmentDate': assessment.get('assessmentDate'),
                'weight': assessment.get('weight'),
                'weightUnit': assessment.get('weightUnit'),
                'height': assessment.get('height'),
                'heightUnit': assessment.get('heightUnit'),
                'age': assessment.get('age'),
                'symptoms': assessment.get('symptoms', []),
                'followUpResponses': assessment.get('followUpResponses', [])
            }

            # Add prescription if it exists
            if assessment_id in prescription_map:
                prescription = prescription_map[assessment_id]
                history_entry['prescription'] = {
                    'prescriptionID': prescription.get('prescriptionID'),
                    'medications': prescription.get('medications', []),
                    'instructions': prescription.get('instructions'),
                    'generatedDate': prescription.get('generatedDate')
                }

            history.append(history_entry)

        # Sort history by assessment date (most recent first)
        history.sort(key=lambda x: x.get('assessmentDate', ''), reverse=True)

        return jsonify({
            'patientID': patient_id,
            'history': history
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500


# Simple symptom-to-medication mapping for MVP
SYMPTOM_MEDICATIONS = {
    'headache': {'name': 'Ibuprofen', 'dosage': '200mg', 'frequency': 'Every 6 hours', 'duration': '3 days'},
    'fever': {'name': 'Acetaminophen', 'dosage': '500mg', 'frequency': 'Every 4-6 hours', 'duration': '5 days'},
    'cough': {'name': 'Dextromethorphan', 'dosage': '10mg', 'frequency': 'Every 4 hours', 'duration': '7 days'},
    'sore throat': {'name': 'Throat Lozenges', 'dosage': '1 lozenge', 'frequency': 'Every 2-3 hours', 'duration': '5 days'},
    'fatigue': {'name': 'Multivitamin', 'dosage': '1 tablet', 'frequency': 'Once daily', 'duration': '30 days'},
    'nausea': {'name': 'Ondansetron', 'dosage': '4mg', 'frequency': 'Every 8 hours', 'duration': '3 days'},
}

@app.route('/api/assessments', methods=['POST'])
def create_assessment():
    """
    Create a new health assessment and generate prescription.
    
    Expected JSON body:
    {
        "patientID": "patient-uuid",
        "weight": 70,
        "weightUnit": "kg",
        "height": 175,
        "heightUnit": "cm",
        "age": 30,
        "symptoms": ["headache", "fever"]
    }
    
    Returns:
        201: Assessment created with prescription and doctor assignment
        400: Validation error
        401: Unauthorized
    """
    try:
        # Validate authentication
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({
                'error': 'Unauthorized',
                'message': 'Missing or invalid authorization header'
            }), 401

        token = auth_header.split(' ')[1]
        authenticated_patient_id = validate_token(token)

        if not authenticated_patient_id:
            return jsonify({
                'error': 'Unauthorized',
                'message': 'Invalid or expired token'
            }), 401

        data = request.get_json()
        
        # Validate required fields
        required_fields = ['patientID', 'weight', 'weightUnit', 'height', 'heightUnit', 'age', 'symptoms']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({
                'error': 'Validation error',
                'message': f'Missing required fields: {", ".join(missing_fields)}'
            }), 400
        
        # Verify authenticated patient matches request
        if authenticated_patient_id != data['patientID']:
            return jsonify({
                'error': 'Forbidden',
                'message': 'You can only create assessments for yourself'
            }), 403
        
        # Validate data types and values
        try:
            weight = float(data['weight'])
            height = float(data['height'])
            age = int(data['age'])
            
            if weight <= 0 or height <= 0 or age <= 0:
                raise ValueError("Values must be positive")
        except (ValueError, TypeError):
            return jsonify({
                'error': 'Validation error',
                'message': 'Weight, height, and age must be positive numbers'
            }), 400
        
        # Validate units
        if data['weightUnit'] not in ['kg', 'lbs']:
            return jsonify({
                'error': 'Validation error',
                'message': 'Weight unit must be "kg" or "lbs"'
            }), 400
        
        if data['heightUnit'] not in ['cm', 'inches']:
            return jsonify({
                'error': 'Validation error',
                'message': 'Height unit must be "cm" or "inches"'
            }), 400
        
        # Validate symptoms
        symptoms = data['symptoms']
        if not isinstance(symptoms, list) or len(symptoms) == 0:
            return jsonify({
                'error': 'Validation error',
                'message': 'Symptoms must be a non-empty list'
            }), 400
        
        # Create assessment
        assessment_id = generate_id()
        assessment_record = {
            'assessmentID': assessment_id,
            'patientID': data['patientID'],
            'weight': weight,
            'weightUnit': data['weightUnit'],
            'height': height,
            'heightUnit': data['heightUnit'],
            'age': age,
            'symptoms': symptoms,
            'followUpResponses': [],
            'assessmentDate': datetime.now(timezone.utc).isoformat()
        }
        
        add_record('assessments.json', assessment_record)
        
        # Generate prescription based on symptoms
        medications = []
        for symptom in symptoms:
            symptom_lower = symptom.lower()
            if symptom_lower in SYMPTOM_MEDICATIONS:
                medications.append(SYMPTOM_MEDICATIONS[symptom_lower])
        
        # If no matching medications, provide general advice
        if not medications:
            medications.append({
                'name': 'General Rest and Hydration',
                'dosage': 'As needed',
                'frequency': 'Throughout the day',
                'duration': 'Until symptoms improve'
            })
        
        prescription_id = generate_id()
        prescription_record = {
            'prescriptionID': prescription_id,
            'assessmentID': assessment_id,
            'patientID': data['patientID'],
            'medications': medications,
            'instructions': 'Take medications as directed. Consult a doctor if symptoms persist or worsen.',
            'generatedDate': datetime.now(timezone.utc).isoformat()
        }
        
        add_record('prescriptions.json', prescription_record)
        
        # Assign a doctor (simple round-robin)
        doctors = find_all_by_field('doctors.json', 'doctorID', None)  # Get all doctors
        if not doctors:
            # Fallback if no doctors in system
            doctors = [{'doctorID': 'd001', 'firstName': 'Dr.', 'lastName': 'Smith', 'specialization': 'General Practice'}]
        
        # Simple selection: use first doctor for MVP
        selected_doctor = doctors[0] if doctors else None
        
        token_id = generate_id()
        assignment_record = {
            'assignmentID': generate_id(),
            'assessmentID': assessment_id,
            'patientID': data['patientID'],
            'doctorID': selected_doctor['doctorID'] if selected_doctor else 'd001',
            'doctorName': f"{selected_doctor.get('firstName', 'Dr.')} {selected_doctor.get('lastName', 'Smith')}",
            'tokenID': token_id,
            'assignmentDate': datetime.now(timezone.utc).isoformat()
        }
        
        add_record('assignments.json', assignment_record)
        
        # Return complete response
        return jsonify({
            'message': 'Assessment created successfully',
            'assessment': {
                'assessmentID': assessment_id,
                'assessmentDate': assessment_record['assessmentDate']
            },
            'prescription': {
                'prescriptionID': prescription_id,
                'medications': medications,
                'instructions': prescription_record['instructions']
            },
            'doctorAssignment': {
                'doctorName': assignment_record['doctorName'],
                'tokenID': token_id,
                'specialization': selected_doctor.get('specialization', 'General Practice') if selected_doctor else 'General Practice'
            }
        }), 201
        
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
