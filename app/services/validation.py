from typing import List
from pydantic import ValidationError
from app.models.dental_output import DentalOutput

VALID_TOOTH_NUMBERS = set(range(1, 33))

def validate_teeth_positions(teeth: List[int]) -> List[int]:
    cleaned_teeth = []
    for t in teeth:
        if isinstance(t, int) and t in VALID_TOOTH_NUMBERS:
            cleaned_teeth.append(t)
    
    return sorted(set(cleaned_teeth))

def validate_strings(strings: List[str]) -> List[str]:
    cleaned = []

    for s in strings:
        if not isinstance(s, str):
            continue
        s = s.strip().lower()
        if len(s) > 0:
            cleaned.append(s)

    return list(dict.fromkeys(cleaned)) 
    
def validate_dental_output(data: dict) -> DentalOutput:
    try:
        # Accept either "teeth" or "teeth_positions"
        if "teeth_positions" in data:
            data["teeth"] = data.pop("teeth_positions")

        raw_teeth = data.get("teeth", [])
        raw_diagnosis = data.get("diagnosis", [])
        raw_procedures = data.get("procedures", [])
        follow_up_days = data.get("follow_up_days", 30)
        notes = data.get("notes", "").strip()

        clean_teeth = validate_teeth_positions(raw_teeth)
        clean_diagnosis = validate_strings(raw_diagnosis)
        clean_procedures = validate_strings(raw_procedures)

        if not isinstance(notes, str):
            notes = ""

        if not isinstance(follow_up_days, int) or follow_up_days < 0:
            follow_up_days = 30

        return DentalOutput(
            teeth=clean_teeth,
            diagnosis=clean_diagnosis,
            procedures=clean_procedures,
            follow_up_days=follow_up_days,
            notes=notes
        )

    except ValidationError as e:
        raise ValueError(f"Error validating LLM output: {e}")
