# Amazon Bedrock Integration for AI Prescription Generation

## Overview

The application now uses Amazon Bedrock with Claude 3 Sonnet to generate intelligent, context-aware prescriptions based on patient symptoms and health data.

## What Changed

### 1. New Dependencies
- Added `boto3==1.34.34` to `requirements.txt` for AWS SDK

### 2. New Module: `bedrock_service.py`
Created a dedicated service for Bedrock integration with:
- **BedrockService class**: Handles all Bedrock API interactions
- **Smart prompt engineering**: Sends patient data (symptoms, age, weight, height) to LLM
- **JSON response parsing**: Extracts structured prescription data
- **Fallback mechanism**: Uses rule-based system if Bedrock is unavailable
- **Error handling**: Graceful degradation if AWS credentials are missing

### 3. Updated `app.py`
- Imported `get_bedrock_service()` function
- Removed hardcoded `SYMPTOM_MEDICATIONS` dictionary
- Updated `create_assessment()` endpoint to use Bedrock for prescription generation
- Added `generatedBy: 'AI-Bedrock'` field to prescription records

### 4. Environment Configuration
Updated `.env.example` with AWS Bedrock settings:
- `AWS_REGION`: AWS region (default: us-east-1)
- `AWS_ACCESS_KEY_ID`: Your AWS access key
- `AWS_SECRET_ACCESS_KEY`: Your AWS secret key
- `BEDROCK_MODEL_ID`: Model to use (default: Claude 3 Sonnet)

## Setup Instructions

### Step 1: Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### Step 2: Configure AWS Credentials

**Option A: Environment Variables (Recommended for Development)**
Create or update `backend/.env`:
```env
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your-actual-access-key-id
AWS_SECRET_ACCESS_KEY=your-actual-secret-access-key
BEDROCK_MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0
```

**Option B: AWS CLI Configuration (Recommended for Production)**
```bash
aws configure
```
This stores credentials in `~/.aws/credentials`

**Option C: IAM Role (Recommended for EC2/ECS)**
Attach an IAM role with Bedrock permissions to your EC2 instance or ECS task.

### Step 3: Enable Bedrock Model Access

1. Go to AWS Console → Amazon Bedrock
2. Navigate to "Model access" in the left sidebar
3. Click "Manage model access"
4. Enable access to "Claude 3 Sonnet" (anthropic.claude-3-sonnet-20240229-v1:0)
5. Wait for access to be granted (usually instant)

### Step 4: Set IAM Permissions

Your AWS user/role needs these permissions:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel"
      ],
      "Resource": "arn:aws:bedrock:*::foundation-model/anthropic.claude-3-sonnet-20240229-v1:0"
    }
  ]
}
```

## How It Works

### Prescription Generation Flow

1. **Patient submits assessment** with symptoms, age, weight, height
2. **Backend receives request** at `POST /api/assessments`
3. **Bedrock service is called** with patient data
4. **LLM generates prescription** with:
   - Medication names
   - Dosages
   - Frequency
   - Duration
   - General care instructions
5. **Response is parsed** and validated
6. **Prescription is saved** to database
7. **Patient receives** AI-generated prescription

### Example LLM Prompt

```
You are a medical AI assistant helping to generate preliminary medication recommendations.

Patient Information:
- Age: 30 years
- Weight: 70 kg
- Height: 175 cm
- Symptoms: headache, fever

Generate a preliminary prescription recommendation...
```

### Example LLM Response

```json
{
  "medications": [
    {
      "name": "Acetaminophen",
      "dosage": "500mg",
      "frequency": "Every 4-6 hours",
      "duration": "3-5 days"
    },
    {
      "name": "Ibuprofen",
      "dosage": "200mg",
      "frequency": "Every 6-8 hours",
      "duration": "3 days"
    }
  ],
  "instructions": "Take medications with food. Stay hydrated. Rest adequately. If fever persists beyond 3 days or exceeds 103°F, seek immediate medical attention. This is a preliminary recommendation and must be reviewed by a licensed physician."
}
```

## Fallback Mechanism

If Bedrock is unavailable (no credentials, API error, network issue), the system automatically falls back to the rule-based prescription system:

```python
# Fallback uses simple symptom mapping
symptom_medications = {
    'headache': {'name': 'Ibuprofen', 'dosage': '200mg', ...},
    'fever': {'name': 'Acetaminophen', 'dosage': '500mg', ...},
    # ... more mappings
}
```

This ensures the application continues working even without AWS access.

## Testing

### Test Bedrock Integration

1. **Start the backend** with AWS credentials configured
2. **Create an assessment** via API or frontend
3. **Check the prescription** - it should be more detailed and context-aware
4. **Look for `generatedBy: 'AI-Bedrock'`** in the prescription record

### Test Fallback

1. **Remove AWS credentials** or set invalid ones
2. **Create an assessment**
3. **Verify fallback works** - prescription still generated using rules

### Manual API Test

```bash
# Login first
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"email":"patient@example.com","password":"password123"}'

# Create assessment (use token from login)
curl -X POST http://localhost:5000/api/assessments \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "patientID": "your-patient-id",
    "weight": 70,
    "weightUnit": "kg",
    "height": 175,
    "heightUnit": "cm",
    "age": 30,
    "symptoms": ["headache", "fever", "fatigue"]
  }'
```

## Cost Considerations

### Bedrock Pricing (as of 2024)
- **Claude 3 Sonnet**: ~$0.003 per 1K input tokens, ~$0.015 per 1K output tokens
- **Average prescription generation**: ~500 input tokens + 200 output tokens
- **Cost per prescription**: ~$0.005 (half a cent)
- **1000 prescriptions**: ~$5

### Cost Optimization
- Prescriptions are cached in the database
- No repeated LLM calls for the same assessment
- Fallback system reduces API calls during errors

## Security & Compliance

### Important Notes
1. **Not for production medical use**: This is a demonstration system
2. **Requires physician review**: All AI prescriptions must be reviewed by licensed doctors
3. **HIPAA compliance**: Ensure AWS Bedrock is configured for HIPAA if handling real patient data
4. **Audit logging**: Consider adding CloudTrail logging for compliance
5. **Data privacy**: Patient data sent to Bedrock should be anonymized in production

### AWS Bedrock Security Features
- Data is not used to train models
- Requests are encrypted in transit
- No data retention by default
- Supports VPC endpoints for private connectivity

## Troubleshooting

### Error: "Failed to initialize Bedrock client"
- Check AWS credentials are set correctly
- Verify AWS region is valid
- Ensure boto3 is installed

### Error: "Invalid response from Bedrock"
- Check model ID is correct
- Verify model access is enabled in AWS Console
- Check IAM permissions

### Error: "Could not parse prescription from response"
- LLM returned invalid JSON
- System will automatically use fallback
- Check CloudWatch logs for raw response

### Prescriptions seem generic
- This is expected with fallback mode
- Verify Bedrock is actually being called
- Check application logs for "AI-Bedrock" indicator

## Available Models

You can use different Bedrock models by changing `BEDROCK_MODEL_ID`:

- **Claude 3 Sonnet** (recommended): `anthropic.claude-3-sonnet-20240229-v1:0`
- **Claude 3 Haiku** (faster, cheaper): `anthropic.claude-3-haiku-20240307-v1:0`
- **Claude 3 Opus** (most capable): `anthropic.claude-3-opus-20240229-v1:0`

## Future Enhancements

Potential improvements:
1. **Follow-up questions**: LLM asks clarifying questions about symptoms
2. **Drug interaction checking**: Validate against patient medication history
3. **Allergy checking**: Consider patient allergies in recommendations
4. **Multi-language support**: Generate prescriptions in patient's language
5. **Severity assessment**: LLM determines if emergency care is needed
6. **Caching**: Cache similar symptom combinations to reduce costs

## Files Modified

- `backend/requirements.txt` - Added boto3
- `backend/bedrock_service.py` - New Bedrock integration module
- `backend/app.py` - Updated to use Bedrock service
- `backend/.env.example` - Added AWS configuration
- `BEDROCK-INTEGRATION.md` - This documentation

## Support

For issues with:
- **AWS Bedrock**: Check AWS documentation or AWS Support
- **Application integration**: Review application logs
- **Cost concerns**: Monitor AWS Cost Explorer
