from pydantic import BaseModel
from typing import Optional

class DentalScribeOutput(BaseModel):
    """
    Dental Scribe Output Model
    """

    reason_for_appointment: Optional[str] = None

    clinical_summary_pt: str
    clinical_summary_en: str

    patient_explanation_pt: str
    patient_explanation_en: str

    recommended_treatments_pt: str
    recommended_treatments_en: str

    next_steps_pt: str
    next_steps_en: str
