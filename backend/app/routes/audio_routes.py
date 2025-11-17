from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from time import perf_counter

from app.core.database import get_db
from app.services.speech_to_text import transcribe_audio
from app.services.llm_analysis import llm_analysis
from app.services.llm_scribe import run_scribe_transformation

from app.utils.file_handler import save_uploaded_file, delete_file
from app.crud.analysis_crud import create_analysis, save_summaries

router = APIRouter()

VALID_AUDIO_TYPES = {
    "audio/wav", "audio/mpeg", 
    "audio/mp3", "audio/m4a"
}


def validate_audio(file: UploadFile):
    if file.content_type not in VALID_AUDIO_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Please upload an audio file (WAV, MP3, M4A)."
        )


def _error(status_code: int, code: str, message: str):
    raise HTTPException(status_code=status_code, detail={"code": code, "message": message})


@router.post("/process_full", summary="Full pipeline: STT → Clinical JSON → PT/EN Summaries")
async def process_full(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Validate MIME type
    validate_audio(file)

    try:
        filepath = save_uploaded_file(file)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    start_time = perf_counter()
    processing_ms = None
    try:
        # 1 — Transcription
        try:
            transcription = transcribe_audio(filepath)
        except Exception as exc:  # pragma: no cover - passthrough wrapper
            _error(502, "transcription_failed", f"Speech-to-text failed: {exc}")

        if not transcription.strip():
            _error(422, "empty_transcription", "Empty transcription, check audio quality.")

        # 2 — Clinical Extraction (Ensemble)
        try:
            clinical_result = llm_analysis(transcription, runs=5)
        except Exception as exc:  # pragma: no cover - passthrough wrapper
            _error(502, "analysis_failed", f"Clinical extraction failed: {exc}")
        clinical_json = clinical_result["final"].dict()
        confidence = clinical_result["confidence"]

        # 3 — Summaries PT/EN
        try:
            scribe_output = run_scribe_transformation(transcription, clinical_json)
        except Exception as exc:  # pragma: no cover - passthrough wrapper
            _error(502, "summaries_failed", f"Summary generation failed: {exc}")

        # 4 — Save to PostgreSQL
        processing_ms = int((perf_counter() - start_time) * 1000)
        analysis = create_analysis(
            db=db,
            transcription=transcription,
            clinical_json=clinical_json,
            processing_ms=processing_ms,
            status="success",
        )

        save_summaries(
            db=db,
            analysis_id=analysis.id,
            pt=scribe_output.clinical_summary_pt,
            en=scribe_output.clinical_summary_en
        )


        # 5 — Return ID (frontend uses this to redirect to /results/:id)
        return {
            "analysis_id": analysis.id,
            "confidence": confidence,
            "processing_ms": processing_ms,
        }

    finally:
        if filepath:
            delete_file(filepath)
