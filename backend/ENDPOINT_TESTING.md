# Patient Registration Endpoint Testing Guide

## Endpoint: POST /api/patients/register

### Description
Registers a new patient in the system with validation and secure password hashing.

### Request Format
```json
{
  "firstName": "John",
  "lastName": "Doe",
  "email": "john.doe@example.com",
  "password": "securepassword123"
}
```

### Success Response (201 Created)
```json
{
  "message": "Patient registered successfully",
  "patientID": "550e8400-e29b-41d4-a716-446655440000",
  "firstName": "John",
  "lastName": "Doe",
  "email": "john.doe@example.com"
}
```

### Error Responses

#### Missing Required Fields (400 Bad Request)
```json
{
  "error": "Validation error",
  "message": "Missing required fields: firstName, email"
}
```

#### Empty Fields (400 Bad Request)
```json
{
  "error": "Validation error",
  "message": "All fields must be non-empty"
}
```

#### Invalid Email Format (400 Bad Request)
```json
{
  "error": "Validation error",
  "message": "Invalid email format"
}
```

#### Duplicate Email (400 Bad Request)
```json
{
  "error": "Validation error",
  "message": "Email already registered"
}
```

## Testing with curl

### Successful Registration
```bash
curl -X POST http://localhost:5000/api/patients/register \
  -H "Content-Type: application/json" \
  -d '{
    "firstName": "John",
    "lastName": "Doe",
    "email": "john.doe@example.com",
    "password": "securepassword123"
  }'
```

### Missing Field
```bash
curl -X POST http://localhost:5000/api/patients/register \
  -H "Content-Type: application/json" \
  -d '{
    "firstName": "John",
    "email": "john.doe@example.com",
    "password": "securepassword123"
  }'
```

### Invalid Email
```bash
curl -X POST http://localhost:5000/api/patients/register \
  -H "Content-Type: application/json" \
  -d '{
    "firstName": "John",
    "lastName": "Doe",
    "email": "notanemail",
    "password": "securepassword123"
  }'
```

## Running Automated Tests

```bash
cd backend
python -m pytest tests/test_patient_registration.py -v
```

## Implementation Details

### Security Features
- **Password Hashing**: Uses bcrypt with salt for secure password storage
- **Email Normalization**: Converts emails to lowercase for case-insensitive comparison
- **Input Sanitization**: Trims whitespace from input fields

### Validation Rules
1. All fields (firstName, lastName, email, password) are required
2. Fields cannot be empty strings (after trimming whitespace)
3. Email must match standard email format regex
4. Email must be unique (case-insensitive)

### Data Storage
- Patient records are stored in `backend/data/patients.json`
- Each patient receives a unique UUID as their Patient_ID
- Password is hashed using bcrypt before storage
- Registration timestamp is recorded in ISO format (UTC)

### Requirements Validated
- **Requirement 1.1**: System creates unique Patient_ID and stores patient record
- **Requirement 1.2**: System rejects registration with incomplete information and displays validation errors

---

# Patient Authentication Endpoint Testing Guide

## Endpoint: POST /api/patients/login

### Description
Authenticates a patient with email and password, returning a JWT session token for accessing protected endpoints.

### Request Format
```json
{
  "email": "john.doe@example.com",
  "password": "securepassword123"
}
```

### Success Response (200 OK)
```json
{
  "message": "Authentication successful",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "patient": {
    "patientID": "550e8400-e29b-41d4-a716-446655440000",
    "firstName": "John",
    "lastName": "Doe",
    "email": "john.doe@example.com"
  }
}
```

### Error Responses

#### Missing Required Fields (400 Bad Request)
```json
{
  "error": "Validation error",
  "message": "Missing required fields: email"
}
```

#### Empty Fields (400 Bad Request)
```json
{
  "error": "Validation error",
  "message": "Email and password must be non-empty"
}
```

#### Invalid Credentials (401 Unauthorized)
```json
{
  "error": "Invalid credentials",
  "message": "Invalid email or password"
}
```

## Testing with curl

### Successful Login
First, register a patient:
```bash
curl -X POST http://localhost:5000/api/patients/register \
  -H "Content-Type: application/json" \
  -d '{
    "firstName": "John",
    "lastName": "Doe",
    "email": "john.doe@example.com",
    "password": "securepassword123"
  }'
```

Then login:
```bash
curl -X POST http://localhost:5000/api/patients/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@example.com",
    "password": "securepassword123"
  }'
```

### Invalid Password
```bash
curl -X POST http://localhost:5000/api/patients/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@example.com",
    "password": "wrongpassword"
  }'
```

### Non-existent Email
```bash
curl -X POST http://localhost:5000/api/patients/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "nonexistent@example.com",
    "password": "somepassword"
  }'
```

### Missing Field
```bash
curl -X POST http://localhost:5000/api/patients/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@example.com"
  }'
```

## Running Automated Tests

```bash
cd backend
python -m pytest tests/test_patient_login.py -v
```

## Implementation Details

### Security Features
- **JWT Tokens**: Uses JSON Web Tokens (JWT) for stateless authentication
- **Token Expiration**: Tokens expire after 24 hours
- **Password Verification**: Uses bcrypt to verify passwords securely
- **Case-Insensitive Email**: Email matching is case-insensitive
- **Generic Error Messages**: Returns same error message for invalid email or password to prevent user enumeration

### Token Structure
The JWT token contains:
- `patientID`: Unique patient identifier
- `email`: Patient's email address
- `exp`: Token expiration timestamp (24 hours from creation)

### Validation Rules
1. Both email and password fields are required
2. Fields cannot be empty strings
3. Email must exist in the system
4. Password must match the stored hash

### Using the Token
Include the token in the Authorization header for protected endpoints:
```bash
curl -X GET http://localhost:5000/api/patients/{patient_id}/history \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### Requirements Validated
- **Requirement 2.1**: System authenticates patient with valid credentials and grants access
- **Requirement 2.2**: System rejects invalid credentials and displays error message
