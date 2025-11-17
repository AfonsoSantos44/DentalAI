from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud.analysis_crud import get_analysis, list_analyses


router = APIRouter()


def _serialize_analysis(analysis):
    return {
        "id": analysis.id,
        "transcription": analysis.transcription,
        "clinical_json": analysis.clinical_json,
        "summary_pt": analysis.summary_pt,
        "summary_en": analysis.summary_en,
        "processing_ms": analysis.processing_ms,
        "status": analysis.status,
        "created_at": analysis.created_at.isoformat() if analysis.created_at else None,
    }


@router.get("/")
def get_all(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    q: str | None = Query(None, description="Optional search within transcriptions"),
    db: Session = Depends(get_db),
):
    skip = (page - 1) * page_size
    analyses, total = list_analyses(db, skip=skip, limit=page_size, search=q)
    return {
        "items": [_serialize_analysis(analysis) for analysis in analyses],
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total": total,
            "total_pages": (total + page_size - 1) // page_size,
        },
        "filters": {"query": q},
    }


@router.get("/{analysis_id}")
def get_one(analysis_id: int, db: Session = Depends(get_db)):
    analysis = get_analysis(db, analysis_id)
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return _serialize_analysis(analysis)
