@router.get("/{analysis_id}")
def get_summaries(analysis_id: int, db: Session = Depends(get_db)):
    obj = get_analysis(db, analysis_id)
    return {
        "pt": obj.summary_pt,
        "en": obj.summary_en
    }
