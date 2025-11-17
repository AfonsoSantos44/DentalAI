from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import Base, engine
from app.routes.analyses_routes import router as analyses_router
from app.routes.audio_routes import router as audio_router
from app.routes.stats_routes import router as stats_router
from app.routes.summaries_routes import router as summaries_router


app = FastAPI(
    title="Dental AI Assistant",
    description="Processes audio → transcription → dental structured JSON",
    version="1.0.0",
)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

# ---- Allow backend/mobile to call this API ----
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(audio_router, prefix="/audio", tags=["Audio Processing"])
app.include_router(analyses_router, prefix="/analyses", tags=["Analyses"])
app.include_router(summaries_router, prefix="/summaries", tags=["Summaries"])
app.include_router(stats_router, prefix="/stats", tags=["Stats"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Dental AI Assistant API. Use the /audio/process endpoint to upload audio files for processing."}
