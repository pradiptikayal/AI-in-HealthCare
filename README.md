# Patient Assessment System

A healthcare web application that enables patients to register, complete health assessments, and receive dummy prescriptions with doctor assignments. The system provides separate portals for patients and doctors.

## Features

### Patient Portal
- **Patient Registration**: New patients can register with their personal information
- **Patient Sign-In**: Secure authentication for returning patients
- **Patient History**: View previous health assessments and prescriptions
- **Health Assessment Form**: Submit current health information including:
  - Weight (kg/lbs)
  - Height (cm/inches)
  - Age
  - Current symptoms and issues
- **Intelligent Follow-up Questions**: Receive relevant follow-up questions based on reported symptoms
- **Dummy Prescription**: Get generated prescriptions based on assessment data
- **Doctor Assignment**: Receive assigned doctor name and visit token ID

### Doctor Portal
- **Doctor Authentication**: Secure login for healthcare providers
- **Prescription Retrieval**: Search and view patient prescriptions by Patient ID
- **Comprehensive Patient View**: Access assessment data, symptoms, follow-up responses, and prescription details

## Architecture

### Technology Stack
- **Frontend**: React with React Router for navigation
- **Backend**: Python (Flask/FastAPI) RESTful API
- **Data Storage**: JSON files (patients.json, assessments.json, prescriptions.json, doctors.json, assignments.json)
- **Authentication**: JWT-based session management
- **Password Security**: bcrypt hashing

### System Architecture
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
│                      JSON File Storage                       │
└─────────────────────────────────────────────────────────────┘
```

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- Node.js 14 or higher
- npm or yarn package manager

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the data directory:
```bash
mkdir data
```

5. Create initial JSON files (or they will be created automatically on first run):
```bash
# The application will create these files:
# - data/patients.json
# - data/assessments.json
# - data/prescriptions.json
# - data/doctors.json
# - data/assignments.json
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
# or
yarn install
```

## Running the Application

### Start the Backend Server

1. Ensure you're in the backend directory with the virtual environment activated
2. Run the server:
```bash
# Flask
python app.py

# FastAPI
uvicorn main:app --reload
```

The backend API will be available at `http://localhost:5000` (Flask) or `http://localhost:8000` (FastAPI)

### Start the Frontend Development Server

1. In a new terminal, navigate to the frontend directory
2. Start the development server:
```bash
npm start
# or
yarn start
```

The frontend will be available at `http://localhost:3000`

## API Endpoints

### Patient Endpoints
- `POST /api/patients/register` - Register a new patient
- `POST /api/patients/login` - Patient authentication
- `GET /api/patients/{patient_id}/history` - Retrieve patient history

### Assessment Endpoints
- `POST /api/assessments` - Submit health assessment
- `GET /api/assessments/{assessment_id}` - Retrieve specific assessment
- `POST /api/assessments/{assessment_id}/followup-questions` - Get follow-up questions
- `POST /api/assessments/{assessment_id}/followup-responses` - Submit follow-up responses

### Prescription Endpoints
- `POST /api/prescriptions/generate` - Generate prescription from assessment
- `GET /api/prescriptions/patient/{patient_id}` - Retrieve patient prescriptions

### Doctor Endpoints
- `POST /api/doctors/login` - Doctor authentication

### Assignment Endpoints
- `POST /api/assignments` - Create doctor assignment with token

## Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
# or
yarn test
```

### Property-Based Tests
The system includes property-based tests using:
- **Python**: Hypothesis
- **JavaScript/TypeScript**: fast-check

Run property-based tests with:
```bash
# Backend
pytest -k "property"

# Frontend
npm test -- --testNamePattern="property"
```

## Data Storage

The application uses JSON files for data persistence:
- `patients.json` - Patient registration data
- `assessments.json` - Health assessment records
- `prescriptions.json` - Generated prescriptions
- `doctors.json` - Doctor information
- `assignments.json` - Doctor-patient assignments with tokens

**Note**: JSON file storage is suitable for demonstration and development. For production use with multiple concurrent users, migration to SQL Server or another relational database is recommended.

## Security Considerations

- Passwords are hashed using bcrypt before storage
- Session tokens use JWT for secure authentication
- CORS is configured for frontend-backend communication
- Input validation on both client and server side
- Role-based access control (patients can only access their own data)

## Important Disclaimer

⚠️ **This is a demonstration system only**

The prescriptions generated by this system are dummy/demonstration prescriptions and should NOT be used for actual medical advice or treatment. This application is for educational and demonstration purposes only.

## Future Enhancements

- Migration from JSON files to SQL Server database
- Real-time notifications for doctor assignments
- Appointment scheduling integration
- Medical history import/export
- Multi-language support
- Mobile application (iOS/Android)
- Integration with electronic health record (EHR) systems

## License

This project is for educational purposes.

## Support

For questions or issues, please refer to the project documentation in `.kiro/specs/patient-assessment-system/`.
