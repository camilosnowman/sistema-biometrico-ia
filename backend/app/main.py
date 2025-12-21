from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from typing import List

from .services.llama_service import llama_service
from .schemas import EmotionResponse, BatchResponse, HealthResponse
from .logger import get_logger

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

@app.post("/analyze", response_model=EmotionResponse)
@limiter.limit("10/minute")
async def analyze_image(request: Request, file: UploadFile = File(...)):
    """
    Analyzes a single image for emotions.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image.")
    
    try:
        logger.info(f"Processing simple analysis for {file.filename}")
        contents = await file.read()
        result = llama_service.analyze_face(contents)
        return result
    except Exception as e:
        logger.error(f"Error in /analyze: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/batch-analyze", response_model=BatchResponse)
@limiter.limit("2/minute")
async def batch_analyze(request: Request, files: List[UploadFile] = File(...)):
    """
    Analyzes multiple images in batch.
    """
    results = []
    failed = 0
    
    if len(files) > 5:
         raise HTTPException(status_code=400, detail="Batch size limit exceeded (max 5 images).")

    for file in files:
        try:
            if not file.content_type.startswith("image/"):
                failed += 1
                continue
            
            contents = await file.read()
            sentiment = llama_service.analyze_face(contents)
            results.append(sentiment)
        except Exception as e:
            logger.error(f"Batch processing error for {file.filename}: {str(e)}")
            failed += 1
            results.append(EmotionResponse(emotion="error", confidence=0.0, reasoning=str(e)))

    return BatchResponse(
        results=results,
        processed_count=len(results),
        failed_count=failed
    )
