from sqlalchemy import Column, Integer, Text, TIMESTAMP, JSON, String
from sqlalchemy.sql import func
from app.core.database import Base

class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)
    transcription = Column(Text, nullable=False)
    clinical_json = Column(JSON, nullable=False)
    summary_pt = Column(Text)
    summary_en = Column(Text)
    processing_ms = Column(Integer)
    status = Column(String(50), default="success")
    created_at = Column(TIMESTAMP, server_default=func.now())
