# Design Document: Patient Assessment System

## Overview

The Patient Assessment System is a web-based healthcare application with two primary user interfaces: a Patient Portal and a Doctor Portal. The system follows a three-tier architecture with a presentation layer (web UI), business logic layer (application services), and data persistence layer (database).

The application enables patients to register, authenticate, complete health assessments with intelligent follow-up questions, and receive dummy prescriptions with doctor assignments. Doctors can access a separate portal to retrieve patient prescriptions by Patient ID.

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Presentation Layer                       │
│  ┌──────────────────────┐      ┌──────────────────────┐    │
│  │   Patient Portal     │      │   Doctor Portal      │    │
│  │  - Registration      │      │  - Prescription      │    │
│  │  - Sign In           │      │    Retrieval         │    │
│  │  - Assessment Form   │      │                      │    │
│  └──────────────────────┘      └──────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   Business Logic Layer                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Auth Service │  │ Assessment   │  │ Prescription │     │
│  │              │  │ Service      │  │ Service      │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│  ┌──────────────┐  ┌──────────────┐                       │
│  │ Patient      │  │ Follow-up    │                       │
│  │ Service      │  │ Question     │                       │
│  │              │  │ Engine       │                       │
│  └──────────────┘  └──────────────┘                       │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   Data Persistence Layer                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Patient      │  │ Assessment   │  │ Prescription │     │
│  │ Repository   │  │ Repository   │  │ Repository   │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
                    ┌──────────────┐
                    │  JSON Files  │
                    │  - patients  │
                    │  - assess.   │
                    │  - prescript.│
                    │  - doctors   │
                    │  - assign.   │
                    └──────────────┘
```

### Technology Stack Considerations

The design is technology-agnostic but assumes:
- Web-based frontend (HTML/CSS/JavaScript framework)
- RESTful API or similar backend architecture
- JSON file-based storage for data persistence (can be migrated to SQL Server later)
- Session management for authentication

## Components and Interfaces

### 1. Patient Service

**Responsibilities:**
- Patient registration
- Patient authentication
- Patient history retrieval

**Interface:**
```
registerPatient(registrationData: RegistrationData) -> Result<PatientID, ValidationError>
authenticatePatient(credentials: Credentials) -> Result<Session, AuthError>
getPatientHistory(patientID: PatientID) -> Result<List<Assessment>, NotFoundError>
getPatientByID(patientID: PatientID) -> Result<Patient, NotFoundError>
```

### 2. Assessment Service

**Responsibilities:**
- Health assessment form management
- Assessment data validation
- Assessment storage

**Interface:**
```
createAssessment(patientID: PatientID, assessmentData: AssessmentData) -> Result<AssessmentID, ValidationError>
getAssessment(assessmentID: AssessmentID) -> Result<Assessment, NotFoundError>
getAssessmentsByPatient(patientID: PatientID) -> Result<List<Assessment>, NotFoundError>
validateAssessmentData(assessmentData: AssessmentData) -> Result<Valid, ValidationError>
```

### 3. Follow-up Question Engine

**Responsibilities:**
- Generate relevant follow-up questions based on symptoms
- Store follow-up responses

**Interface:**
```
generateFollowUpQuestions(symptoms: List<Symptom>) -> List<Question>
storeFollowUpResponses(assessmentID: AssessmentID, responses: List<Response>) -> Result<Success, Error>
getFollowUpResponses(assessmentID: AssessmentID) -> Result<List<Response>, NotFoundError>
```

### 4. Prescription Service

**Responsibilities:**
- Generate dummy prescriptions based on assessment
- Retrieve prescriptions by patient ID
- Associate prescriptions with assessments

**Interface:**
```
generatePrescription(assessmentID: AssessmentID, assessmentData: AssessmentData) -> Result<Prescription, Error>
getPrescriptionsByPatient(patientID: PatientID) -> Result<List<Prescription>, NotFoundError>
getPrescription(prescriptionID: PrescriptionID) -> Result<Prescription, NotFoundError>
```

### 5. Doctor Assignment Service

**Responsibilities:**
- Assign doctors to patient assessments
- Generate visit tokens
- Manage doctor-patient relationships

**Interface:**
```
assignDoctor(assessmentID: AssessmentID) -> Result<DoctorAssignment, Error>
generateVisitToken(patientID: PatientID, doctorID: DoctorID) -> TokenID
getAssignmentByToken(tokenID: TokenID) -> Result<DoctorAssignment, NotFoundError>
```

### 6. Authentication Service

**Responsibilities:**
- User authentication (patients and doctors)
- Session management
- Credential validation

**Interface:**
```
login(credentials: Credentials, userType: UserType) -> Result<Session, AuthError>
logout(sessionID: SessionID) -> Result<Success, Error>
validateSession(sessionID: SessionID) -> Result<Valid, InvalidSessionError>
```

## Data Models

### Patient
```
Patient {
  patientID: PatientID (unique, auto-generated)
  firstName: String (required)
  lastName: String (required)
  email: String (required, unique)
  passwordHash: String (required)
  dateOfBirth: Date (optional)
  phoneNumber: String (optional)
  registrationDate: Timestamp (auto-generated)
}
```

### Assessment
```
Assessment {
  assessmentID: AssessmentID (unique, auto-generated)
  patientID: PatientID (required, foreign key)
  weight: Number (required, positive)
  weightUnit: String (required, enum: "kg", "lbs")
  height: Number (required, positive)
  heightUnit: String (required, enum: "cm", "inches")
  age: Integer (required, positive)
  symptoms: List<String> (required, non-empty)
  followUpResponses: List<FollowUpResponse> (optional)
  assessmentDate: Timestamp (auto-generated)
}
```

### FollowUpResponse
```
FollowUpResponse {
  questionID: String (required)
  questionText: String (required)
  answer: String (required)
}
```

### Prescription
```
Prescription {
  prescriptionID: PrescriptionID (unique, auto-generated)
  assessmentID: AssessmentID (required, foreign key)
  patientID: PatientID (required, foreign key)
  medications: List<Medication> (required, non-empty)
  instructions: String (required)
  generatedDate: Timestamp (auto-generated)
}
```

### Medication
```
Medication {
  name: String (required)
  dosage: String (required)
  frequency: String (required)
  duration: String (required)
}
```

### DoctorAssignment
```
DoctorAssignment {
  assignmentID: AssignmentID (unique, auto-generated)
  assessmentID: AssessmentID (required, foreign key)
  patientID: PatientID (required, foreign key)
  doctorID: DoctorID (required)
  doctorName: String (required)
  tokenID: TokenID (unique, auto-generated)
  assignmentDate: Timestamp (auto-generated)
}
```

### Doctor
```
Doctor {
  doctorID: DoctorID (unique, auto-generated)
  firstName: String (required)
  lastName: String (required)
  email: String (required, unique)
  passwordHash: String (required)
  specialization: String (optional)
}
```

## Correctness Properties


A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.

### Property 1: Patient Registration Creates Unique ID
*For any* valid registration data, registering a patient should create a unique Patient_ID and store the patient record such that the patient can be retrieved by that ID.
**Validates: Requirements 1.1**

### Property 2: Invalid Registration Data Rejected
*For any* incomplete or invalid registration data (missing required fields, invalid email format, etc.), the registration attempt should be rejected with appropriate validation errors.
**Validates: Requirements 1.2**

### Property 3: Valid Credentials Grant Access
*For any* registered patient with valid credentials, authentication should succeed and grant access to the Patient_Portal.
**Validates: Requirements 2.1**

### Property 4: Invalid Credentials Rejected
*For any* invalid credentials (wrong password, non-existent user, malformed input), the authentication attempt should be rejected with an appropriate error message.
**Validates: Requirements 2.2**

### Property 5: Patient History Retrieval Completeness
*For any* patient with N assessments, retrieving patient history should return all N assessments associated with that Patient_ID.
**Validates: Requirements 3.1**

### Property 6: History Display Contains Required Fields
*For any* patient history display, all assessments should include assessment dates, symptoms, and associated prescriptions.
**Validates: Requirements 3.3**

### Property 7: Incomplete Assessment Data Rejected
*For any* assessment submission with missing required fields (weight, height, age, or symptoms), the submission should be rejected with validation errors.
**Validates: Requirements 4.2**

### Property 8: Valid Assessment Data Persisted
*For any* complete and valid assessment data, submitting the assessment should store it associated with the correct Patient_ID such that it can be retrieved later.
**Validates: Requirements 4.3**

### Property 9: Numeric Fields Accept Valid Values with Units
*For any* valid numeric value with appropriate units (weight in kg/lbs, height in cm/inches), the assessment form should accept the input without errors.
**Validates: Requirements 4.4, 4.5**

### Property 10: Symptoms Generate Follow-up Questions
*For any* assessment with specific symptoms, the system should generate at least one relevant follow-up question related to those symptoms.
**Validates: Requirements 5.1**

### Property 11: Follow-up Responses Stored with Assessment
*For any* follow-up responses provided by a patient, the responses should be stored and associated with the correct assessment such that they can be retrieved together.
**Validates: Requirements 5.2**

### Property 12: Assessment Completion Generates Prescription
*For any* completed health assessment, the system should generate a Dummy_Prescription based on the assessment data.
**Validates: Requirements 6.1**

### Property 13: Prescription Contains Required Fields
*For any* generated prescription, it should include at least one medication with name, dosage, frequency, duration, and general instructions.
**Validates: Requirements 6.2**

### Property 14: Assessment Completion Assigns Doctor
*For any* completed health assessment, the system should assign a doctor to the patient and create a doctor assignment record.
**Validates: Requirements 7.1**

### Property 15: Token ID Uniqueness
*For any* set of doctor assignments, all generated Token_IDs should be unique (no duplicates).
**Validates: Requirements 7.2**

### Property 16: Doctor Authentication Grants Prescription Access
*For any* authenticated doctor, the system should grant access to the prescription retrieval functionality.
**Validates: Requirements 8.2**

### Property 17: Valid Patient ID Retrieves All Prescriptions
*For any* valid Patient_ID with N prescriptions, querying by that Patient_ID should return all N prescriptions associated with that patient.
**Validates: Requirements 9.1**

### Property 18: Invalid Patient ID Returns Error
*For any* Patient_ID that does not exist in the system, attempting to retrieve prescriptions should return a "patient not found" error.
**Validates: Requirements 9.2**

### Property 19: Prescription Display Contains Complete Information
*For any* prescription display, it should show assessment data (weight, height, age), symptoms, follow-up responses, and prescription details (medications with dosages).
**Validates: Requirements 9.3**

### Property 20: Data Persistence Immediate Retrieval
*For any* data created or updated (patient, assessment, prescription), immediately retrieving that data should return the newly created or updated version.
**Validates: Requirements 10.1, 10.3**

## Error Handling

### Validation Errors

**Registration Validation:**
- Missing required fields (firstName, lastName, email, password)
- Invalid email format
- Duplicate email (patient already exists)
- Weak password (if password requirements exist)

**Authentication Errors:**
- Invalid credentials (wrong password)
- User not found
- Session expired
- Unauthorized access attempts

**Assessment Validation:**
- Missing required fields (weight, height, age, symptoms)
- Invalid numeric values (negative weight/height, non-numeric input)
- Invalid units (unsupported weight/height units)
- Age out of reasonable range

**Prescription Retrieval Errors:**
- Patient ID not found
- No prescriptions available for patient
- Unauthorized access (doctor not authenticated)

### Error Response Format

All errors should follow a consistent format:
```
ErrorResponse {
  errorCode: String (machine-readable error identifier)
  message: String (human-readable error description)
  field: String (optional, for validation errors)
  timestamp: Timestamp
}
```

### Error Handling Strategy

1. **Input Validation**: Validate all inputs at the service layer before processing
2. **Graceful Degradation**: Return meaningful error messages rather than system crashes
3. **Error Logging**: Log all errors with context for debugging
4. **User Feedback**: Provide clear, actionable error messages to users
5. **Security**: Avoid exposing sensitive system information in error messages

## Testing Strategy

### Dual Testing Approach

The system will employ both unit testing and property-based testing to ensure comprehensive coverage:

**Unit Tests:**
- Specific examples demonstrating correct behavior
- Edge cases (empty patient history, no symptoms, etc.)
- Error conditions and validation scenarios
- Integration points between components

**Property-Based Tests:**
- Universal properties that hold across all inputs
- Comprehensive input coverage through randomization
- Minimum 100 iterations per property test
- Each test tagged with feature name and property number

### Property-Based Testing Configuration

**Testing Library Selection:**
- Python: Hypothesis
- TypeScript/JavaScript: fast-check
- Java: jqwik or QuickCheck for Java
- Other languages: Select appropriate PBT library

**Test Configuration:**
- Minimum 100 iterations per property test
- Each property test must reference its design document property
- Tag format: `Feature: patient-assessment-system, Property {number}: {property_text}`
- Each correctness property implemented by a SINGLE property-based test

### Testing Coverage

**Patient Service:**
- Unit tests: Specific registration examples, authentication flows
- Property tests: Properties 1-4 (registration, authentication)

**Assessment Service:**
- Unit tests: Specific assessment examples, validation edge cases
- Property tests: Properties 7-9 (assessment validation, persistence)

**Follow-up Question Engine:**
- Unit tests: Specific symptom-question mappings
- Property tests: Properties 10-11 (question generation, response storage)

**Prescription Service:**
- Unit tests: Specific prescription generation examples
- Property tests: Properties 12-13, 17-19 (prescription generation, retrieval, display)

**Doctor Assignment Service:**
- Unit tests: Specific assignment examples
- Property tests: Properties 14-15 (doctor assignment, token uniqueness)

**Data Persistence:**
- Unit tests: Specific CRUD operations
- Property tests: Property 20 (immediate retrieval consistency)

### Integration Testing

**End-to-End Flows:**
1. New patient registration → sign-in → assessment → prescription generation
2. Existing patient sign-in → assessment with follow-ups → doctor assignment
3. Doctor portal access → prescription retrieval by patient ID

**Cross-Component Testing:**
- Assessment creation triggers prescription generation
- Prescription generation triggers doctor assignment
- Patient history retrieval includes all related data

### Test Data Management

**Generators for Property-Based Tests:**
- Random patient registration data (valid and invalid)
- Random assessment data with various symptom combinations
- Random follow-up responses
- Random Patient_IDs (valid and invalid)

**Test Database:**
- Use in-memory database or test database for isolation
- Reset database state between tests
- Seed data for integration tests

## Implementation Notes

### Security Considerations

1. **Password Storage**: Use bcrypt or similar hashing algorithm for password storage
2. **Session Management**: Implement secure session tokens with expiration
3. **Input Sanitization**: Sanitize all user inputs to prevent injection attacks
4. **Access Control**: Enforce role-based access (patients can only access their own data)
5. **HTTPS**: All communication should use HTTPS in production

### Performance Considerations

1. **File Access Optimization**: Implement caching for frequently accessed JSON files
2. **File Locking**: Use file locking mechanisms to prevent concurrent write conflicts
3. **Pagination**: Implement pagination for patient history if assessments grow large
4. **Async Operations**: Consider async file I/O for better performance

### Scalability Considerations

1. **Migration Path**: Design data access layer to easily migrate from JSON to SQL Server
2. **Repository Pattern**: Use repository pattern to abstract data storage implementation
3. **Stateless Services**: Design services to be stateless for horizontal scaling
4. **Monitoring**: Implement logging and monitoring for system health

**Note on JSON Storage**: The current implementation uses JSON files for simplicity and rapid development. This approach is suitable for demonstration and small-scale use. For production use with multiple concurrent users, migration to SQL Server or another relational database is recommended. The repository pattern ensures this migration can be done with minimal changes to business logic.

### Follow-up Question Engine Implementation

The follow-up question engine can use a rule-based approach:

**Symptom-to-Question Mapping:**
```
symptomRules = {
  "headache": ["How long have you had the headache?", "Rate the pain from 1-10", "Is it constant or intermittent?"],
  "fever": ["What is your temperature?", "How long have you had the fever?", "Any other symptoms?"],
  "cough": ["Is it a dry or wet cough?", "How long have you been coughing?", "Any chest pain?"],
  "fatigue": ["How long have you felt fatigued?", "Does rest help?", "Any recent life changes?"],
  // ... more symptom mappings
}
```

**Question Selection Logic:**
1. Parse symptoms from assessment
2. Match symptoms to question rules
3. Return relevant questions (limit to 3-5 per symptom)
4. Store responses with assessment

### Dummy Prescription Generation Logic

The prescription generator can use a simple rule-based approach:

**Symptom-to-Medication Mapping:**
```
prescriptionRules = {
  "headache": {medication: "Ibuprofen", dosage: "200mg", frequency: "Every 6 hours", duration: "3 days"},
  "fever": {medication: "Acetaminophen", dosage: "500mg", frequency: "Every 4-6 hours", duration: "5 days"},
  "cough": {medication: "Dextromethorphan", dosage: "10mg", frequency: "Every 4 hours", duration: "7 days"},
  // ... more symptom mappings
}
```

**Generation Logic:**
1. Parse symptoms from assessment
2. Match symptoms to medication rules
3. Generate prescription with matched medications
4. Add general instructions based on symptoms

**Note:** This is a dummy/demonstration system. Real prescription generation requires medical expertise and should not be used for actual medical advice.
