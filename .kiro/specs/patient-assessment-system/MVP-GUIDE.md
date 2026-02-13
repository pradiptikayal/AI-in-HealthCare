# Patient Assessment System - MVP Guide

## What's Included in This MVP

This is a minimal working version of the Patient Assessment System with the essential features:

### Backend Features ✅
- **Patient Registration** - Create new patient accounts with secure password hashing
- **Patient Login** - JWT-based authentication
- **Patient History** - View all past assessments and prescriptions
- **Health Assessment** - Submit symptoms and health data
- **Automatic Prescription Generation** - Get dummy prescriptions based on symptoms
- **Doctor Assignment** - Automatic doctor assignment with visit token

### Frontend Features ✅
- **Registration Page** - Clean, user-friendly registration form
- **Login Page** - Secure login with error handling
- **Dashboard** - View patient info and assessment history
- **Assessment Form** - Submit health assessments with weight, height, age, and symptoms
- **Results Page** - View prescription and doctor assignment after assessment

### What's NOT Included (Can Be Added Later)
- Follow-up questions based on symptoms
- Doctor portal
- Advanced prescription logic
- Property-based tests
- Responsive design optimizations
- Email verification
- Password reset

## Quick Start

### 1. Start the Backend

```bash
cd backend
python app.py
```

The API will run on `http://localhost:5000`

### 2. Start the Frontend

In a new terminal:

```bash
cd frontend
npm run dev
```

The app will run on `http://localhost:3000`

### 3. Test the Application

1. **Register a New Patient**
   - Go to `http://localhost:3000`
   - Click "Register here"
   - Fill in your details
   - Click "Register"

2. **Login**
   - Use your email and password
   - Click "Login"

3. **Submit an Assessment**
   - Click "Start New Assessment"
   - Enter your weight, height, and age
   - Enter symptoms (try: headache, fever, cough)
   - Click "Submit Assessment"

4. **View Results**
   - See your prescription with medications
   - Note your doctor assignment and visit token
   - Return to dashboard

5. **View History**
   - Your dashboard shows all past assessments
   - Each assessment includes prescription details

## API Endpoints

### Patient Endpoints

**POST /api/patients/register**
```json
{
  "firstName": "John",
  "lastName": "Doe",
  "email": "john@example.com",
  "password": "password123"
}
```

**POST /api/patients/login**
```json
{
  "email": "john@example.com",
  "password": "password123"
}
```

**GET /api/patients/{patient_id}/history**
- Requires: `Authorization: Bearer <token>` header

### Assessment Endpoint

**POST /api/assessments**
```json
{
  "patientID": "patient-uuid",
  "weight": 70,
  "weightUnit": "kg",
  "height": 175,
  "heightUnit": "cm",
  "age": 30,
  "symptoms": ["headache", "fever"]
}
```
- Requires: `Authorization: Bearer <token>` header

## Supported Symptoms

The MVP recognizes these symptoms and provides appropriate medications:

- **headache** → Ibuprofen
- **fever** → Acetaminophen
- **cough** → Dextromethorphan
- **sore throat** → Throat Lozenges
- **fatigue** → Multivitamin
- **nausea** → Ondansetron

For unrecognized symptoms, the system provides general rest and hydration advice.

## Sample Doctors

The system includes 5 sample doctors:
- Dr. Sarah Johnson (General Practice)
- Dr. Michael Chen (Internal Medicine)
- Dr. Emily Rodriguez (Family Medicine)
- Dr. David Patel (Cardiology)
- Dr. Jennifer Williams (Pediatrics)

## Testing

### Manual Testing

1. **Test Registration**
   ```bash
   curl -X POST http://localhost:5000/api/patients/register \
     -H "Content-Type: application/json" \
     -d '{"firstName":"Test","lastName":"User","email":"test@example.com","password":"test123"}'
   ```

2. **Test Login**
   ```bash
   curl -X POST http://localhost:5000/api/patients/login \
     -H "Content-Type: application/json" \
     -d '{"email":"test@example.com","password":"test123"}'
   ```

3. **Test Assessment** (use token from login)
   ```bash
   curl -X POST http://localhost:5000/api/assessments \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer YOUR_TOKEN_HERE" \
     -d '{"patientID":"YOUR_PATIENT_ID","weight":70,"weightUnit":"kg","height":175,"heightUnit":"cm","age":30,"symptoms":["headache","fever"]}'
   ```

### Automated Tests

Run backend tests:
```bash
cd backend
pytest
```

## Project Structure

```
patient-assessment-system/
├── backend/
│   ├── app.py                    # Main Flask application
│   ├── data_access.py            # Data persistence utilities
│   ├── data/                     # JSON data files
│   │   ├── patients.json
│   │   ├── assessments.json
│   │   ├── prescriptions.json
│   │   ├── doctors.json
│   │   └── assignments.json
│   └── tests/                    # Backend tests
├── frontend/
│   ├── src/
│   │   ├── pages/               # React page components
│   │   │   ├── Register.jsx
│   │   │   ├── Login.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   └── Assessment.jsx
│   │   ├── App.jsx              # Main app component
│   │   ├── App.css              # Styles
│   │   └── main.jsx             # Entry point
│   └── package.json
└── README.md
```

## Data Storage

All data is stored in JSON files in `backend/data/`:
- `patients.json` - Patient accounts
- `assessments.json` - Health assessments
- `prescriptions.json` - Generated prescriptions
- `doctors.json` - Doctor information
- `assignments.json` - Doctor-patient assignments

## Security Features

- ✅ Password hashing with bcrypt
- ✅ JWT token authentication
- ✅ Token expiration (24 hours)
- ✅ CORS configuration
- ✅ Input validation
- ✅ Authorization checks (patients can only access their own data)

## Next Steps to Enhance

1. **Add Follow-up Questions**
   - Implement symptom-based follow-up questions
   - Store and display follow-up responses

2. **Build Doctor Portal**
   - Doctor login
   - View patient prescriptions by Patient ID

3. **Improve Prescription Logic**
   - More sophisticated symptom-to-medication mapping
   - Consider patient age, weight, and medical history

4. **Add Property-Based Tests**
   - Implement Hypothesis tests for backend
   - Implement fast-check tests for frontend

5. **Enhance UI/UX**
   - Better mobile responsiveness
   - Loading states and animations
   - Form validation feedback

6. **Add More Features**
   - Email notifications
   - Appointment scheduling
   - Medical history import/export
   - Multi-language support

## Troubleshooting

### Backend won't start
- Make sure you're in the backend directory
- Ensure Python 3.8+ is installed
- Check that all dependencies are installed: `pip install -r requirements.txt`

### Frontend won't start
- Make sure you're in the frontend directory
- Ensure Node.js is installed
- Run `npm install` to install dependencies

### Can't login after registration
- Check that the backend is running
- Verify the email and password are correct
- Check browser console for errors

### Assessment submission fails
- Ensure you're logged in
- Check that all fields are filled
- Verify symptoms are comma-separated
- Check backend console for errors

## Important Disclaimer

⚠️ **This is a demonstration system only**

The prescriptions generated by this system are dummy/demonstration prescriptions and should NOT be used for actual medical advice or treatment. This application is for educational and demonstration purposes only.

## Support

For issues or questions:
1. Check the main README.md
2. Review the API documentation in backend/ENDPOINT_TESTING.md
3. Check the spec files in .kiro/specs/patient-assessment-system/

