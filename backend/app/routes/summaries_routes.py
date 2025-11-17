from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud.analysis_crud import get_analysis


router = APIRouter()


@router.get("/{analysis_id}")
def get_summaries(analysis_id: int, db: Session = Depends(get_db)):
    obj = get_analysis(db, analysis_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return {
        "pt": obj.summary_pt,
        "en": obj.summary_en,
    }
