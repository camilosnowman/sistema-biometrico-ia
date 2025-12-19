from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .services.llama_service import llama_service

app = FastAPI(title="Sistema Biométrico Llama", version="1.0.0")

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "online", "service": "Llama Biometric Backend"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):
    """
    Analyzes an uploaded image file for emotions using Llama 3.2 Vision.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image.")
    
    try:
        contents = await file.read()
        result = llama_service.analyze_face(contents)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
