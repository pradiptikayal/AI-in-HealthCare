# Patient History Endpoint Documentation

## Overview

The patient history endpoint allows authenticated patients to retrieve their complete medical history, including all assessments and associated prescriptions.

## Endpoint

```
GET /api/patients/{patient_id}/history
```

## Authentication

This endpoint requires authentication via JWT token in the Authorization header:

```
Authorization: Bearer <jwt_token>
```

The token must belong to the patient whose history is being requested. Patients can only access their own history.

## Request

### URL Parameters

- `patient_id` (string, required): The unique identifier of the patient

### Headers

- `Authorization` (string, required): Bearer token obtained from login endpoint

### Example Request

```bash
curl -X GET http://localhost:5000/api/patients/abc-123-def/history \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

## Response

### Success Response (200 OK)

```json
{
  "patientID": "abc-123-def",
  "history": [
    {
      "assessmentID": "assessment-xyz",
      "assessmentDate": "2024-01-20T10:00:00Z",
      "weight": 71,
      "weightUnit": "kg",
      "height": 175,
      "heightUnit": "cm",
      "age": 30,
      "symptoms": ["cough", "sore throat"],
      "followUpResponses": [
        {
          "questionID": "q1",
          "questionText": "Is it a dry or wet cough?",
          "answer": "Dry cough"
        }
      ],
      "prescription": {
        "prescriptionID": "prescription-123",
        "medications": [
          {
            "name": "Dextromethorphan",
            "dosage": "10mg",
            "frequency": "Every 4 hours",
            "duration": "7 days"
          }
        ],
        "instructions": "Take with water. Avoid alcohol.",
        "generatedDate": "2024-01-20T10:30:00Z"
      }
    },
    {
      "assessmentID": "assessment-abc",
      "assessmentDate": "2024-01-15T10:00:00Z",
      "weight": 70,
      "weightUnit": "kg",
      "height": 175,
      "heightUnit": "cm",
      "age": 30,
      "symptoms": ["headache", "fever"],
      "followUpResponses": [],
      "prescription": {
        "prescriptionID": "prescription-456",
        "medications": [
          {
            "name": "Ibuprofen",
            "dosage": "200mg",
            "frequency": "Every 6 hours",
            "duration": "3 days"
          }
        ],
        "instructions": "Take with food",
        "generatedDate": "2024-01-15T10:30:00Z"
      }
    }
  ]
}
```

### Response Fields

- `patientID` (string): The patient's unique identifier
- `history` (array): List of assessment records, sorted by date (most recent first)
  - `assessmentID` (string): Unique identifier for the assessment
  - `assessmentDate` (string): ISO 8601 timestamp of when the assessment was created
  - `weight` (number): Patient's weight at time of assessment
  - `weightUnit` (string): Unit of weight measurement ("kg" or "lbs")
  - `height` (number): Patient's height at time of assessment
  - `heightUnit` (string): Unit of height measurement ("cm" or "inches")
  - `age` (number): Patient's age at time of assessment
  - `symptoms` (array): List of symptoms reported
  - `followUpResponses` (array): Follow-up questions and answers (may be empty)
    - `questionID` (string): Unique identifier for the question
    - `questionText` (string): The follow-up question text
    - `answer` (string): Patient's answer to the question
  - `prescription` (object, optional): Prescription details if one was generated
    - `prescriptionID` (string): Unique identifier for the prescription
    - `medications` (array): List of prescribed medications
      - `name` (string): Medication name
      - `dosage` (string): Dosage amount
      - `frequency` (string): How often to take the medication
      - `duration` (string): How long to take the medication
    - `instructions` (string): General instructions for the prescription
    - `generatedDate` (string): ISO 8601 timestamp of when prescription was generated

### Empty History Response (200 OK)

When a patient has no assessments:

```json
{
  "patientID": "abc-123-def",
  "history": []
}
```

### Error Responses

#### 401 Unauthorized - Missing or Invalid Token

```json
{
  "error": "Unauthorized",
  "message": "Missing or invalid authorization header"
}
```

or

```json
{
  "error": "Unauthorized",
  "message": "Invalid or expired token"
}
```

#### 403 Forbidden - Accessing Another Patient's History

```json
{
  "error": "Forbidden",
  "message": "You can only access your own patient history"
}
```

#### 404 Not Found - Patient Does Not Exist

```json
{
  "error": "Not found",
  "message": "Patient not found"
}
```

#### 500 Internal Server Error

```json
{
  "error": "Internal server error",
  "message": "Error details..."
}
```

## Usage Examples

### Python Example

```python
import requests

# Login first to get token
login_response = requests.post('http://localhost:5000/api/patients/login', json={
    'email': 'patient@example.com',
    'password': 'password123'
})
token = login_response.json()['token']
patient_id = login_response.json()['patient']['patientID']

# Get patient history
headers = {'Authorization': f'Bearer {token}'}
history_response = requests.get(
    f'http://localhost:5000/api/patients/{patient_id}/history',
    headers=headers
)

if history_response.status_code == 200:
    history = history_response.json()['history']
    print(f"Found {len(history)} assessments")
    for assessment in history:
        print(f"Date: {assessment['assessmentDate']}")
        print(f"Symptoms: {', '.join(assessment['symptoms'])}")
```

### JavaScript/Fetch Example

```javascript
// Login first to get token
const loginResponse = await fetch('http://localhost:5000/api/patients/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'patient@example.com',
    password: 'password123'
  })
});
const { token, patient } = await loginResponse.json();

// Get patient history
const historyResponse = await fetch(
  `http://localhost:5000/api/patients/${patient.patientID}/history`,
  {
    headers: { 'Authorization': `Bearer ${token}` }
  }
);

if (historyResponse.ok) {
  const { history } = await historyResponse.json();
  console.log(`Found ${history.length} assessments`);
  history.forEach(assessment => {
    console.log(`Date: ${assessment.assessmentDate}`);
    console.log(`Symptoms: ${assessment.symptoms.join(', ')}`);
  });
}
```

## Testing

### Unit Tests

Run the unit tests:

```bash
cd backend
python -m pytest tests/test_patient_history.py -v
```

### Manual Testing

1. Start the Flask server:
   ```bash
   cd backend
   python app.py
   ```

2. Run the manual test script:
   ```bash
   python test_history_manual.py
   ```

This will:
- Register a new patient
- Login to get a token
- Create sample assessments and prescriptions
- Retrieve and display the patient history
- Test error cases

## Requirements Validated

This endpoint validates the following requirements:

- **Requirement 2.3**: When a patient successfully signs in, the system retrieves and displays the patient's history based on Patient_ID
- **Requirement 3.1**: When a patient signs in, the system retrieves all historical health assessments associated with the Patient_ID
- **Requirement 3.2**: When a patient has no previous assessments, the system displays an appropriate message (empty history array)
- **Requirement 3.3**: When displaying patient history, the system shows assessment dates, symptoms, and associated prescriptions

## Security Features

1. **Authentication Required**: All requests must include a valid JWT token
2. **Authorization Check**: Patients can only access their own history
3. **Token Validation**: Expired or invalid tokens are rejected
4. **Patient Verification**: Verifies the patient exists before retrieving history

## Notes

- History is sorted by assessment date in descending order (most recent first)
- Assessments without prescriptions are included in the history
- Follow-up responses are included if they exist
- The endpoint handles empty history gracefully
- All dates are in ISO 8601 format (UTC timezone)
