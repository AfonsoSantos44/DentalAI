from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.sql.models import Analysis


router = APIRouter()


@router.get("/")
def get_stats(db: Session = Depends(get_db)):
    total = db.query(Analysis).count()
    return {
        "total_analyses": total,
        "avg_processing": "45s",
        "success_rate": "98%",
    }
