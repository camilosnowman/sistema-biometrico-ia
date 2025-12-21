from fastapi import FastAPI, UploadFile, File, HTTPException, Request, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from typing import List

import sys
import os

# Ensure the current directory is in sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from services.bio_llama_service import llama_service
import bio_schemas
import bio_logger

# Extracting what we need from modules
EmotionResponse = bio_schemas.EmotionResponse
BatchResponse = bio_schemas.BatchResponse
HealthResponse = bio_schemas.HealthResponse
get_logger = bio_logger.get_logger

logger = get_logger("MainAPI")

# Initialize Rate Limiter
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(title="Sistema Biométrico Llama", version="1.1.0")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Catches any unhandled exceptions and returns a structured JSON response.
    """
    logger.error(f"Unhandled error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error. Please try again later.", "type": "internal_error"}
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Ensures HTTPExceptions return consistent structure.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "type": "http_error"}
    )


@app.on_event("startup")
async def startup_event():
    logger.info("Starting Biometric API...")

@app.get("/")
def read_root():
    return {"status": "online", "service": "Llama Biometric Backend", "docs": "/docs"}

@app.get("/health", response_model=HealthResponse)
@limiter.limit("5/minute")
def health_check(request: Request):
    is_llama_up = llama_service.check_connection()
    status = "healthy" if is_llama_up else "degraded"
    
    return HealthResponse(
        status=status,
        service="Biometric API",
        llama_status="connected" if is_llama_up else "disconnected",
        version="1.1.0"
    )

MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5 MB
ALLOWED_MIME_TYPES = ["image/jpeg", "image/png", "image/webp"]

@app.post("/analyze", response_model=EmotionResponse)
@limiter.limit("15/minute")
async def analyze_image(request: Request, file: UploadFile = File(...)):
    """
    Analyzes a single image for emotions.
    - Max size: 5MB
    - Allowed types: JPEG, PNG, WEBP
    """
    # 1. Validate MIME type
    if file.content_type not in ALLOWED_MIME_TYPES:
        logger.warning(f"Invalid MIME type: {file.content_type}")
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid file type. Allowed: {', '.join(ALLOWED_MIME_TYPES)}"
        )
    
    # 2. Validate File Size
    contents = await file.read()
    if len(contents) > MAX_IMAGE_SIZE:
        logger.warning(f"File too large: {len(contents)} bytes")
        raise HTTPException(
            status_code=413, 
            detail="Image too large. Maximum size is 5MB."
        )
    
    try:
        logger.info(f"Processing analysis for {file.filename} ({len(contents)} bytes)")
        result = llama_service.analyze_face(contents)
        return result
    except Exception as e:
        logger.error(f"Critical error in /analyze: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error during analysis")

@app.post("/batch-analyze", response_model=BatchResponse)
@limiter.limit("5/minute")
async def batch_analyze(request: Request, files: List[UploadFile] = File(...)):
    """
    Analyzes multiple images (max 5) in batch.
    Processes them sequentially to manage AI model resources.
    """
    if len(files) > 5:
         raise HTTPException(status_code=400, detail="Batch size limit exceeded (max 5 images).")

    results = []
    failed = 0
    
    for file in files:
        try:
            # Re-using the same validations as /analyze
            if file.content_type not in ALLOWED_MIME_TYPES:
                logger.warning(f"Batch: Invalid MIME type for {file.filename}")
                results.append(EmotionResponse(
                    emotion="error", 
                    confidence=0.0, 
                    reasoning=f"File type {file.content_type} not allowed"
                ))
                failed += 1
                continue
            
            contents = await file.read()
            if len(contents) > MAX_IMAGE_SIZE:
                logger.warning(f"Batch: File too large: {file.filename}")
                results.append(EmotionResponse(
                    emotion="error", 
                    confidence=0.0, 
                    reasoning="Image exceeds 5MB limit"
                ))
                failed += 1
                continue
                
            sentiment = llama_service.analyze_face(contents)
            results.append(sentiment)
            if sentiment.emotion == "error":
                failed += 1
                
        except Exception as e:
            logger.error(f"Batch processing error for {file.filename}: {str(e)}")
            failed += 1
            results.append(EmotionResponse(
                emotion="error", 
                confidence=0.0, 
                reasoning=f"Critical processing error: {str(e)}"
            ))

    return BatchResponse(
        results=results,
        processed_count=len(results),
        failed_count=failed
    )
