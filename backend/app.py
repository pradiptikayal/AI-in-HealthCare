from flask import Flask, request, jsonify
from flask_cors import CORS
import bcrypt
import re
import jwt
import os
from datetime import datetime, timezone, timedelta
from data_access import generate_id, add_record, find_by_id, find_all_by_field, update_record, read_json_file
from bedrock_service import get_bedrock_service

app = Flask(__name__)
CORS(app)

# Secret key for JWT token generation from environment variable
SECRET_KEY = os.getenv('SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable is not set. Please set it in your .env file.")

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

@app.route('/api/login', methods=['POST'])
def unified_login():
    """
    Unified authentication for both patients and doctors.
    
    Expected JSON body:
    {
        "email": "user@example.com",
        "password": "securepassword"
    }
    
    Returns:
        200: Authentication successful with session token and user info
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
        
        # Try to find as patient first
        patients = find_all_by_field('patients.json', 'email', email)
        
        if patients:
            patient = patients[0]
            password_hash = patient.get('passwordHash', '')
            
            if bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8')):
                # Generate JWT token for patient
                token_payload = {
                    'userID': patient['patientID'],
                    'email': patient['email'],
                    'userType': 'patient',
                    'exp': datetime.now(timezone.utc) + timedelta(hours=24)
                }
                
                token = jwt.encode(token_payload, SECRET_KEY, algorithm='HS256')
                
                return jsonify({
                    'message': 'Authentication successful',
                    'token': token,
                    'userType': 'patient',
                    'user': {
                        'userID': patient['patientID'],
                        'firstName': patient['firstName'],
                        'lastName': patient['lastName'],
                        'email': patient['email']
                    }
                }), 200
        
        # Try to find as doctor
        doctors = find_all_by_field('doctors.json', 'email', email)
        
        if doctors:
            doctor = doctors[0]
            password_hash = doctor.get('passwordHash', '')
            
            if bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8')):
                # Generate JWT token for doctor
                token_payload = {
                    'userID': doctor['doctorID'],
                    'email': doctor['email'],
                    'userType': 'doctor',
                    'exp': datetime.now(timezone.utc) + timedelta(hours=24)
                }
                
                token = jwt.encode(token_payload, SECRET_KEY, algorithm='HS256')
                
                return jsonify({
                    'message': 'Authentication successful',
                    'token': token,
                    'userType': 'doctor',
                    'user': {
                        'userID': doctor['doctorID'],
                        'firstName': doctor['firstName'],
                        'lastName': doctor['lastName'],
                        'email': doctor['email'],
                        'specialization': doctor.get('specialization', '')
                    }
                }), 200
        
        # No match found
        return jsonify({
            'error': 'Invalid credentials',
            'message': 'Invalid email or password'
        }), 401
        
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500
def validate_token(token):
    """
    Validate JWT token and return user info.

    Args:
        token: JWT token string

    Returns:
        Dict with userID and userType if valid, None otherwise
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return {
            'userID': payload.get('userID'),
            'userType': payload.get('userType', 'patient')  # Default to patient for backward compatibility
        }
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

@app.route('/api/doctors/patients', methods=['GET'])
def get_doctor_patients():
    """
    Get all patients assigned to a doctor with their complete history.
    
    Requires authentication via Bearer token in Authorization header.
    
    Returns:
        200: List of patients with their assessments and prescriptions
        401: Unauthorized
        403: Forbidden (not a doctor)
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
        user_info = validate_token(token)

        if not user_info:
            return jsonify({
                'error': 'Unauthorized',
                'message': 'Invalid or expired token'
            }), 401

        # Verify user is a doctor
        if user_info['userType'] != 'doctor':
            return jsonify({
                'error': 'Forbidden',
                'message': 'Only doctors can access this endpoint'
            }), 403

        doctor_id = user_info['userID']

        # Get all assignments for this doctor
        assignments = find_all_by_field('assignments.json', 'doctorID', doctor_id)
        
        # Get unique patient IDs
        patient_ids = list(set([a['patientID'] for a in assignments]))
        
        # Build patient data with history
        patients_data = []
        for patient_id in patient_ids:
            # Get patient info
            patient = find_by_id('patients.json', 'patientID', patient_id)
            if not patient:
                continue
            
            # Get assessments
            assessments = find_all_by_field('assessments.json', 'patientID', patient_id)
            
            # Get prescriptions
            prescriptions = find_all_by_field('prescriptions.json', 'patientID', patient_id)
            
            # Create prescription map
            prescription_map = {}
            for prescription in prescriptions:
                assessment_id = prescription.get('assessmentID')
                if assessment_id:
                    prescription_map[assessment_id] = prescription
            
            # Format history
            history = []
            for assessment in assessments:
                assessment_id = assessment.get('assessmentID')
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
                
                if assessment_id in prescription_map:
                    prescription = prescription_map[assessment_id]
                    history_entry['prescription'] = {
                        'prescriptionID': prescription.get('prescriptionID'),
                        'medications': prescription.get('medications', []),
                        'instructions': prescription.get('instructions'),
                        'generatedDate': prescription.get('generatedDate')
                    }
                
                history.append(history_entry)
            
            # Sort history by date
            history.sort(key=lambda x: x.get('assessmentDate', ''), reverse=True)
            
            patients_data.append({
                'patientID': patient_id,
                'firstName': patient.get('firstName'),
                'lastName': patient.get('lastName'),
                'email': patient.get('email'),
                'assessmentCount': len(assessments),
                'history': history
            })
        
        return jsonify({
            'doctorID': doctor_id,
            'patientCount': len(patients_data),
            'patients': patients_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500

@app.route('/api/prescriptions/<prescription_id>', methods=['PUT'])
def update_prescription(prescription_id):
    """
    Update a prescription (doctor can edit AI-generated prescription).
    
    Expected JSON body:
    {
        "medications": [...],
        "instructions": "..."
    }
    
    Returns:
        200: Prescription updated successfully
        401: Unauthorized
        403: Forbidden (not a doctor)
        404: Prescription not found
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
        user_info = validate_token(token)

        if not user_info:
            return jsonify({
                'error': 'Unauthorized',
                'message': 'Invalid or expired token'
            }), 401

        # Verify user is a doctor
        if user_info['userType'] != 'doctor':
            return jsonify({
                'error': 'Forbidden',
                'message': 'Only doctors can edit prescriptions'
            }), 403

        data = request.get_json()
        
        # Find prescription
        prescriptions = find_all_by_field('prescriptions.json', 'prescriptionID', prescription_id)
        if not prescriptions:
            return jsonify({
                'error': 'Not found',
                'message': 'Prescription not found'
            }), 404
        
        # Update prescription
        updates = {}
        if 'medications' in data:
            updates['medications'] = data['medications']
        if 'instructions' in data:
            updates['instructions'] = data['instructions']
        
        updates['lastModifiedBy'] = user_info['userID']
        updates['lastModifiedDate'] = datetime.now(timezone.utc).isoformat()
        
        updated_prescription = update_record('prescriptions.json', 'prescriptionID', prescription_id, updates)
        
        return jsonify({
            'message': 'Prescription updated successfully',
            'prescription': updated_prescription
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500

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
        user_info = validate_token(token)

        if not user_info:
            return jsonify({
                'error': 'Unauthorized',
                'message': 'Invalid or expired token'
            }), 401

        # Verify the authenticated patient is requesting their own history
        if user_info['userType'] == 'patient' and user_info['userID'] != patient_id:
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
        user_info = validate_token(token)

        if not user_info:
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
        
        # Verify authenticated patient matches request (only for patients, doctors can create for any patient)
        if user_info['userType'] == 'patient' and user_info['userID'] != data['patientID']:
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
        
        # Generate prescription using Amazon Bedrock LLM
        bedrock_service = get_bedrock_service()
        prescription_data = bedrock_service.generate_prescription(
            symptoms=symptoms,
            age=age,
            weight=weight,
            weight_unit=data['weightUnit'],
            height=height,
            height_unit=data['heightUnit']
        )
        
        medications = prescription_data['medications']
        instructions = prescription_data['instructions']
        
        prescription_id = generate_id()
        prescription_record = {
            'prescriptionID': prescription_id,
            'assessmentID': assessment_id,
            'patientID': data['patientID'],
            'medications': medications,
            'instructions': instructions,
            'generatedDate': datetime.now(timezone.utc).isoformat(),
            'generatedBy': 'AI-Bedrock'
        }
        
        add_record('prescriptions.json', prescription_record)
        
        # Assign a doctor (get all doctors from database)
        try:
            doctors = read_json_file('doctors.json')
        except:
            doctors = []
        
        if not doctors:
            # Fallback if no doctors in system
            doctors = [{'doctorID': 'd001', 'firstName': 'Dr.', 'lastName': 'Smith', 'specialization': 'General Practice'}]
        
        # Simple selection: use first doctor for MVP
        selected_doctor = doctors[0]
        
        token_id = generate_id()
        assignment_record = {
            'assignmentID': generate_id(),
            'assessmentID': assessment_id,
            'patientID': data['patientID'],
            'doctorID': selected_doctor['doctorID'],
            'doctorName': f"{selected_doctor['firstName']} {selected_doctor['lastName']}",
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
