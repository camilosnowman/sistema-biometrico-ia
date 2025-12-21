import json
import requests
import base64
from typing import Dict, Any
import sys
import os

# Add parent directory to path to find schemas and logger
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

import bio_schemas
import bio_logger

EmotionResponse = bio_schemas.EmotionResponse
get_logger = bio_logger.get_logger

logger = get_logger("LlamaService")

class LlamaService:
    def __init__(self, model: str = "llama3.2-vision", provider: str = "ollama", api_url: str = "http://localhost:11434/api/chat"):
        self.model = model
        self.provider = provider
        self.api_url = api_url
        logger.info(f"LlamaService initialized with model: {model}")

    def _encode_image(self, image_bytes: bytes) -> str:
        return base64.b64encode(image_bytes).decode('utf-8')

    def check_connection(self) -> bool:
        """Checks if the LLM provider is reachable."""
        try:
            # Simple check to tags endpoint usually confirms Ollama is up
            requests.get("http://localhost:11434/api/tags", timeout=2)
            return True
        except requests.RequestException:
            logger.error("Llama Provider unreachable.")
            return False

    def analyze_face(self, image_bytes: bytes) -> EmotionResponse:
        """
        Sends image to Llama 3.2 Vision and expects a structured JSON response.
        Returns an EmotionResponse Pydantic model.
        """
        logger.info("Starting face analysis...")
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
            response = requests.post(self.api_url, json=payload, timeout=30)
            response.raise_for_status()
            result = response.json()
            
            content = result.get("message", {}).get("content", "{}")
            
            # Robust JSON parsing
            try:
                # model occasionally wraps json in markdown blocks
                if "```json" in content:
                    content = content.split("```json")[1].split("```")[0].strip()
                elif "```" in content:
                    content = content.split("```")[1].split("```")[0].strip()
                
                parsed_content = json.loads(content)
                
                # Ensure we have the minimum required fields for EmotionResponse
                if not all(k in parsed_content for k in ["emotion", "confidence", "reasoning"]):
                    logger.warning(f"Response missing fields: {parsed_content.keys()}")
                
                logger.info(f"Analysis successful: {parsed_content.get('emotion')}")
                return EmotionResponse(**parsed_content)
                
            except (json.JSONDecodeError, ValueError) as e:
                logger.error(f"Failed to parse model output: {content} | Error: {str(e)}")
                return EmotionResponse(
                    emotion="error", 
                    confidence=0.0, 
                    reasoning=f"Invalid JSON from model: {str(e)}"
                )

        except requests.exceptions.Timeout:
            logger.error("Llama provider request timed out.")
            return EmotionResponse(emotion="error", confidence=0.0, reasoning="Request to AI service timed out")
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {str(e)}")
            return EmotionResponse(emotion="error", confidence=0.0, reasoning=f"API Connection error: {str(e)}")


# Singleton instance
llama_service = LlamaService()
