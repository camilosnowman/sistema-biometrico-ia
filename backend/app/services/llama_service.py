import json
import urllib.request
import urllib.error
import base64
import os
from typing import Dict, Optional

class LlamaService:
    def __init__(self, model: str = "llama3.2-vision", provider: str = "ollama", api_url: str = "http://localhost:11434/api/chat"):
        self.model = model
        self.provider = provider
        self.api_url = api_url

    def _encode_image(self, image_bytes: bytes) -> str:
        return base64.b64encode(image_bytes).decode('utf-8')

    def analyze_face(self, image_bytes: bytes) -> Dict:
        """
        Sends image to Llama 3.2 Vision and expects a structured JSON response.
        Uses standard urllib to avoid 'requests' dependency issues.
        """
        base64_image = self._encode_image(image_bytes)
        
        system_prompt = """
You are an advanced Biometric AI specialized in micro-expression analysis.
Your task is to analyze the provided image of a human face and identify the primary emotion.

output MUST be a valid JSON object with exactly these fields:
- "emotion": string (e.g., "joy", "anger", "surprise", "neutral", "sadness", "fear", "disgust").
- "confidence": float (0.0 to 1.0).
- "reasoning": string (concise explanation citing specific facial features like eyebrows, mouth, eyes).

RULES:
1. ROI: Focus ONLY on the face.
2. If no face is visible, return "emotion": "unknown".
3. "reasoning" must be clinical and observational.
4. Output strictly JSON. No markdown, no preambles.
        """

        user_message = "Analyze the facial expressions in this image. Return strictly JSON."

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_message,
                    "images": [base64_image]
                }
            ],
            "stream": False,
            "format": "json", 
            "options": {
                "temperature": 0.2,
                "num_ctx": 2048 
            }
        }

        try:
            data = json.dumps(payload).encode('utf-8')
            req = urllib.request.Request(self.api_url, data=data, headers={'Content-Type': 'application/json'})
            
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode('utf-8'))
                content = result.get("message", {}).get("content", "{}")
                
                try:
                    parsed_content = json.loads(content)
                    return parsed_content
                except json.JSONDecodeError:
                    return {
                        "emotion": "error",
                        "confidence": 0.0,
                        "reasoning": f"Failed to parse JSON: {content}"
                    }

        except urllib.error.URLError as e:
            return {
                "emotion": "error",
                "confidence": 0.0,
                "reasoning": f"Connection error: {str(e)}"
            }
        except Exception as e:
             return {
                "emotion": "error",
                "confidence": 0.0,
                "reasoning": f"Unexpected error: {str(e)}"
            }

# Singleton instance
llama_service = LlamaService()
