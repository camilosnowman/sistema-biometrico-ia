from pydantic import BaseModel, Field
from typing import List, Optional

class EmotionResponse(BaseModel):
    emotion: str = Field(..., description="Detected emotion (e.g., joy, anger, neutral)")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score between 0 and 1")
    reasoning: str = Field(..., description="Explanation of the facial features analysis")

class BatchResponse(BaseModel):
    results: List[EmotionResponse]
    processed_count: int
    failed_count: int

class HealthResponse(BaseModel):
    status: str
    service: str
    llama_status: str
    version: str
