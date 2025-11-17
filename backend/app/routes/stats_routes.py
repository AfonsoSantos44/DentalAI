@router.get("/")
def get_stats(db: Session = Depends(get_db)):
    total = db.query(Analysis).count()
    return {
        "total_analyses": total,
        "avg_processing": "45s",
        "success_rate": "98%"
    }
