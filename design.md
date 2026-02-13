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
│  └──────────────┘  └──────────────┘  └──────┬───────┘     │
│  ┌──────────────┐  ┌──────────────┐         │             │
│  │ Patient      │  │ Follow-up    │         │             │
│  │ Service      │  │ Question     │         │             │
│  │              │  │ Engine       │         │             │
│  └──────────────┘  └──────────────┘         │             │
│                                              │             │
│  ┌──────────────────────────────────────────┘             │
│  │ Bedrock AI Service                                     │
│  │ - Prompt Engineering                                   │
│  │ - LLM Integration                                      │
│  │ - Response Parsing                                     │
│  │ - Fallback Logic                                       │
│  └────────────────────────────────────────────────────────┘
└─────────────────────────────────────────────────────────────┘
                    │                    │
                    │                    └──────────────────┐
                    ▼                                       ▼
┌─────────────────────────────────────┐    ┌──────────────────────┐
│   Data Persistence Layer            │    │  Amazon Bedrock      │
│  ┌──────────────┐  ┌──────────────┐│    │  (AWS Cloud)         │
│  │ Patient      │  │ Assessment   ││    │                      │
│  │ Repository   │  │ Repository   ││    │  Claude 3 Sonnet     │
│  └──────────────┘  └──────────────┘│    │  - Context-aware     │
│  ┌──────────────┐                  │    │  - Personalized      │
│  │ Prescription │                  │    │  - AI-powered        │
│  │ Repository   │                  │    │                      │
│  └──────────────┘                  │    └──────────────────────┘
└─────────────────────────────────────┘
                    │
                    ▼
            ┌──────────────┐
            │  SQL Server  │
            │  Database    │
            └──────────────┘
```

### Technology Stack Considerations

The design is technology-agnostic but assumes:
- Web-based frontend (HTML/CSS/JavaScript framework)
- RESTful API or similar backend architecture
- SQL Server database for data persistence
- Session management for authentication
- Amazon Bedrock for AI-powered prescription generation

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
- Generate AI-powered prescriptions using Amazon Bedrock
- Fallback to rule-based prescription generation
- Retrieve prescriptions by patient ID
- Associate prescriptions with assessments
- Track prescription generation method (AI vs rule-based)

**Interface:**
```
generatePrescription(assessmentID: AssessmentID, assessmentData: AssessmentData) -> Result<Prescription, Error>
getPrescriptionsByPatient(patientID: PatientID) -> Result<List<Prescription>, NotFoundError>
getPrescription(prescriptionID: PrescriptionID) -> Result<Prescription, NotFoundError>
updatePrescription(prescriptionID: PrescriptionID, updates: PrescriptionUpdates, doctorID: DoctorID) -> Result<Prescription, Error>
```

### 4a. Bedrock AI Service

**Responsibilities:**
- Interface with Amazon Bedrock API
- Construct prompts with patient data
- Parse and validate LLM responses
- Handle errors and fallback scenarios
- Manage AWS credentials and configuration

**Interface:**
```
generateAIPrescription(
    symptoms: List<Symptom>,
    age: int,
    weight: float,
    weightUnit: string,
    height: float,
    heightUnit: string
) -> Result<PrescriptionData, Error>

invokeBedrock(prompt: string) -> Result<string, Error>
parseResponse(response: string) -> Result<PrescriptionData, ParseError>
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

## Database Schema

### SQL Server Tables

#### Patients Table
```sql
CREATE TABLE Patients (
    PatientID UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    FirstName NVARCHAR(100) NOT NULL,
    LastName NVARCHAR(100) NOT NULL,
    Email NVARCHAR(255) NOT NULL UNIQUE,
    PasswordHash NVARCHAR(255) NOT NULL,
    DateOfBirth DATE NULL,
    PhoneNumber NVARCHAR(20) NULL,
    RegistrationDate DATETIME2 DEFAULT GETUTCDATE(),
    INDEX IX_Patients_Email (Email)
);
```

#### Assessments Table
```sql
CREATE TABLE Assessments (
    AssessmentID UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    PatientID UNIQUEIDENTIFIER NOT NULL,
    Weight DECIMAL(10,2) NOT NULL CHECK (Weight > 0),
    WeightUnit NVARCHAR(10) NOT NULL CHECK (WeightUnit IN ('kg', 'lbs')),
    Height DECIMAL(10,2) NOT NULL CHECK (Height > 0),
    HeightUnit NVARCHAR(10) NOT NULL CHECK (HeightUnit IN ('cm', 'inches')),
    Age INT NOT NULL CHECK (Age > 0 AND Age < 150),
    Symptoms NVARCHAR(MAX) NOT NULL, -- JSON array
    FollowUpResponses NVARCHAR(MAX) NULL, -- JSON array
    AssessmentDate DATETIME2 DEFAULT GETUTCDATE(),
    FOREIGN KEY (PatientID) REFERENCES Patients(PatientID) ON DELETE CASCADE,
    INDEX IX_Assessments_PatientID (PatientID),
    INDEX IX_Assessments_Date (AssessmentDate DESC)
);
```

#### Prescriptions Table
```sql
CREATE TABLE Prescriptions (
    PrescriptionID UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    AssessmentID UNIQUEIDENTIFIER NOT NULL,
    PatientID UNIQUEIDENTIFIER NOT NULL,
    Medications NVARCHAR(MAX) NOT NULL, -- JSON array
    Instructions NVARCHAR(MAX) NOT NULL,
    GeneratedDate DATETIME2 DEFAULT GETUTCDATE(),
    GeneratedBy NVARCHAR(50) NULL, -- 'AI-Bedrock' or 'Rule-Based'
    LastModifiedBy UNIQUEIDENTIFIER NULL, -- DoctorID who modified
    LastModifiedDate DATETIME2 NULL,
    FOREIGN KEY (AssessmentID) REFERENCES Assessments(AssessmentID) ON DELETE CASCADE,
    FOREIGN KEY (PatientID) REFERENCES Patients(PatientID) ON DELETE NO ACTION,
    INDEX IX_Prescriptions_PatientID (PatientID),
    INDEX IX_Prescriptions_AssessmentID (AssessmentID)
);
```

#### Doctors Table
```sql
CREATE TABLE Doctors (
    DoctorID UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    FirstName NVARCHAR(100) NOT NULL,
    LastName NVARCHAR(100) NOT NULL,
    Email NVARCHAR(255) NOT NULL UNIQUE,
    PasswordHash NVARCHAR(255) NOT NULL,
    Specialization NVARCHAR(100) NULL,
    INDEX IX_Doctors_Email (Email)
);
```

#### DoctorAssignments Table
```sql
CREATE TABLE DoctorAssignments (
    AssignmentID UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    AssessmentID UNIQUEIDENTIFIER NOT NULL,
    PatientID UNIQUEIDENTIFIER NOT NULL,
    DoctorID UNIQUEIDENTIFIER NOT NULL,
    DoctorName NVARCHAR(200) NOT NULL,
    TokenID UNIQUEIDENTIFIER NOT NULL UNIQUE,
    AssignmentDate DATETIME2 DEFAULT GETUTCDATE(),
    FOREIGN KEY (AssessmentID) REFERENCES Assessments(AssessmentID) ON DELETE CASCADE,
    FOREIGN KEY (PatientID) REFERENCES Patients(PatientID) ON DELETE NO ACTION,
    FOREIGN KEY (DoctorID) REFERENCES Doctors(DoctorID) ON DELETE NO ACTION,
    INDEX IX_DoctorAssignments_PatientID (PatientID),
    INDEX IX_DoctorAssignments_DoctorID (DoctorID),
    INDEX IX_DoctorAssignments_TokenID (TokenID)
);
```

### Database Relationships

```
Patients (1) ──────< (N) Assessments
    │                      │
    │                      │
    │                      └──< (1) Prescriptions
    │                      │
    │                      └──< (1) DoctorAssignments
    │                                    │
    └────────────────────────────────────┘
                                         │
Doctors (1) ────────────────────────────┘
```

### JSON Field Structures

#### Symptoms Field (in Assessments)
```json
["headache", "fever", "cough"]
```

#### FollowUpResponses Field (in Assessments)
```json
[
  {
    "questionID": "q1",
    "questionText": "How long have you had the headache?",
    "answer": "2 days"
  }
]
```

#### Medications Field (in Prescriptions)
```json
[
  {
    "name": "Ibuprofen",
    "dosage": "200mg",
    "frequency": "Every 6 hours",
    "duration": "3 days"
  }
]
```



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

### Database Connection Configuration

**Connection String Format:**
```
Server=your_server_name;Database=PatientAssessmentDB;User Id=your_username;Password=your_password;Encrypt=True;TrustServerCertificate=False;
```

**Environment Variables:**
```
DB_SERVER=your_server_name
DB_NAME=PatientAssessmentDB
DB_USER=your_username
DB_PASSWORD=your_password
DB_ENCRYPT=True
```

**Connection Pooling Settings:**
- Min Pool Size: 5
- Max Pool Size: 100
- Connection Timeout: 30 seconds
- Command Timeout: 30 seconds

### Database Migration Strategy

**Initial Setup:**
1. Create database: `CREATE DATABASE PatientAssessmentDB`
2. Run table creation scripts in order (Patients, Doctors, Assessments, Prescriptions, DoctorAssignments)
3. Create indexes for performance
4. Seed initial doctor data

**Data Migration from JSON:**
1. Export existing JSON data
2. Transform to SQL INSERT statements
3. Import into SQL Server tables
4. Verify data integrity
5. Update application configuration
6. Test all endpoints

### ORM/Data Access Layer

**Recommended Approaches:**
- **Python**: SQLAlchemy or pyodbc
- **Node.js**: Sequelize or mssql
- **C#/.NET**: Entity Framework Core or Dapper

**Repository Pattern Implementation:**
```python
class PatientRepository:
    def create(self, patient_data) -> Patient
    def find_by_id(self, patient_id) -> Patient
    def find_by_email(self, email) -> Patient
    def update(self, patient_id, updates) -> Patient
    def delete(self, patient_id) -> bool
```

### Security Considerations

1. **Password Storage**: Use bcrypt or similar hashing algorithm for password storage
2. **Session Management**: Implement secure session tokens with expiration
3. **Input Sanitization**: Sanitize all user inputs to prevent injection attacks
4. **SQL Injection Prevention**: Use parameterized queries/prepared statements for all database operations
5. **Access Control**: Enforce role-based access (patients can only access their own data)
6. **HTTPS**: All communication should use HTTPS in production
7. **Database Security**: 
   - Use least privilege principle for database users
   - Enable SQL Server encryption at rest
   - Implement row-level security where appropriate
   - Regular security audits and updates

### Performance Considerations

1. **Database Indexing**: Implement appropriate indexes on frequently queried columns (Email, PatientID, DoctorID)
2. **Connection Pooling**: Use connection pooling for efficient database connections
3. **Query Optimization**: Use parameterized queries and avoid N+1 query problems
4. **Caching**: Implement caching for frequently accessed data (doctor lists, etc.)
5. **Pagination**: Implement pagination for patient history and large result sets
6. **Async Operations**: Use async database operations for better performance

### Scalability Considerations

1. **Database Design**: SQL Server provides ACID compliance, transactions, and concurrent access
2. **Repository Pattern**: Use repository pattern to abstract data storage implementation
3. **Stateless Services**: Design services to be stateless for horizontal scaling
4. **Monitoring**: Implement logging and monitoring for system health
5. **Read Replicas**: Consider read replicas for scaling read-heavy operations
6. **Stored Procedures**: Use stored procedures for complex queries and better performance

**SQL Server Benefits**:
- **ACID Transactions**: Ensures data consistency and integrity
- **Concurrent Access**: Handles multiple users simultaneously with proper locking
- **Scalability**: Supports vertical and horizontal scaling
- **Backup & Recovery**: Built-in backup and point-in-time recovery
- **Security**: Row-level security, encryption, and audit logging
- **Performance**: Query optimization, indexing, and execution plans

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

The prescription generator uses Amazon Bedrock AI for intelligent, context-aware prescription generation with a fallback to rule-based system.

#### AI-Powered Prescription Generation (Primary)

**Amazon Bedrock Integration:**

The system uses Amazon Bedrock with Claude 3 Sonnet to generate intelligent prescriptions based on comprehensive patient data.

**Architecture:**
```
Assessment Data → Bedrock Service → LLM (Claude 3) → Structured Prescription
     ↓                                                         ↓
  Fallback Rule-Based System ←─────────────────────────────────┘
  (if Bedrock unavailable)
```

**Bedrock Service Interface:**
```python
class BedrockService:
    def generate_prescription(
        symptoms: List[str],
        age: int,
        weight: float,
        weight_unit: str,
        height: float,
        height_unit: str
    ) -> PrescriptionData
```

**LLM Prompt Structure:**
```
You are a medical AI assistant helping to generate preliminary medication recommendations.

Patient Information:
- Age: {age} years
- Weight: {weight} {weight_unit}
- Height: {height} {height_unit}
- Symptoms: {symptoms}

Generate a preliminary prescription recommendation with medications and general instructions.
This is for informational purposes only and will be reviewed by a licensed physician.

Respond with JSON:
{
  "medications": [
    {
      "name": "Medication Name",
      "dosage": "dosage amount",
      "frequency": "how often",
      "duration": "how long"
    }
  ],
  "instructions": "General care instructions"
}
```

**Bedrock Configuration:**
- **Model**: anthropic.claude-3-sonnet-20240229-v1:0
- **Region**: us-east-1 (configurable)
- **Max Tokens**: 1000
- **Temperature**: 0.7
- **Authentication**: AWS IAM credentials or IAM role

**AWS Configuration Requirements:**
```
Environment Variables:
- AWS_REGION: AWS region for Bedrock (default: us-east-1)
- AWS_ACCESS_KEY_ID: AWS access key
- AWS_SECRET_ACCESS_KEY: AWS secret key
- BEDROCK_MODEL_ID: Model identifier (default: Claude 3 Sonnet)
```

**IAM Permissions Required:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream"
      ],
      "Resource": "arn:aws:bedrock:*::foundation-model/*"
    }
  ]
}
```

**Response Processing:**
1. Invoke Bedrock API with patient data
2. Parse JSON response from LLM
3. Validate prescription structure
4. Store with `generatedBy: 'AI-Bedrock'` marker
5. Return structured prescription data

**Error Handling:**
- Network errors → Fallback to rule-based system
- Invalid AWS credentials → Fallback to rule-based system
- LLM timeout → Fallback to rule-based system
- Invalid JSON response → Fallback to rule-based system
- All errors logged for monitoring

**Benefits of AI-Powered Generation:**
- Context-aware recommendations considering age, weight, height
- More detailed and personalized instructions
- Natural language explanations
- Considers symptom combinations intelligently
- Continuously improving with model updates

**Cost Considerations:**
- Claude 3 Sonnet: ~$0.003 per 1K input tokens, ~$0.015 per 1K output tokens
- Average prescription: ~500 input + 200 output tokens
- Cost per prescription: ~$0.005 (half a cent)
- Prescriptions cached in database (no repeated API calls)

#### Rule-Based Prescription Generation (Fallback)

**Symptom-to-Medication Mapping:**
```
prescriptionRules = {
  "headache": {medication: "Ibuprofen", dosage: "200mg", frequency: "Every 6 hours", duration: "3 days"},
  "fever": {medication: "Acetaminophen", dosage: "500mg", frequency: "Every 4-6 hours", duration: "5 days"},
  "cough": {medication: "Dextromethorphan", dosage: "10mg", frequency: "Every 4 hours", duration: "7 days"},
  "sore throat": {medication: "Throat Lozenges", dosage: "1 lozenge", frequency: "Every 2-3 hours", duration: "5 days"},
  "fatigue": {medication: "Multivitamin", dosage: "1 tablet", frequency: "Once daily", duration: "30 days"},
  "nausea": {medication: "Ondansetron", dosage: "4mg", frequency: "Every 8 hours", duration: "3 days"}
}
```

**Fallback Generation Logic:**
1. Parse symptoms from assessment
2. Match symptoms to medication rules
3. Generate prescription with matched medications
4. Add general instructions based on symptoms
5. Store without `generatedBy` field (indicates fallback)

**When Fallback is Used:**
- AWS credentials not configured
- Bedrock service unavailable
- Network connectivity issues
- API rate limits exceeded
- Development/testing environments without AWS access

**Fallback Advantages:**
- Zero cost
- No external dependencies
- Instant response
- Predictable behavior
- Works offline

### AI Integration Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   Assessment Service                         │
│                                                              │
│  createAssessment(patientData, symptoms)                    │
│         │                                                    │
│         ▼                                                    │
│  ┌──────────────────────────────────────┐                  │
│  │   Bedrock Service                    │                  │
│  │                                      │                  │
│  │  Try:                                │                  │
│  │    1. Build LLM prompt               │                  │
│  │    2. Call Bedrock API               │                  │
│  │    3. Parse JSON response            │                  │
│  │    4. Return prescription            │                  │
│  │                                      │                  │
│  │  Catch (any error):                  │                  │
│  │    → Fallback to rule-based          │                  │
│  └──────────────────────────────────────┘                  │
│         │                                                    │
│         ▼                                                    │
│  Store prescription in SQL Server                           │
│  (with generatedBy marker)                                  │
└─────────────────────────────────────────────────────────────┘
                    │
                    ▼
        ┌───────────────────────┐
        │   Amazon Bedrock      │
        │   Claude 3 Sonnet     │
        │                       │
        │   - Context-aware     │
        │   - Personalized      │
        │   - Detailed          │
        └───────────────────────┘
```

### Bedrock Integration Best Practices

1. **Prompt Engineering**:
   - Clear, structured prompts
   - Include all relevant patient data
   - Request specific JSON format
   - Add medical disclaimers

2. **Response Validation**:
   - Validate JSON structure
   - Check required fields present
   - Verify medication format
   - Sanitize output

3. **Error Handling**:
   - Graceful degradation to fallback
   - Log all errors for monitoring
   - No user-facing error messages about AI
   - Transparent fallback behavior

4. **Security**:
   - Never send PII to logs
   - Use IAM roles in production (not access keys)
   - Enable AWS CloudTrail for audit
   - Encrypt data in transit (HTTPS)

5. **Cost Optimization**:
   - Cache prescriptions in database
   - No repeated API calls for same assessment
   - Monitor usage with AWS Cost Explorer
   - Set billing alerts

6. **Testing**:
   - Test with Bedrock enabled
   - Test with Bedrock disabled (fallback)
   - Test error scenarios
   - Validate prescription quality

7. **Monitoring**:
   - Track AI vs fallback usage ratio
   - Monitor API latency
   - Log prescription quality metrics
   - Alert on high error rates

**Note:** This is a demonstration system. Real prescription generation requires medical expertise and should not be used for actual medical advice. All AI-generated prescriptions must be reviewed by licensed physicians.


## Future Enhancements

### 1. Speech-to-Text Support

**Overview:**
Enable voice input for patient assessments, allowing patients to speak their symptoms instead of typing.

**Architecture Integration:**

```
┌─────────────────────────────────────────────────────────────┐
│                   Presentation Layer                         │
│  ┌──────────────────────┐                                   │
│  │   Assessment Form    │                                   │
│  │   + Voice Input UI   │                                   │
│  │   + Audio Capture    │                                   │
│  └──────────┬───────────┘                                   │
└─────────────┼───────────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────────────┐
│              Speech Recognition Service                      │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Amazon Transcribe                                   │  │
│  │  - Real-time audio streaming                         │  │
│  │  - Speech-to-text conversion                         │  │
│  │  - Medical vocabulary support                        │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────┼───────────────────────────────────────────────┘
              │
              ▼
        Text → Assessment Service → Prescription Generation
```

**Technical Components:**

**Frontend (Browser):**
```javascript
// Audio capture using Web Audio API
navigator.mediaDevices.getUserMedia({ audio: true })
  .then(stream => {
    // Stream audio to backend
    const mediaRecorder = new MediaRecorder(stream);
    // Send audio chunks to transcription service
  });
```

**Backend Service:**
```python
class SpeechService:
    def transcribe_audio(audio_stream) -> str:
        # Use AWS Transcribe
        transcribe_client = boto3.client('transcribe')
        response = transcribe_client.start_stream_transcription(
            LanguageCode='en-US',
            MediaSampleRateHertz=16000,
            MediaEncoding='pcm',
            AudioStream=audio_stream
        )
        return response['TranscriptResultStream']
```

**AWS Configuration:**
```
Environment Variables:
- AWS_TRANSCRIBE_REGION: AWS region for Transcribe
- TRANSCRIBE_LANGUAGE_CODE: Default language (en-US)
- TRANSCRIBE_VOCABULARY_NAME: Custom medical vocabulary
```

**IAM Permissions:**
```json
{
  "Effect": "Allow",
  "Action": [
    "transcribe:StartStreamTranscription",
    "transcribe:StartTranscriptionJob"
  ],
  "Resource": "*"
}
```

**Benefits:**
- Hands-free assessment completion
- Faster data entry (speaking is 3x faster than typing)
- Better accessibility for elderly and disabled patients
- More natural symptom description

**Cost Estimate:**
- AWS Transcribe: ~$0.024 per minute of audio
- Average assessment: 2-3 minutes of speech
- Cost per assessment: ~$0.05-$0.07

### 2. Multilingual Support

**Overview:**
Support patients speaking in any language with automatic translation to English for processing.

**Architecture Integration:**

```
┌─────────────────────────────────────────────────────────────┐
│                Voice Input (Any Language)                    │
│                         │                                    │
│                         ▼                                    │
│              ┌──────────────────────┐                       │
│              │  Amazon Transcribe   │                       │
│              │  + Language Detection│                       │
│              └──────────┬───────────┘                       │
│                         │                                    │
│                         ▼                                    │
│              ┌──────────────────────┐                       │
│              │  Amazon Translate    │                       │
│              │  Source → English    │                       │
│              └──────────┬───────────┘                       │
│                         │                                    │
│                         ▼                                    │
│              English Text → Assessment                       │
│                         │                                    │
│                         ▼                                    │
│              ┌──────────────────────┐                       │
│              │  Amazon Bedrock      │                       │
│              │  Prescription Gen    │                       │
│              └──────────┬───────────┘                       │
│                         │                                    │
│                         ▼                                    │
│              English Prescription                            │
│              (Optional: Translate back)                      │
└─────────────────────────────────────────────────────────────┘
```

**Technical Components:**

**Language Detection:**
```python
class LanguageService:
    def detect_language(text: str) -> str:
        comprehend = boto3.client('comprehend')
        response = comprehend.detect_dominant_language(Text=text)
        return response['Languages'][0]['LanguageCode']
```

**Translation Service:**
```python
class TranslationService:
    def translate_to_english(text: str, source_language: str) -> str:
        translate = boto3.client('translate')
        response = translate.translate_text(
            Text=text,
            SourceLanguageCode=source_language,
            TargetLanguageCode='en'
        )
        return response['TranslatedText']
    
    def translate_from_english(text: str, target_language: str) -> str:
        translate = boto3.client('translate')
        response = translate.translate_text(
            Text=text,
            SourceLanguageCode='en',
            TargetLanguageCode=target_language
        )
        return response['TranslatedText']
```

**Supported Languages:**
- Spanish (es)
- French (fr)
- German (de)
- Chinese Simplified (zh)
- Chinese Traditional (zh-TW)
- Hindi (hi)
- Arabic (ar)
- Portuguese (pt)
- Russian (ru)
- Japanese (ja)
- Korean (ko)
- Italian (it)
- And 70+ more languages

**AWS Configuration:**
```
Environment Variables:
- AWS_TRANSLATE_REGION: AWS region for Translate
- SUPPORTED_LANGUAGES: Comma-separated list of language codes
- DEFAULT_OUTPUT_LANGUAGE: Default prescription language (en)
```

**IAM Permissions:**
```json
{
  "Effect": "Allow",
  "Action": [
    "translate:TranslateText",
    "comprehend:DetectDominantLanguage"
  ],
  "Resource": "*"
}
```

**Database Schema Updates:**

```sql
-- Add language tracking to assessments
ALTER TABLE Assessments
ADD InputLanguage NVARCHAR(10) NULL,
ADD TranslatedFromLanguage BIT DEFAULT 0;

-- Add language preference to patients
ALTER TABLE Patients
ADD PreferredLanguage NVARCHAR(10) DEFAULT 'en';
```

**Benefits:**
- Global accessibility - support for 70+ languages
- Reduced language barriers in healthcare
- Improved accuracy through native language input
- Better patient comfort and trust

**Cost Estimate:**
- AWS Translate: ~$15 per million characters
- Average assessment: 500 characters
- Cost per assessment: ~$0.0075 (less than 1 cent)

### 3. Combined Workflow Implementation

**End-to-End Service:**

```python
class MultilingualVoiceAssessmentService:
    def __init__(self):
        self.speech_service = SpeechService()
        self.language_service = LanguageService()
        self.translation_service = TranslationService()
        self.bedrock_service = BedrockService()
    
    def process_voice_assessment(
        self,
        audio_stream,
        patient_id: str,
        weight: float,
        height: float,
        age: int
    ) -> dict:
        # Step 1: Transcribe audio to text
        transcribed_text = self.speech_service.transcribe_audio(audio_stream)
        
        # Step 2: Detect language
        detected_language = self.language_service.detect_language(transcribed_text)
        
        # Step 3: Translate to English if needed
        if detected_language != 'en':
            english_text = self.translation_service.translate_to_english(
                transcribed_text, 
                detected_language
            )
        else:
            english_text = transcribed_text
        
        # Step 4: Extract symptoms from text
        symptoms = self.extract_symptoms(english_text)
        
        # Step 5: Generate prescription using Bedrock
        prescription = self.bedrock_service.generate_prescription(
            symptoms=symptoms,
            age=age,
            weight=weight,
            weight_unit='kg',
            height=height,
            height_unit='cm'
        )
        
        # Step 6: Optionally translate prescription back
        if detected_language != 'en':
            prescription['instructions'] = self.translation_service.translate_from_english(
                prescription['instructions'],
                detected_language
            )
        
        return {
            'original_text': transcribed_text,
            'detected_language': detected_language,
            'english_text': english_text,
            'prescription': prescription
        }
```

**Frontend UI Components:**

```javascript
// Voice input button with language indicator
<VoiceInputButton 
  onTranscript={(text, language) => {
    setSymptoms(text);
    setDetectedLanguage(language);
  }}
  supportedLanguages={['en', 'es', 'fr', 'de', 'zh', 'hi', 'ar']}
/>

// Language selector for prescription output
<LanguageSelector
  value={prescriptionLanguage}
  onChange={setPrescriptionLanguage}
  label="Prescription Language"
/>
```

### Implementation Roadmap

**Phase 1: Speech-to-Text (English Only)**
- Estimated Time: 2-3 weeks
- Components:
  - Frontend audio capture
  - AWS Transcribe integration
  - Voice input UI components
  - Testing with medical vocabulary

**Phase 2: Multilingual Translation**
- Estimated Time: 2-3 weeks
- Components:
  - Language detection service
  - AWS Translate integration
  - Database schema updates
  - Multi-language UI support

**Phase 3: Optimization & Enhancement**
- Estimated Time: 1-2 weeks
- Components:
  - Custom medical vocabulary for Transcribe
  - Caching for common translations
  - Performance optimization
  - Comprehensive testing

### Testing Strategy

**Speech-to-Text Testing:**
- Test with various accents and speech patterns
- Test with medical terminology
- Test with background noise
- Test audio quality variations

**Translation Testing:**
- Verify accuracy of medical term translations
- Test with idiomatic expressions
- Validate prescription translation quality
- Test with multiple language combinations

**Integration Testing:**
- End-to-end workflow testing
- Performance testing under load
- Cost monitoring and optimization
- User acceptance testing

### Monitoring & Analytics

**Metrics to Track:**
- Speech recognition accuracy rate
- Translation accuracy rate
- Language distribution of users
- Average processing time per assessment
- Cost per assessment by feature
- User satisfaction scores

**AWS CloudWatch Metrics:**
- Transcribe API latency
- Translate API latency
- Error rates by service
- Cost tracking by service

### Security & Privacy Considerations

**Audio Data:**
- Audio streams not stored permanently
- Encrypted in transit (TLS)
- Temporary storage only for processing
- Automatic deletion after transcription

**Translation Data:**
- No data retention by AWS Translate
- Patient data anonymized in logs
- Compliance with HIPAA requirements
- Audit trail for all translations

**Compliance:**
- GDPR compliance for EU patients
- HIPAA compliance for US patients
- Data residency requirements
- Patient consent for voice recording

### Cost Optimization Strategies

1. **Caching**: Cache common symptom translations
2. **Batch Processing**: Group translation requests when possible
3. **Compression**: Compress audio before transmission
4. **Selective Translation**: Only translate when necessary
5. **Custom Vocabulary**: Reduce transcription errors and retries

### Success Metrics

**Adoption:**
- 30% of assessments use voice input within 6 months
- Support for 10+ languages within 1 year
- 95% transcription accuracy for medical terms

**User Experience:**
- 50% reduction in assessment completion time
- 80% user satisfaction with voice input
- 90% translation accuracy for medical content

**Business Impact:**
- 25% increase in patient engagement
- Expanded market reach to non-English speakers
- Improved accessibility ratings
