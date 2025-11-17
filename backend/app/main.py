from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

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

static_dir = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=static_dir), name="static")


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

@app.get("/", response_class=HTMLResponse)
async def root():
    index_path = static_dir / "index.html"
    if index_path.exists():
        return index_path.read_text(encoding="utf-8")
    return "<h1>Dental AI Assistant</h1><p>Static assets missing. Check deployment.</p>"
