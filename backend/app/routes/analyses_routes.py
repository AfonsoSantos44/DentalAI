@router.get("/")
def get_all(db: Session = Depends(get_db)):
    return list_analyses(db)
