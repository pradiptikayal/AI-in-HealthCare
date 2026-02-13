# AWS Bedrock Setup Guide

## Quick Start (5 minutes)

### Step 1: Create AWS Account
If you don't have one: https://aws.amazon.com/free/

### Step 2: Create IAM User with Bedrock Access

1. Go to AWS Console → IAM → Users
2. Click "Create user"
3. Username: `bedrock-app-user`
4. Click "Next"
5. Select "Attach policies directly"
6. Click "Create policy" → JSON tab
7. Paste this policy:

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

8. Name it: `BedrockInvokePolicy`
9. Create policy
10. Go back to user creation, attach `BedrockInvokePolicy`
11. Click "Next" → "Create user"

### Step 3: Create Access Keys

1. Click on the created user
2. Go to "Security credentials" tab
3. Scroll to "Access keys"
4. Click "Create access key"
5. Select "Application running outside AWS"
6. Click "Next" → "Create access key"
7. **IMPORTANT**: Copy both:
   - Access key ID
   - Secret access key
   (You won't see the secret again!)

### Step 4: Enable Bedrock Model Access

1. Go to AWS Console → Amazon Bedrock
2. Select region: **us-east-1** (recommended)
3. Click "Model access" in left sidebar
4. Click "Manage model access"
5. Find "Anthropic" section
6. Check "Claude 3 Sonnet"
7. Click "Request model access"
8. Wait ~30 seconds for approval (usually instant)

### Step 5: Configure Application

Create `backend/.env` file:

```env
# AWS Bedrock Configuration
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=AKIA...your-access-key-id
AWS_SECRET_ACCESS_KEY=your-secret-access-key
BEDROCK_MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0
```

### Step 6: Test It!

```bash
cd backend
python app.py
```

Create an assessment and check if prescription is AI-generated!

## Verification

### Check if Bedrock is Working

Look for this in prescription records:
```json
{
  "generatedBy": "AI-Bedrock"
}
```

If you see this, Bedrock is working! 🎉

### Check Application Logs

When creating assessment, you should see:
- No "Warning: Failed to initialize Bedrock client" message
- No "Error generating prescription with Bedrock" message

## Troubleshooting

### "Failed to initialize Bedrock client"
- Check AWS credentials in `.env` file
- Verify credentials are correct (no extra spaces)
- Ensure `.env` file is in `backend/` directory

### "Access Denied" or "UnauthorizedOperation"
- Check IAM policy is attached to user
- Verify policy allows `bedrock:InvokeModel`
- Check you're using the correct region

### "Model not found" or "Model access denied"
- Go to Bedrock console → Model access
- Verify Claude 3 Sonnet is enabled
- Wait a few minutes if just enabled

### Prescriptions still generic
- Check if fallback is being used
- Look for error messages in console
- Verify `generatedBy: 'AI-Bedrock'` in prescription

## Cost Estimate

- **Claude 3 Sonnet**: ~$0.005 per prescription
- **100 prescriptions/day**: ~$0.50/day = ~$15/month
- **1000 prescriptions/day**: ~$5/day = ~$150/month

## Security Best Practices

### For Development
✅ Use `.env` file (already in `.gitignore`)
✅ Never commit AWS credentials to git
✅ Use IAM user with minimal permissions

### For Production
✅ Use AWS IAM roles (EC2/ECS)
✅ Enable CloudTrail logging
✅ Use AWS Secrets Manager
✅ Enable VPC endpoints for Bedrock
✅ Set up billing alerts

## Alternative: Use AWS CLI Configuration

Instead of `.env` file, you can use AWS CLI:

```bash
aws configure
```

Enter:
- AWS Access Key ID: [your key]
- AWS Secret Access Key: [your secret]
- Default region: us-east-1
- Default output format: json

The application will automatically use these credentials.

## Regions with Bedrock

Claude 3 Sonnet is available in:
- us-east-1 (N. Virginia) ✅ Recommended
- us-west-2 (Oregon)
- eu-west-1 (Ireland)
- ap-southeast-1 (Singapore)
- ap-northeast-1 (Tokyo)

## Testing Without AWS

The application has a fallback system. If AWS is not configured:
- Prescriptions still work
- Uses rule-based system
- No AI features
- No AWS costs

This is useful for:
- Local development
- Testing
- Demo environments

## Next Steps

After setup:
1. Test prescription generation
2. Review AI-generated prescriptions
3. Monitor AWS costs in Cost Explorer
4. Set up billing alerts
5. Consider caching for cost optimization

## Support Resources

- AWS Bedrock Docs: https://docs.aws.amazon.com/bedrock/
- AWS Support: https://console.aws.amazon.com/support/
- Pricing Calculator: https://calculator.aws/
