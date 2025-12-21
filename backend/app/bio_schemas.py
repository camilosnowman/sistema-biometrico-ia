from pydantic import BaseModel, Field, field_validator
from typing import List, Optional

class EmotionResponse(BaseModel):
    """
    Schema for a single emotion analysis result.
    """
    emotion: str = Field(..., description="The detected primary emotion (e.g., joy, anger, neutral)")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score between 0 and 1")
    reasoning: str = Field(..., description="Clinical explanation of the detected micro-expressions")

    @field_validator('emotion')
    @classmethod
    def validate_emotion(cls, v: str) -> str:
        allowed = ["joy", "anger", "surprise", "neutral", "sadness", "fear", "disgust", "unknown", "error"]
        if v.lower() not in allowed:
            # We allow it but log a warning or normalize?
            # For now, let's just normalize to lowercase
            return v.lower()
        return v.lower()

class BatchResponse(BaseModel):
    """
    Schema for multiple emotion analysis results.
    """
    results: List[EmotionResponse]
    processed_count: int
    failed_count: int

class HealthResponse(BaseModel):
    """
    Schema for API health status.
    """
    status: str
    service: str = "Biometric API"
    llama_status: str
    version: str = "1.1.0"
