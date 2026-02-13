# Requirements Document

## Introduction

The Patient Assessment System is a healthcare web application that enables patients to register, complete health assessments, and receive dummy prescriptions with doctor assignments. The system provides separate portals for patients and doctors, facilitating the collection of health information and prescription management.

## Glossary

- **Patient**: A user who registers, signs in, and completes health assessments
- **Patient_ID**: Unique identifier assigned to each patient upon registration
- **Health_Assessment**: A form collecting patient health information including weight, height, age, and symptoms
- **Dummy_Prescription**: A generated prescription based on patient assessment data (for demonstration purposes)
- **Token_ID**: Unique identifier generated for a patient visit with an assigned doctor
- **Doctor**: A healthcare provider who accesses the doctor portal to view patient prescriptions
- **Doctor_Portal**: Interface for doctors to retrieve patient prescriptions by Patient_ID
- **Patient_Portal**: Interface for patients to register, sign in, and complete assessments
- **System**: The Patient Assessment System application

## Requirements

### Requirement 1: Patient Registration

**User Story:** As a new patient, I want to register in the system, so that I can access health assessment services.

#### Acceptance Criteria

1. WHEN a new user provides registration information, THE System SHALL create a unique Patient_ID and store the patient record
2. WHEN a user attempts to register with incomplete information, THE System SHALL reject the registration and display validation errors
3. WHEN a patient completes registration, THE System SHALL confirm successful registration and provide sign-in access

### Requirement 2: Patient Authentication

**User Story:** As a patient, I want to sign in to the system, so that I can access my health assessment forms.

#### Acceptance Criteria

1. WHEN a patient provides valid credentials, THE System SHALL authenticate the patient and grant access to the Patient_Portal
2. WHEN a patient provides invalid credentials, THE System SHALL reject the sign-in attempt and display an error message
3. WHEN a patient successfully signs in, THE System SHALL retrieve and display the patient's history based on Patient_ID

### Requirement 3: Patient History Retrieval

**User Story:** As a patient, I want to view my previous health assessments, so that I can track my health history.

#### Acceptance Criteria

1. WHEN a patient signs in, THE System SHALL retrieve all historical health assessments associated with the Patient_ID
2. WHEN a patient has no previous assessments, THE System SHALL display an appropriate message indicating no history exists
3. WHEN displaying patient history, THE System SHALL show assessment dates, symptoms, and associated prescriptions

### Requirement 4: Health Assessment Form

**User Story:** As a patient, I want to complete a health assessment form, so that I can receive medical guidance.

#### Acceptance Criteria

1. WHEN a patient accesses the health assessment form, THE System SHALL display fields for current weight, current height, age, and current issues/symptoms
2. WHEN a patient submits the form with missing required fields, THE System SHALL prevent submission and display validation errors
3. WHEN a patient submits a complete health assessment, THE System SHALL store the assessment data associated with the Patient_ID
4. WHEN a patient enters weight, THE System SHALL accept numeric values with appropriate units
5. WHEN a patient enters height, THE System SHALL accept numeric values with appropriate units

### Requirement 5: Intelligent Follow-up Questions

**User Story:** As a patient, I want to receive relevant follow-up questions based on my symptoms, so that I can provide more detailed health information.

#### Acceptance Criteria

1. WHEN a patient describes specific symptoms, THE System SHALL generate and display relevant follow-up questions
2. WHEN a patient answers follow-up questions, THE System SHALL store the responses with the health assessment
3. WHEN no specific symptoms are identified, THE System SHALL proceed without additional follow-up questions

### Requirement 6: Dummy Prescription Generation

**User Story:** As a patient, I want to receive a prescription based on my assessment, so that I know what treatment is recommended.

#### Acceptance Criteria

1. WHEN a patient completes a health assessment, THE System SHALL generate a Dummy_Prescription based on the assessment data
2. WHEN generating a prescription, THE System SHALL include medication names, dosages, and instructions
3. WHEN a prescription is generated, THE System SHALL associate it with the Patient_ID and store it in the system

### Requirement 7: Doctor Assignment and Token Generation

**User Story:** As a patient, I want to be assigned a doctor and receive a visit token, so that I can schedule my appointment.

#### Acceptance Criteria

1. WHEN a patient completes a health assessment, THE System SHALL assign a doctor to the patient
2. WHEN a doctor is assigned, THE System SHALL generate a unique Token_ID for the patient visit
3. WHEN a Token_ID is generated, THE System SHALL display it to the patient and store it with the assessment record

### Requirement 8: Doctor Portal Access

**User Story:** As a doctor, I want to access a dedicated portal, so that I can view patient prescriptions.

#### Acceptance Criteria

1. WHEN a doctor accesses the Doctor_Portal, THE System SHALL display an interface for entering Patient_ID
2. WHEN a doctor is authenticated, THE System SHALL grant access to patient prescription retrieval functionality

### Requirement 9: Prescription Retrieval by Doctor

**User Story:** As a doctor, I want to retrieve patient prescriptions by Patient_ID, so that I can review patient treatment plans.

#### Acceptance Criteria

1. WHEN a doctor enters a valid Patient_ID, THE System SHALL retrieve and display all Dummy_Prescriptions associated with that Patient_ID
2. WHEN a doctor enters an invalid Patient_ID, THE System SHALL display an error message indicating the patient was not found
3. WHEN displaying prescriptions, THE System SHALL show assessment data, symptoms, follow-up responses, and prescription details

### Requirement 10: Data Persistence

**User Story:** As a system administrator, I want all patient data to be persisted, so that information is available across sessions.

#### Acceptance Criteria

1. WHEN patient data is created or updated, THE System SHALL persist the data to storage immediately
2. WHEN the system restarts, THE System SHALL retain all previously stored patient records, assessments, and prescriptions
3. WHEN data is retrieved, THE System SHALL return the most current version of the requested information

### Requirement 11: User Interface Responsiveness

**User Story:** As a user, I want the application to be responsive, so that I can access it from different devices.

#### Acceptance Criteria

1. WHEN a user accesses the application from a desktop browser, THE System SHALL display a properly formatted interface
2. WHEN a user accesses the application from a mobile device, THE System SHALL adapt the interface to the screen size
3. WHEN a user interacts with forms, THE System SHALL provide immediate visual feedback for validation errors

### Requirement 12: Documentation

**User Story:** As a developer, I want comprehensive documentation, so that I can understand how to set up and use the system.

#### Acceptance Criteria

1. THE System SHALL include a README.md file with setup instructions
2. WHEN a developer reads the README, THE System documentation SHALL explain the application architecture and features
3. WHEN a developer reads the README, THE System documentation SHALL provide instructions for running the application locally
