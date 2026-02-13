# Patient Assessment System - Architecture Diagram

## System Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          PATIENT ASSESSMENT SYSTEM                           │
│                     AI-Powered Healthcare Management Platform                │
└─────────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────────┐
│                              FRONTEND LAYER                                    │
│                           (React + Vite + CSS)                                 │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │   Register   │  │    Login     │  │   Patient    │  │    Doctor    │    │
│  │     Page     │  │     Page     │  │  Dashboard   │  │  Dashboard   │    │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘    │
│         │                 │                  │                  │             │
│         │                 │                  │                  │             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                       │
│  │  Assessment  │  │   App.jsx    │  │   Routing    │                       │
│  │     Page     │  │  (Main App)  │  │  Component   │                       │
│  └──────────────┘  └──────────────┘  └──────────────┘                       │
│                                                                                │
└────────────────────────────────┬──────────────────────────────────────────────┘
                                 │
                                 │ HTTP/HTTPS (REST API)
                                 │ JSON Payloads
                                 │
┌────────────────────────────────▼──────────────────────────────────────────────┐
│                              BACKEND LAYER                                     │
│                         (Flask + Python + CORS)                                │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                                │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │                          API ENDPOINTS                                   │ │
│  ├─────────────────────────────────────────────────────────────────────────┤ │
│  │  POST /api/patients/register    - Patient Registration                  │ │
│  │  POST /api/login                 - Unified Login (Patient/Doctor)       │ │
│  │  POST /api/assessments           - Create Health Assessment             │ │
│  │  GET  /api/patients/{id}/history - Get Patient History                  │ │
│  │  GET  /api/doctors/patients      - Get Doctor's Patients                │ │
│  │  PUT  /api/prescriptions/{id}    - Update Prescription                  │ │
│  │  GET  /api/health                - Health Check                         │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                                │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │                       CORE SERVICES                                      │ │
│  ├─────────────────────────────────────────────────────────────────────────┤ │
│  │                                                                          │ │
│  │  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐     │ │
│  │  │  Authentication  │  │   Bedrock AI     │  │  Data Access     │     │ │
│  │  │     Service      │  │     Service      │  │     Layer        │     │ │
│  │  │                  │  │                  │  │                  │     │ │
│  │  │  • JWT Tokens    │  │  • Claude 3      │  │  • CRUD Ops      │     │ │
│  │  │  • bcrypt Hash   │  │  • Prescription  │  │  • File Locking  │     │ │
│  │  │  • User Types    │  │    Generation    │  │  • JSON Storage  │     │ │
│  │  │  • Validation    │  │  • Fallback      │  │  • ID Generation │     │ │
│  │  └──────────────────┘  └──────────────────┘  └──────────────────┘     │ │
│  │                                                                          │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                                │
└────────────────────────────────┬──────────────────────────────────────────────┘
                                 │
                    ┌────────────┴────────────┐
                    │                         │
                    ▼                         ▼
┌───────────────────────────────┐  ┌──────────────────────────────────────────┐
│      DATA STORAGE LAYER       │  │        EXTERNAL SERVICES                 │
│      (JSON File System)       │  │        (AWS Bedrock)                     │
├───────────────────────────────┤  ├──────────────────────────────────────────┤
│                               │  │                                          │
│  ┌─────────────────────────┐ │  │  ┌────────────────────────────────────┐ │
│  │   patients.json         │ │  │  │   Amazon Bedrock                   │ │
│  │   • Patient Records     │ │  │  │   ┌──────────────────────────────┐ │ │
│  │   • Credentials         │ │  │  │   │  Claude 3 Sonnet             │ │ │
│  │   • Registration Data   │ │  │  │   │  (AI Model)                  │ │ │
│  └─────────────────────────┘ │  │  │   │                              │ │ │
│                               │  │  │   │  • Symptom Analysis          │ │ │
│  ┌─────────────────────────┐ │  │  │   │  • Medication Suggestions    │ │ │
│  │   doctors.json          │ │  │  │   │  • Dosage Recommendations    │ │ │
│  │   • Doctor Profiles     │ │  │  │   │  • Instructions Generation   │ │ │
│  │   • Specializations     │ │  │  │   └──────────────────────────────┘ │ │
│  │   • Credentials         │ │  │  │                                      │ │
│  └─────────────────────────┘ │  │  │   Fallback: Rule-based System       │ │
│                               │  │  └────────────────────────────────────┘ │
│  ┌─────────────────────────┐ │  │                                          │
│  │   assessments.json      │ │  └──────────────────────────────────────────┘
│  │   • Health Assessments  │ │
│  │   • Symptoms            │ │
│  │   • Vitals (Age/Wt/Ht)  │ │
│  └─────────────────────────┘ │
│                               │
│  ┌─────────────────────────┐ │
│  │   prescriptions.json    │ │
│  │   • AI Prescriptions    │ │
│  │   • Medications         │ │
│  │   • Instructions        │ │
│  └─────────────────────────┘ │
│                               │
│  ┌─────────────────────────┐ │
│  │   assignments.json      │ │
│  │   • Doctor Assignments  │ │
│  │   • Token IDs           │ │
│  │   • Assignment Dates    │ │
│  └─────────────────────────┘ │
│                               │
└───────────────────────────────┘


## User Flow Diagrams

### 1. Patient Registration & Assessment Flow

```
┌─────────┐
│ Patient │
└────┬────┘
     │
     │ 1. Register
     ▼
┌─────────────────┐
│ Register Page   │
│ • First Name    │
│ • Last Name     │
│ • Email         │
│ • Password      │
└────┬────────────┘
     │
     │ POST /api/patients/register
     ▼
┌─────────────────┐
│  Backend API    │
│ • Validate      │
│ • Hash Password │
│ • Generate ID   │
│ • Store Patient │
└────┬────────────┘
     │
     │ 2. Login
     ▼
┌─────────────────┐
│   Login Page    │
│ • Email         │
│ • Password      │
└────┬────────────┘
     │
     │ POST /api/login
     ▼
┌─────────────────┐
│  Backend API    │
│ • Verify Creds  │
│ • Generate JWT  │
│ • Return Token  │
└────┬────────────┘
     │
     │ 3. Create Assessment
     ▼
┌─────────────────┐
│ Assessment Page │
│ • Weight        │
│ • Height        │
│ • Age           │
│ • Symptoms      │
└────┬────────────┘
     │
     │ POST /api/assessments
     │ (with JWT token)
     ▼
┌─────────────────────────────────┐
│       Backend Processing        │
│                                 │
│  1. Validate Token              │
│  2. Store Assessment            │
│  3. Call Bedrock AI ──────────┐ │
│  4. Generate Prescription      │ │
│  5. Assign Doctor              │ │
│  6. Return Results             │ │
└────┬────────────────────────────┘ │
     │                              │
     │                              │
     │                    ┌─────────▼──────────┐
     │                    │   AWS Bedrock      │
     │                    │   Claude 3 Sonnet  │
     │                    │                    │
     │                    │ Analyzes symptoms  │
     │                    │ Generates meds     │
     │                    │ Creates dosage     │
     │                    └─────────┬──────────┘
     │                              │
     │ 4. View Results              │
     ▼                              │
┌─────────────────────────────────┐ │
│    Patient Dashboard            │ │
│                                 │ │
│  ┌───────────────────────────┐ │ │
│  │  Assessment History       │ │ │
│  │  • Date                   │ │ │
│  │  • Symptoms               │ │ │
│  │  • Vitals                 │ │ │
│  └───────────────────────────┘ │ │
│                                 │ │
│  ┌───────────────────────────┐ │ │
│  │  AI Prescription ◄────────┼─┘
│  │  • Medications            │
│  │  • Dosage                 │
│  │  • Instructions           │
│  └───────────────────────────┘
│
│  ┌───────────────────────────┐
│  │  Doctor Assignment        │
│  │  • Doctor Name            │
│  │  • Token ID               │
│  │  • Specialization         │
│  └───────────────────────────┘
│
└─────────────────────────────────┘
```


### 2. Doctor Dashboard Flow

```
┌─────────┐
│ Doctor  │
└────┬────┘
     │
     │ 1. Login
     ▼
┌─────────────────┐
│   Login Page    │
│ • Email         │
│ • Password      │
└────┬────────────┘
     │
     │ POST /api/login
     ▼
┌─────────────────┐
│  Backend API    │
│ • Verify Doctor │
│ • Generate JWT  │
│ • userType:     │
│   "doctor"      │
└────┬────────────┘
     │
     │ 2. View Patients
     ▼
┌─────────────────────────────────────────────────────────────┐
│              Doctor Dashboard                                │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Patient List                                          │ │
│  │                                                        │ │
│  │  ┌──────────────────────────────────────────────────┐ │ │
│  │  │ Patient: John Doe                                │ │ │
│  │  │ Email: john@example.com                          │ │ │
│  │  │ Assessments: 3                                   │ │ │
│  │  │                                                  │ │ │
│  │  │ [▼ View History]                                 │ │ │
│  │  │                                                  │ │ │
│  │  │ ┌──────────────────────────────────────────────┐│ │ │
│  │  │ │ Assessment #1 - 2024-01-20                   ││ │ │
│  │  │ │ Symptoms: Headache, Fever                    ││ │ │
│  │  │ │ Vitals: 70kg, 175cm, Age 30                  ││ │ │
│  │  │ │                                              ││ │ │
│  │  │ │ Prescription:                                ││ │ │
│  │  │ │ • Ibuprofen 200mg - Every 6 hours           ││ │ │
│  │  │ │ • Paracetamol 500mg - Every 8 hours         ││ │ │
│  │  │ │                                              ││ │ │
│  │  │ │ [Edit Prescription]                          ││ │ │
│  │  │ └──────────────────────────────────────────────┘│ │ │
│  │  │                                                  │ │ │
│  │  │ ┌──────────────────────────────────────────────┐│ │ │
│  │  │ │ Assessment #2 - 2024-01-15                   ││ │ │
│  │  │ │ ...                                          ││ │ │
│  │  │ └──────────────────────────────────────────────┘│ │ │
│  │  └──────────────────────────────────────────────────┘ │ │
│  │                                                        │ │
│  │  ┌──────────────────────────────────────────────────┐ │ │
│  │  │ Patient: Jane Smith                              │ │ │
│  │  │ ...                                              │ │ │
│  │  └──────────────────────────────────────────────────┘ │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
└─────────────────────────────────────────────────────────────┘
     │
     │ 3. Edit Prescription
     ▼
┌─────────────────┐
│  Backend API    │
│ PUT /api/       │
│ prescriptions/  │
│ {id}            │
│                 │
│ • Validate JWT  │
│ • Check Doctor  │
│ • Update Rx     │
│ • Log Changes   │
└─────────────────┘
```


## Security Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      SECURITY LAYERS                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. AUTHENTICATION                                               │
│     ┌──────────────────────────────────────────────────────┐   │
│     │  • JWT Token-based Authentication                    │   │
│     │  • 24-hour Token Expiry                              │   │
│     │  • bcrypt Password Hashing (12 rounds)               │   │
│     │  • SECRET_KEY from Environment Variables             │   │
│     │  • User Type Validation (patient/doctor)             │   │
│     └──────────────────────────────────────────────────────┘   │
│                                                                  │
│  2. AUTHORIZATION                                                │
│     ┌──────────────────────────────────────────────────────┐   │
│     │  • Role-based Access Control (RBAC)                  │   │
│     │  • Patients: Own data only                           │   │
│     │  • Doctors: Assigned patients only                   │   │
│     │  • Token validation on every request                 │   │
│     │  • Endpoint-level permission checks                  │   │
│     └──────────────────────────────────────────────────────┘   │
│                                                                  │
│  3. DATA PROTECTION                                              │
│     ┌──────────────────────────────────────────────────────┐   │
│     │  • Passwords never stored in plain text              │   │
│     │  • Passwords never returned in API responses         │   │
│     │  • Email normalization (lowercase)                   │   │
│     │  • Input validation and sanitization                 │   │
│     │  • File locking for concurrent access                │   │
│     └──────────────────────────────────────────────────────┘   │
│                                                                  │
│  4. ENVIRONMENT SECURITY                                         │
│     ┌──────────────────────────────────────────────────────┐   │
│     │  • .env files in .gitignore                          │   │
│     │  • No hardcoded secrets in code                      │   │
│     │  • AWS credentials via environment variables         │   │
│     │  • Separate dev/prod configurations                  │   │
│     └──────────────────────────────────────────────────────┘   │
│                                                                  │
│  5. API SECURITY                                                 │
│     ┌──────────────────────────────────────────────────────┐   │
│     │  • CORS enabled for frontend                         │   │
│     │  • Bearer token in Authorization header              │   │
│     │  • Input validation on all endpoints                 │   │
│     │  • Error messages don't leak sensitive info          │   │
│     └──────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow Diagram

```
┌──────────────────────────────────────────────────────────────────────┐
│                    PRESCRIPTION GENERATION FLOW                       │
└──────────────────────────────────────────────────────────────────────┘

Patient Symptoms Input
         │
         ▼
┌─────────────────────┐
│  Frontend Collects  │
│  • Symptoms         │
│  • Weight           │
│  • Height           │
│  • Age              │
└──────────┬──────────┘
           │
           │ POST /api/assessments
           │ Authorization: Bearer {JWT}
           ▼
┌─────────────────────────────┐
│  Backend Validation         │
│  1. Verify JWT Token        │
│  2. Check Patient ID Match  │
│  3. Validate Input Data     │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│  Store Assessment           │
│  • Generate Assessment ID   │
│  • Save to assessments.json │
│  • Timestamp                │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────────────────┐
│  Call Bedrock AI Service                │
│                                         │
│  bedrock_service.generate_prescription( │
│    symptoms=['headache', 'fever'],      │
│    age=30,                              │
│    weight=70,                           │
│    weight_unit='kg',                    │
│    height=175,                          │
│    height_unit='cm'                     │
│  )                                      │
└──────────┬──────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────┐
│  AWS Bedrock Processing                 │
│                                         │
│  Claude 3 Sonnet Analyzes:              │
│  • Symptom patterns                     │
│  • Patient demographics                 │
│  • Medical best practices               │
│                                         │
│  Generates:                             │
│  • Medication list                      │
│  • Dosage recommendations               │
│  • Frequency instructions               │
│  • Duration                             │
│  • Special instructions                 │
└──────────┬──────────────────────────────┘
           │
           │ If Bedrock fails
           ├──────────────────────────────┐
           │                              │
           ▼                              ▼
┌─────────────────────┐      ┌─────────────────────┐
│  AI Response        │      │  Fallback System    │
│  {                  │      │  Rule-based Logic   │
│    medications: [   │      │  • Fever → Tylenol  │
│      {              │      │  • Pain → Ibuprofen │
│        name: "...", │      │  • Generic dosages  │
│        dosage: "...",│      └─────────────────────┘
│        frequency: "",│
│        duration: "" │
│      }              │
│    ],               │
│    instructions: "" │
│  }                  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────────────┐
│  Store Prescription         │
│  • Generate Prescription ID │
│  • Link to Assessment       │
│  • Save to prescriptions.json│
│  • Mark as AI-generated     │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│  Assign Doctor              │
│  • Select available doctor  │
│  • Generate Token ID        │
│  • Save to assignments.json │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│  Return Complete Response   │
│  {                          │
│    assessment: {...},       │
│    prescription: {...},     │
│    doctorAssignment: {...}  │
│  }                          │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│  Frontend Displays          │
│  • Prescription details     │
│  • Doctor assignment        │
│  • Token for tracking       │
└─────────────────────────────┘
```


## Technology Stack

```
┌─────────────────────────────────────────────────────────────────────┐
│                         TECHNOLOGY STACK                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  FRONTEND                                                            │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │  • React 18.x          - UI Framework                          │ │
│  │  • Vite               - Build Tool & Dev Server                │ │
│  │  • React Router       - Client-side Routing                    │ │
│  │  • CSS3               - Styling                                │ │
│  │  • Fetch API          - HTTP Requests                          │ │
│  │  • localStorage       - Token Storage                          │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                                                                      │
│  BACKEND                                                             │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │  • Python 3.x         - Programming Language                   │ │
│  │  • Flask              - Web Framework                          │ │
│  │  • Flask-CORS         - Cross-Origin Resource Sharing          │ │
│  │  • bcrypt             - Password Hashing                       │ │
│  │  • PyJWT              - JWT Token Generation                   │ │
│  │  • boto3              - AWS SDK for Python                     │ │
│  │  • python-dotenv      - Environment Variable Management        │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                                                                      │
│  AI/ML                                                               │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │  • AWS Bedrock        - AI Service Platform                    │ │
│  │  • Claude 3 Sonnet    - Large Language Model                   │ │
│  │  • Anthropic API      - Model Interface                        │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                                                                      │
│  DATA STORAGE                                                        │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │  • JSON Files         - Current Storage (MVP)                  │ │
│  │  • File Locking       - Concurrency Control                    │ │
│  │  • Future: SQL Server - Planned Migration                      │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                                                                      │
│  TESTING                                                             │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │  • pytest             - Testing Framework                      │ │
│  │  • pytest fixtures    - Test Setup/Teardown                    │ │
│  │  • Unit Tests         - 52 tests, 100% pass rate               │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                                                                      │
│  DEVELOPMENT TOOLS                                                   │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │  • Git                - Version Control                        │ │
│  │  • npm/pip            - Package Management                     │ │
│  │  • VS Code            - IDE                                    │ │
│  │  • Postman            - API Testing                            │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

## Deployment Architecture (Future)

```
┌─────────────────────────────────────────────────────────────────────┐
│                      PRODUCTION DEPLOYMENT                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │                         USERS                                  │ │
│  │              (Patients & Doctors)                              │ │
│  └──────────────────────────┬─────────────────────────────────────┘ │
│                             │                                        │
│                             │ HTTPS                                  │
│                             ▼                                        │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │                    LOAD BALANCER                               │ │
│  │                  (AWS ALB / Nginx)                             │ │
│  └──────────────────────────┬─────────────────────────────────────┘ │
│                             │                                        │
│              ┌──────────────┴──────────────┐                        │
│              │                             │                        │
│              ▼                             ▼                        │
│  ┌─────────────────────┐       ┌─────────────────────┐            │
│  │  Frontend Server    │       │  Backend Server     │            │
│  │  (Static Files)     │       │  (Flask API)        │            │
│  │                     │       │                     │            │
│  │  • React Build      │       │  • Python App       │            │
│  │  • Nginx/S3         │       │  • Gunicorn/uWSGI   │            │
│  │  • CDN (CloudFront) │       │  • Auto-scaling     │            │
│  └─────────────────────┘       └──────────┬──────────┘            │
│                                            │                        │
│                             ┌──────────────┴──────────────┐        │
│                             │                             │        │
│                             ▼                             ▼        │
│              ┌─────────────────────┐       ┌─────────────────────┐│
│              │   SQL Server DB     │       │   AWS Bedrock       ││
│              │   (Azure/AWS RDS)   │       │   (Claude 3)        ││
│              │                     │       │                     ││
│              │  • Patient Data     │       │  • AI Processing    ││
│              │  • Assessments      │       │  • Prescriptions    ││
│              │  • Prescriptions    │       │                     ││
│              │  • Backups          │       └─────────────────────┘│
│              └─────────────────────┘                               │
│                                                                     │
│  ┌────────────────────────────────────────────────────────────────┐│
│  │                    MONITORING & LOGGING                        ││
│  │  • CloudWatch / Application Insights                           ││
│  │  • Error Tracking (Sentry)                                     ││
│  │  • Performance Monitoring                                      ││
│  │  • Audit Logs                                                  ││
│  └────────────────────────────────────────────────────────────────┘│
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```


## API Request/Response Examples

### 1. Patient Registration

```
REQUEST:
POST /api/patients/register
Content-Type: application/json

{
  "firstName": "John",
  "lastName": "Doe",
  "email": "john.doe@example.com",
  "password": "securePassword123"
}

RESPONSE: 201 Created
{
  "message": "Patient registered successfully",
  "patientID": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "firstName": "John",
  "lastName": "Doe",
  "email": "john.doe@example.com"
}
```

### 2. Unified Login

```
REQUEST:
POST /api/login
Content-Type: application/json

{
  "email": "john.doe@example.com",
  "password": "securePassword123"
}

RESPONSE: 200 OK
{
  "message": "Authentication successful",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "userType": "patient",
  "user": {
    "userID": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "firstName": "John",
    "lastName": "Doe",
    "email": "john.doe@example.com"
  }
}
```

### 3. Create Assessment

```
REQUEST:
POST /api/assessments
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "patientID": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "weight": 70,
  "weightUnit": "kg",
  "height": 175,
  "heightUnit": "cm",
  "age": 30,
  "symptoms": ["headache", "fever", "fatigue"]
}

RESPONSE: 201 Created
{
  "message": "Assessment created successfully",
  "assessment": {
    "assessmentID": "assess-123-456",
    "assessmentDate": "2024-01-20T10:30:00Z"
  },
  "prescription": {
    "prescriptionID": "rx-789-012",
    "medications": [
      {
        "name": "Ibuprofen",
        "dosage": "200mg",
        "frequency": "Every 6 hours",
        "duration": "3 days"
      },
      {
        "name": "Paracetamol",
        "dosage": "500mg",
        "frequency": "Every 8 hours",
        "duration": "5 days"
      }
    ],
    "instructions": "Take medications with food. Rest and stay hydrated."
  },
  "doctorAssignment": {
    "doctorName": "Dr. Sarah Johnson",
    "tokenID": "token-345-678",
    "specialization": "General Practice"
  }
}
```

### 4. Get Patient History

```
REQUEST:
GET /api/patients/a1b2c3d4-e5f6-7890-abcd-ef1234567890/history
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

RESPONSE: 200 OK
{
  "patientID": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "history": [
    {
      "assessmentID": "assess-123-456",
      "assessmentDate": "2024-01-20T10:30:00Z",
      "weight": 70,
      "weightUnit": "kg",
      "height": 175,
      "heightUnit": "cm",
      "age": 30,
      "symptoms": ["headache", "fever", "fatigue"],
      "followUpResponses": [],
      "prescription": {
        "prescriptionID": "rx-789-012",
        "medications": [...],
        "instructions": "...",
        "generatedDate": "2024-01-20T10:31:00Z"
      }
    }
  ]
}
```

### 5. Doctor Get Patients

```
REQUEST:
GET /api/doctors/patients
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

RESPONSE: 200 OK
{
  "doctorID": "doc-001",
  "patientCount": 2,
  "patients": [
    {
      "patientID": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "firstName": "John",
      "lastName": "Doe",
      "email": "john.doe@example.com",
      "assessmentCount": 3,
      "history": [...]
    },
    {
      "patientID": "b2c3d4e5-f6g7-8901-bcde-fg2345678901",
      "firstName": "Jane",
      "lastName": "Smith",
      "email": "jane.smith@example.com",
      "assessmentCount": 1,
      "history": [...]
    }
  ]
}
```

### 6. Update Prescription

```
REQUEST:
PUT /api/prescriptions/rx-789-012
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "medications": [
    {
      "name": "Ibuprofen",
      "dosage": "400mg",
      "frequency": "Every 8 hours",
      "duration": "5 days"
    }
  ],
  "instructions": "Take with food. Increased dosage due to persistent symptoms."
}

RESPONSE: 200 OK
{
  "message": "Prescription updated successfully",
  "prescription": {
    "prescriptionID": "rx-789-012",
    "medications": [...],
    "instructions": "...",
    "lastModifiedBy": "doc-001",
    "lastModifiedDate": "2024-01-21T14:30:00Z"
  }
}
```

## Key Features Summary

```
┌─────────────────────────────────────────────────────────────────────┐
│                         KEY FEATURES                                 │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ✓ Patient Registration & Authentication                             │
│  ✓ Doctor Authentication                                             │
│  ✓ Unified Login System (Auto-detect user type)                     │
│  ✓ Health Assessment Creation                                        │
│  ✓ AI-Powered Prescription Generation (AWS Bedrock Claude 3)        │
│  ✓ Automatic Doctor Assignment                                       │
│  ✓ Patient History Tracking                                          │
│  ✓ Doctor Dashboard with Patient Management                          │
│  ✓ Prescription Editing by Doctors                                   │
│  ✓ JWT-based Security                                                │
│  ✓ Role-based Access Control                                         │
│  ✓ Password Hashing (bcrypt)                                         │
│  ✓ Comprehensive Test Suite (52 tests, 100% pass)                   │
│  ✓ Fallback System for AI Service                                    │
│  ✓ Responsive UI Design                                              │
│                                                                      │
│  FUTURE ENHANCEMENTS:                                                │
│  ○ Speech-to-Text Support                                            │
│  ○ Multilingual Support (AWS Translate)                              │
│  ○ SQL Server Database Migration                                     │
│  ○ Real-time Notifications                                           │
│  ○ Video Consultation                                                │
│  ○ Mobile App (React Native)                                         │
│  ○ Analytics Dashboard                                               │
│  ○ Appointment Scheduling                                            │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

**Document Version:** 1.0  
**Last Updated:** 2024  
**System Status:** Production Ready (MVP)
