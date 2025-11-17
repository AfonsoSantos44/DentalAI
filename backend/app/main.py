from fastapi import FastAPI
from app.routes.audio_routes import router as audio_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Dental AI Assistant",
    description="Processes audio → transcription → dental structured JSON",
    version="1.0.0",
)

# ---- Allow backend/mobile to call this API ----
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(audio_router, prefix="/audio", tags=["Audio Processing"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Dental AI Assistant API. Use the /audio/process endpoint to upload audio files for processing."}
