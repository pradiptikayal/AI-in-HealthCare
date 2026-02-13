"""
Amazon Bedrock service for AI-powered prescription generation.
"""

import json
import boto3
import os
from typing import List, Dict, Any


class BedrockService:
    """Service for interacting with Amazon Bedrock LLM."""
    
    def __init__(self):
        """Initialize Bedrock client."""
        self.region = os.getenv('AWS_REGION', 'us-east-1')
        self.model_id = os.getenv('BEDROCK_MODEL_ID', 'anthropic.claude-3-sonnet-20240229-v1:0')
        
        try:
            self.client = boto3.client(
                service_name='bedrock-runtime',
                region_name=self.region
            )
        except Exception as e:
            print(f"Warning: Failed to initialize Bedrock client: {e}")
            self.client = None
    
    def generate_prescription(
        self, 
        symptoms: List[str], 
        age: int, 
        weight: float, 
        weight_unit: str,
        height: float,
        height_unit: str
    ) -> Dict[str, Any]:
        """
        Generate prescription using Amazon Bedrock LLM.
        
        Args:
            symptoms: List of patient symptoms
            age: Patient age
            weight: Patient weight
            weight_unit: Weight unit (kg or lbs)
            height: Patient height
            height_unit: Height unit (cm or inches)
        
        Returns:
            Dictionary with medications list and instructions
        """
        if not self.client:
            return self._fallback_prescription(symptoms)
        
        try:
            # Construct prompt for the LLM
            prompt = self._build_prompt(symptoms, age, weight, weight_unit, height, height_unit)
            
            # Call Bedrock
            response = self._invoke_bedrock(prompt)
            
            # Parse response
            prescription = self._parse_response(response)
            
            return prescription
            
        except Exception as e:
            print(f"Error generating prescription with Bedrock: {e}")
            return self._fallback_prescription(symptoms)
    
    def _build_prompt(
        self, 
        symptoms: List[str], 
        age: int, 
        weight: float, 
        weight_unit: str,
        height: float,
        height_unit: str
    ) -> str:
        """Build the prompt for the LLM."""
        symptoms_str = ", ".join(symptoms)
        
        prompt = f"""You are a medical AI assistant helping to generate preliminary medication recommendations. 

Patient Information:
- Age: {age} years
- Weight: {weight} {weight_unit}
- Height: {height} {height_unit}
- Symptoms: {symptoms_str}

Generate a preliminary prescription recommendation with medications and general instructions. This is for informational purposes only and will be reviewed by a licensed physician.

Respond ONLY with a valid JSON object in this exact format (no markdown, no code blocks, just raw JSON):
{{
  "medications": [
    {{
      "name": "Medication Name",
      "dosage": "dosage amount",
      "frequency": "how often",
      "duration": "how long"
    }}
  ],
  "instructions": "General care instructions for the patient"
}}

Important:
- Recommend only over-the-counter medications or general care
- Keep it simple and safe
- Include 1-3 medications maximum
- Add disclaimer that doctor review is required"""
        
        return prompt
    
    def _invoke_bedrock(self, prompt: str) -> str:
        """Invoke Bedrock API."""
        # Prepare request body for Claude 3
        request_body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "temperature": 0.7,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        
        # Invoke the model
        response = self.client.invoke_model(
            modelId=self.model_id,
            body=json.dumps(request_body)
        )
        
        # Parse response
        response_body = json.loads(response['body'].read())
        
        # Extract text from Claude 3 response
        if 'content' in response_body and len(response_body['content']) > 0:
            return response_body['content'][0]['text']
        
        raise ValueError("Invalid response from Bedrock")
    
    def _parse_response(self, response_text: str) -> Dict[str, Any]:
        """Parse LLM response into structured prescription."""
        try:
            # Try to parse as JSON
            prescription = json.loads(response_text)
            
            # Validate structure
            if 'medications' not in prescription or 'instructions' not in prescription:
                raise ValueError("Invalid prescription structure")
            
            # Ensure medications is a list
            if not isinstance(prescription['medications'], list):
                raise ValueError("Medications must be a list")
            
            return prescription
            
        except json.JSONDecodeError:
            # If JSON parsing fails, try to extract JSON from markdown code blocks
            import re
            json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', response_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(1))
            
            # If still fails, return fallback
            raise ValueError("Could not parse prescription from response")
    
    def _fallback_prescription(self, symptoms: List[str]) -> Dict[str, Any]:
        """Fallback prescription when Bedrock is unavailable."""
        # Simple symptom-to-medication mapping
        symptom_medications = {
            'headache': {'name': 'Ibuprofen', 'dosage': '200mg', 'frequency': 'Every 6 hours', 'duration': '3 days'},
            'fever': {'name': 'Acetaminophen', 'dosage': '500mg', 'frequency': 'Every 4-6 hours', 'duration': '5 days'},
            'cough': {'name': 'Dextromethorphan', 'dosage': '10mg', 'frequency': 'Every 4 hours', 'duration': '7 days'},
            'sore throat': {'name': 'Throat Lozenges', 'dosage': '1 lozenge', 'frequency': 'Every 2-3 hours', 'duration': '5 days'},
            'fatigue': {'name': 'Multivitamin', 'dosage': '1 tablet', 'frequency': 'Once daily', 'duration': '30 days'},
            'nausea': {'name': 'Ondansetron', 'dosage': '4mg', 'frequency': 'Every 8 hours', 'duration': '3 days'},
        }
        
        medications = []
        for symptom in symptoms:
            symptom_lower = symptom.lower()
            if symptom_lower in symptom_medications:
                medications.append(symptom_medications[symptom_lower])
        
        if not medications:
            medications.append({
                'name': 'General Rest and Hydration',
                'dosage': 'As needed',
                'frequency': 'Throughout the day',
                'duration': 'Until symptoms improve'
            })
        
        return {
            'medications': medications,
            'instructions': 'Take medications as directed. Consult a doctor if symptoms persist or worsen.'
        }


# Global instance
_bedrock_service = None

def get_bedrock_service() -> BedrockService:
    """Get or create Bedrock service instance."""
    global _bedrock_service
    if _bedrock_service is None:
        _bedrock_service = BedrockService()
    return _bedrock_service
