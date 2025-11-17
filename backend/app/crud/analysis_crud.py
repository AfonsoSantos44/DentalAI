from sqlalchemy.orm import Session
from app.models.sql.models import Analysis

def create_analysis(db: Session, transcription: str, clinical_json: dict):
    obj = Analysis(
        transcription=transcription,
        clinical_json=clinical_json,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def list_analyses(db: Session):
    return db.query(Analysis).order_by(Analysis.id.desc()).all()

def get_analysis(db: Session, analysis_id: int):
    return db.query(Analysis).filter(Analysis.id == analysis_id).first()

def save_summaries(db: Session, analysis_id: int, pt: str, en: str):
    analysis = get_analysis(db, analysis_id)
    analysis.summary_pt = pt
    analysis.summary_en = en
    db.commit()
    return analysis
