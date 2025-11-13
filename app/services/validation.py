import re
from typing import List
from pydantic import ValidationError
from app.models.dental_output import DentalOutput



VALID_TOOTH_NUMBERS = set(range(1, 48)) 


def extract_spoken_teeth(transcription: str) -> List[int]:
    text = transcription.lower()
    teeth = set()

    # Pattern 1 — ranges (2–11)
    for a, b in re.findall(r"\b(\d{1,2})\s*(?:–|-)\s*(\d{1,2})\b", text):
        lo, hi = sorted([int(a), int(b)])
        teeth.update(range(lo, hi + 1))

    # Pattern 2 — explicit “tooth 12”
    for num in re.findall(r"(?:tooth|teeth|number)\s+(\d{1,2})", text):
        teeth.add(int(num))

    # Pattern 3 — “12 or 22”
    for num in re.findall(r"(?:or|and|e)\s+(\d{1,2})", text):
        teeth.add(int(num))

    # Pattern 4 — fallback: capture numbers near “tooth”
    fallback_matches = re.findall(r"\b(\d{1,2})\b", text)
    for idx, num in enumerate(fallback_matches):
        num = int(num)
        # Only add if number is close to other extracted teeth
        if num not in teeth:
            # If spoken teeth already include a neighbor or paired number
            if any(abs(num - t) <= 1 for t in teeth):
                teeth.add(num)

    return sorted(t for t in teeth if 1 <= t <= 48)




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
            print("WARNING: LLM changed tooth numbers. Fixing to spoken teeth.")
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
