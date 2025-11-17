from sqlalchemy.orm import Session
from app.models.sql.models import Analysis

def create_analysis(
    db: Session,
    transcription: str,
    clinical_json: dict,
    *,
    processing_ms: int | None = None,
    status: str = "success",
):
    obj = Analysis(
        transcription=transcription,
        clinical_json=clinical_json,
        processing_ms=processing_ms,
        status=status,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def list_analyses(db: Session, *, skip: int = 0, limit: int = 20, search: str | None = None):
    query = db.query(Analysis)
    if search:
        query = query.filter(Analysis.transcription.ilike(f"%{search}%"))
    total = query.count()
    records = (
        query.order_by(Analysis.id.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return records, total

def get_analysis(db: Session, analysis_id: int):
    return db.query(Analysis).filter(Analysis.id == analysis_id).first()

def save_summaries(db: Session, analysis_id: int, pt: str, en: str):
    analysis = get_analysis(db, analysis_id)
    analysis.summary_pt = pt
    analysis.summary_en = en
    db.commit()
    return analysis
