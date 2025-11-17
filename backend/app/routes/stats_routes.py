from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

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

    success_rate = f"{int((successful / total) * 100)}%" if total else "--"
    avg_processing = f"{int(avg_processing_ms)} ms" if avg_processing_ms else "--"

    return {
        "total_analyses": total,
        "avg_processing": avg_processing,
        "success_rate": success_rate,
    }
