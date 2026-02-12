# Implementation Plan: Patient Assessment System

## Overview

This implementation plan breaks down the Patient Assessment System into discrete coding tasks. The system uses React for the frontend and Python for the backend, following a RESTful API architecture. Tasks are organized to build incrementally, with testing integrated throughout.

## Tasks

- [x] 1. Set up project structure and dependencies
  - Create backend directory with Python virtual environment
  - Set up Flask/FastAPI for REST API
  - Create React frontend with create-react-app or Vite
  - Configure CORS for frontend-backend communication
  - Install testing frameworks (pytest for backend, Jest/React Testing Library for frontend)
  - Create .gitignore and basic project documentation
  - _Requirements: All requirements depend on proper project setup_

- [ ] 2. Implement JSON-based data storage
  - [x] 2.1 Create JSON file structure for data storage
    - Create data directory in backend
    - Create patients.json file with empty array
    - Create assessments.json file with empty array
    - Create prescriptions.json file with empty array
    - Create doctors.json file with sample doctor records
    - Create assignments.json file with empty array
    - _Requirements: 1.1, 2.1, 4.3, 6.1, 7.1_
  
  - [x] 2.2 Create data access utility functions
    - Write functions to read from JSON files
    - Write functions to write to JSON files
    - Implement ID generation (UUID or incremental)
    - Add file locking for concurrent access safety
    - _Requirements: 10.1, 10.3_
  
  - [ ]* 2.3 Write property test for data model validation
    - **Property 9: Numeric Fields Accept Valid Values with Units**
    - **Validates: Requirements 4.4, 4.5**
  
  - [x] 2.4 Initialize doctors.json with sample data
    - Add 3-5 sample doctor records
    - Include doctorID, firstName, lastName, email, specialization
    - _Requirements: 7.1_

- [ ] 3. Implement Patient Service (backend)
  - [x] 3.1 Create patient registration endpoint (POST /api/patients/register)
    - Accept registration data (firstName, lastName, email, password)
    - Validate required fields and email format
    - Hash password using bcrypt
    - Generate unique Patient_ID (UUID)
    - Store patient record in patients.json file
    - Return Patient_ID and success message
    - _Requirements: 1.1, 1.2_
  
  - [ ]* 3.2 Write property test for patient registration
    - **Property 1: Patient Registration Creates Unique ID**
    - **Validates: Requirements 1.1**
  
  - [ ]* 3.3 Write property test for registration validation
    - **Property 2: Invalid Registration Data Rejected**
    - **Validates: Requirements 1.2**
  
  - [x] 3.4 Create patient authentication endpoint (POST /api/patients/login)
    - Accept credentials (email, password)
    - Read from patients.json and validate credentials
    - Generate session token (JWT or similar)
    - Return session token and patient info
    - _Requirements: 2.1, 2.2_
  
  - [ ]* 3.5 Write property test for authentication
    - **Property 3: Valid Credentials Grant Access**
    - **Property 4: Invalid Credentials Rejected**
    - **Validates: Requirements 2.1, 2.2**
  
  - [x] 3.6 Create patient history endpoint (GET /api/patients/{patient_id}/history)
    - Require authentication (validate session token)
    - Read assessments.json and filter by patient_id
    - Read prescriptions.json and match with assessments
    - Return formatted history data
    - _Requirements: 2.3, 3.1, 3.2, 3.3_
  
  - [ ]* 3.7 Write property test for patient history retrieval
    - **Property 5: Patient History Retrieval Completeness**
    - **Property 6: History Display Contains Required Fields**
    - **Validates: Requirements 3.1, 3.3**

- [~] 4. Checkpoint - Ensure patient service tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 5. Implement Assessment Service (backend)
  - [x] 5.1 Create assessment submission endpoint (POST /api/assessments)
    - Accept assessment data (patientID, weight, height, age, symptoms)
    - Validate required fields and numeric values
    - Validate weight/height units (kg/lbs, cm/inches)
    - Generate unique assessment_ID (UUID)
    - Store assessment in assessments.json file
    - Return assessment_ID
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_
  
  - [ ]* 5.2 Write property test for assessment validation
    - **Property 7: Incomplete Assessment Data Rejected**
    - **Property 8: Valid Assessment Data Persisted**
    - **Validates: Requirements 4.2, 4.3**
  
  - [~] 5.3 Create assessment retrieval endpoint (GET /api/assessments/{assessment_id})
    - Require authentication
    - Read from assessments.json and find by assessment_id
    - Include follow-up responses if present
    - _Requirements: 4.3_

- [ ] 6. Implement Follow-up Question Engine (backend)
  - [~] 6.1 Create symptom-to-question mapping rules
    - Define dictionary of symptoms to follow-up questions
    - Include common symptoms (headache, fever, cough, fatigue, etc.)
    - Each symptom maps to 3-5 relevant questions
    - _Requirements: 5.1_
  
  - [~] 6.2 Create follow-up questions endpoint (POST /api/assessments/{assessment_id}/followup-questions)
    - Accept symptoms list from assessment
    - Match symptoms to question rules
    - Return relevant follow-up questions
    - _Requirements: 5.1, 5.3_
  
  - [ ]* 6.3 Write property test for follow-up question generation
    - **Property 10: Symptoms Generate Follow-up Questions**
    - **Validates: Requirements 5.1**
  
  - [~] 6.4 Create follow-up responses endpoint (POST /api/assessments/{assessment_id}/followup-responses)
    - Accept follow-up responses
    - Read assessments.json, find assessment by ID
    - Update assessment with follow-up responses
    - Write back to assessments.json
    - _Requirements: 5.2_
  
  - [ ]* 6.5 Write property test for follow-up response storage
    - **Property 11: Follow-up Responses Stored with Assessment**
    - **Validates: Requirements 5.2**

- [ ] 7. Implement Prescription Service (backend)
  - [~] 7.1 Create symptom-to-medication mapping rules
    - Define dictionary of symptoms to medications
    - Include medication name, dosage, frequency, duration
    - Add general instructions templates
    - _Requirements: 6.1, 6.2_
  
  - [x] 7.2 Create prescription generation endpoint (POST /api/prescriptions/generate)
    - Accept assessment_ID
    - Read assessment data from assessments.json
    - Match symptoms to medication rules
    - Generate prescription with medications
    - Generate unique prescription_ID (UUID)
    - Store prescription in prescriptions.json file
    - Return prescription details
    - _Requirements: 6.1, 6.2, 6.3_
  
  - [ ]* 7.3 Write property test for prescription generation
    - **Property 12: Assessment Completion Generates Prescription**
    - **Property 13: Prescription Contains Required Fields**
    - **Validates: Requirements 6.1, 6.2**
  
  - [~] 7.4 Create prescription retrieval endpoint (GET /api/prescriptions/patient/{patient_id})
    - Require authentication (doctor or patient)
    - Read prescriptions.json and filter by patient_id
    - Read assessments.json to include assessment data
    - Return prescriptions with assessment data and symptoms
    - _Requirements: 9.1, 9.2, 9.3_
  
  - [ ]* 7.5 Write property test for prescription retrieval
    - **Property 17: Valid Patient ID Retrieves All Prescriptions**
    - **Property 18: Invalid Patient ID Returns Error**
    - **Property 19: Prescription Display Contains Complete Information**
    - **Validates: Requirements 9.1, 9.2, 9.3**

- [~] 8. Checkpoint - Ensure assessment and prescription services tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 9. Implement Doctor Assignment Service (backend)
  - [x] 9.1 Create doctor assignment endpoint (POST /api/assignments)
    - Accept assessment_ID and patient_ID
    - Read doctors.json and select a doctor (random or round-robin)
    - Generate unique Token_ID (UUID)
    - Store assignment in assignments.json file
    - Return doctor info and Token_ID
    - _Requirements: 7.1, 7.2, 7.3_
  
  - [ ]* 9.2 Write property test for doctor assignment
    - **Property 14: Assessment Completion Assigns Doctor**
    - **Property 15: Token ID Uniqueness**
    - **Validates: Requirements 7.1, 7.2**

- [ ] 10. Implement Doctor Portal endpoints (backend)
  - [~] 10.1 Create doctor authentication endpoint (POST /api/doctors/login)
    - Accept doctor credentials
    - Read from doctors.json and validate credentials
    - Generate session token
    - Return token and doctor info
    - _Requirements: 8.2_
  
  - [ ]* 10.2 Write property test for doctor authentication
    - **Property 16: Doctor Authentication Grants Prescription Access**
    - **Validates: Requirements 8.2**
  
  - [~] 10.3 Ensure prescription retrieval endpoint supports doctor access
    - Verify doctor authentication in prescription retrieval
    - Allow doctors to access any patient's prescriptions
    - _Requirements: 9.1, 9.2, 9.3_

- [ ] 11. Implement data persistence verification (backend)
  - [ ]* 11.1 Write property test for immediate data retrieval
    - **Property 20: Data Persistence Immediate Retrieval**
    - **Validates: Requirements 10.1, 10.3**

- [ ] 12. Implement Patient Portal UI (React frontend)
  - [x] 12.1 Create registration page component
    - Form with firstName, lastName, email, password fields
    - Client-side validation
    - Call registration API endpoint
    - Display success/error messages
    - Redirect to login on success
    - _Requirements: 1.1, 1.2, 1.3_
  
  - [x] 12.2 Create login page component
    - Form with email and password fields
    - Call authentication API endpoint
    - Store session token in localStorage or context
    - Redirect to dashboard on success
    - Display error messages for invalid credentials
    - _Requirements: 2.1, 2.2_
  
  - [x] 12.3 Create patient dashboard component
    - Display patient name and welcome message
    - Show patient history (previous assessments)
    - Button to start new assessment
    - Display assessment dates, symptoms, prescriptions
    - _Requirements: 2.3, 3.1, 3.2, 3.3_
  
  - [x] 12.4 Create health assessment form component
    - Form fields for weight (with unit selector), height (with unit selector), age, symptoms
    - Client-side validation for required fields
    - Call assessment submission API
    - Display validation errors
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_
  
  - [~] 12.5 Create follow-up questions component
    - Display follow-up questions based on symptoms
    - Text input or radio buttons for responses
    - Call follow-up responses API
    - _Requirements: 5.1, 5.2, 5.3_
  
  - [~] 12.6 Create prescription display component
    - Show generated prescription details
    - Display medications with dosages and instructions
    - Show assigned doctor name and Token_ID
    - Option to return to dashboard
    - _Requirements: 6.1, 6.2, 7.1, 7.2, 7.3_

- [ ] 13. Implement Doctor Portal UI (React frontend)
  - [~] 13.1 Create doctor login page component
    - Form with email and password fields
    - Call doctor authentication API
    - Store session token
    - Redirect to doctor dashboard
    - _Requirements: 8.1, 8.2_
  
  - [~] 13.2 Create doctor dashboard component
    - Input field for Patient_ID
    - Search button to retrieve prescriptions
    - Display prescription results
    - Show assessment data, symptoms, follow-up responses, prescription details
    - Handle "patient not found" errors
    - _Requirements: 8.1, 9.1, 9.2, 9.3_

- [ ] 14. Implement routing and navigation (React frontend)
  - [x] 14.1 Set up React Router
    - Define routes for patient registration, login, dashboard, assessment
    - Define routes for doctor login and dashboard
    - Implement protected routes (require authentication)
    - _Requirements: All UI requirements_
  
  - [~] 14.2 Create navigation components
    - Header with logout button
    - Navigation between patient portal sections
    - Separate navigation for doctor portal
    - _Requirements: All UI requirements_

- [ ] 15. Implement complete patient flow integration
  - [~] 15.1 Wire together patient registration → login → assessment → prescription flow
    - Ensure data flows correctly through all steps
    - Test new patient journey end-to-end
    - Handle errors gracefully at each step
    - _Requirements: 1.1, 1.2, 1.3, 2.1, 4.1, 4.3, 5.1, 5.2, 6.1, 7.1_
  
  - [~] 15.2 Wire together existing patient login → assessment → prescription flow
    - Ensure patient history displays correctly
    - Test existing patient journey end-to-end
    - _Requirements: 2.1, 2.3, 3.1, 4.1, 6.1, 7.1_
  
  - [ ]* 15.3 Write integration tests for patient flows
    - Test complete new patient flow
    - Test complete existing patient flow
    - _Requirements: 1.1, 2.1, 4.1, 6.1, 7.1_

- [ ] 16. Implement complete doctor flow integration
  - [~] 16.1 Wire together doctor login → prescription retrieval flow
    - Ensure doctor can access portal
    - Test prescription retrieval by Patient_ID
    - Handle invalid Patient_ID gracefully
    - _Requirements: 8.1, 8.2, 9.1, 9.2, 9.3_
  
  - [ ]* 16.2 Write integration tests for doctor flow
    - Test doctor authentication and prescription retrieval
    - _Requirements: 8.2, 9.1_

- [~] 17. Checkpoint - Ensure all integration tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 18. Add responsive design and UI polish
  - [~] 18.1 Add CSS styling for all components
    - Create consistent color scheme and typography
    - Style forms, buttons, and navigation
    - Add loading spinners for API calls
    - _Requirements: 11.1, 11.2, 11.3_
  
  - [~] 18.2 Implement responsive design
    - Use CSS media queries or responsive framework
    - Test on desktop and mobile viewports
    - Ensure forms are usable on mobile devices
    - _Requirements: 11.1, 11.2_
  
  - [~] 18.3 Add form validation feedback
    - Display inline validation errors
    - Highlight invalid fields
    - Show success messages
    - _Requirements: 11.3_

- [ ] 19. Create README.md documentation
  - [x] 19.1 Write README.md file
    - Project overview and features
    - Architecture description (React frontend + Python backend)
    - Setup instructions (install dependencies, database setup)
    - Running instructions (start backend server, start frontend dev server)
    - API endpoint documentation
    - Testing instructions
    - Technology stack details
    - _Requirements: 12.1, 12.2, 12.3_

- [ ] 20. Final testing and bug fixes
  - [ ]* 20.1 Run all property-based tests
    - Execute all property tests with 100+ iterations
    - Fix any failing tests
    - _Requirements: All testable requirements_
  
  - [ ]* 20.2 Run all unit and integration tests
    - Execute full test suite
    - Fix any failing tests
    - _Requirements: All requirements_
  
  - [~] 20.3 Manual testing of complete user flows
    - Test new patient registration and assessment flow
    - Test existing patient login and assessment flow
    - Test doctor portal prescription retrieval
    - Test error handling and edge cases
    - _Requirements: All requirements_

- [~] 21. Final checkpoint - System ready for use
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Backend uses Python (Flask/FastAPI) with JSON files for data storage
- Frontend uses React with React Router for navigation
- Data is stored in JSON files: patients.json, assessments.json, prescriptions.json, doctors.json, assignments.json
- JSON file storage can be migrated to SQL Server later without changing API contracts
- Property-based tests use Hypothesis (Python) and fast-check (TypeScript/JavaScript)
- Integration tests verify end-to-end flows work correctly
- The system generates dummy prescriptions for demonstration purposes only
