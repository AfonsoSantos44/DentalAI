from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from app.core.database import get_db
from app.models.sql.models import Analysis


router = APIRouter()


@router.get("/")
def get_stats(db: Session = Depends(get_db)):
    total = db.query(Analysis).count()
    successful = db.query(Analysis).filter(Analysis.status == "success").count()
    avg_processing_ms = (
        db.query(func.avg(Analysis.processing_ms))
        .filter(Analysis.processing_ms.isnot(None))
        .scalar()
    )

    return {
        "total_analyses": total,
        "success_rate": round((successful / total) * 100, 2) if total else 0,
        "avg_processing_ms": int(avg_processing_ms) if avg_processing_ms else 0,
    }
