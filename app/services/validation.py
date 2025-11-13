import re
from typing import List
from pydantic import ValidationError
from app.models.dental_output import DentalOutput



VALID_TOOTH_NUMBERS = set(range(1, 48)) 


def extract_spoken_teeth(transcription: str) -> List[int]:
  
    text = transcription.lower()
    teeth: set[int] = set()

   
    range_matches = re.findall(r"\b(\d{1,2})\s*(?:–|-)\s*(\d{1,2})\b", text)
    for a, b in range_matches:
        start, end = int(a), int(b)
        lo, hi = min(start, end), max(start, end)
        for t in range(lo, hi + 1):
            teeth.add(t)

    context_pattern = r"(?:tooth|teeth|on|number|dente|elemento)\s+(\d{1,2})"
    singles = re.findall(context_pattern, text)
    for num in singles:
        teeth.add(int(num))

    and_pattern = r"(?:and|e)\s+(\d{1,2})"
    and_nums = re.findall(and_pattern, text)
    for num in and_nums:
        teeth.add(int(num))

    valid_teeth = sorted(t for t in teeth if 1 <= t <= 48)

    return valid_teeth



def validate_teeth_positions(teeth: List[int]) -> List[int]:
   
    return sorted(set([t for t in teeth if t in VALID_TOOTH_NUMBERS]))


def validate_strings(strings: List[str]) -> List[str]:
    cleaned = []
    for s in strings:
        if isinstance(s, str):
            s = s.strip()
            if len(s) > 0:
                cleaned.append(s)
    return list(dict.fromkeys(cleaned))


def validate_dental_output(data: dict, transcription: str) -> DentalOutput:
    try:
        raw_teeth = data.get("teeth", [])
        raw_diagnosis = data.get("diagnosis", [])
        raw_procedures = data.get("procedures", [])
        follow_up_days = data.get("follow_up_days", 30)
        notes = data.get("notes", "").strip()

        # 1. Sanitize LLM teeth
        clean_teeth = validate_teeth_positions(raw_teeth)

        # 2. Extract ACTUAL spoken teeth
        spoken_teeth = extract_spoken_teeth(transcription)

        if set(clean_teeth) != set(spoken_teeth):
            print("⚠️ WARNING: LLM changed tooth numbers. Fixing to spoken teeth.")
            clean_teeth = validate_teeth_positions(spoken_teeth)

        # Clean remaining fields
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
            notes=notes,
        )

    except ValidationError as e:
        raise ValueError(f"Error validating LLM output: {e}")
