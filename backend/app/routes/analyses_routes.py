from fastapi import APIRouter, Depends, HTTPException
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
        "created_at": analysis.created_at.isoformat() if analysis.created_at else None,
    }


@router.get("/")
def get_all(db: Session = Depends(get_db)):
    analyses, total = list_analyses(db)
    return [_serialize_analysis(analysis) for analysis in analyses]


@router.get("/{analysis_id}")
def get_one(analysis_id: int, db: Session = Depends(get_db)):
    analysis = get_analysis(db, analysis_id)
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return _serialize_analysis(analysis)
