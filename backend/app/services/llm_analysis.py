from collections import Counter
from difflib import SequenceMatcher
from typing import List, Dict

from app.services.llm_processing import run_single_extraction
from app.services.validation import validate_dental_output
from app.models.dental_output import DentalOutput
from app.utils.logger_file import log  


def notes_similar(a: str, b: str, threshold: float = 0.85) -> bool:
    """Return True if notes are similar enough to be considered equivalent."""
    a_clean = a.lower().strip()
    b_clean = b.lower().strip()
    ratio = SequenceMatcher(None, a_clean, b_clean).ratio()
    return ratio >= threshold


def llm_analysis(transcription: str, runs: int = 5, debug: bool = False) -> Dict:
    intermediate_results: List[Dict] = []

    for i in range(runs):

        if debug:
            log.debug(f"[Ensemble] Starting run {i+1}/{runs}")

        # 1. Run single LLM extraction
        raw = run_single_extraction(transcription)

        # 2. Validate & correct using transcription
        cleaned = validate_dental_output(raw, transcription)
        cleaned_dict = cleaned.dict(exclude={"confidence_score"})

        if debug:
            log.debug(f"[Run {i+1}] CLEANED OUTPUT: {cleaned_dict}")

        intermediate_results.append(cleaned_dict)

    buckets = []

    for res in intermediate_results:
        placed = False

        for bucket in buckets:
            # Structured fields MUST match
            if (
                tuple(res["teeth"]) == bucket["teeth"]
                and tuple(res["diagnosis"]) == bucket["diagnosis"]
                and tuple(res["procedures"]) == bucket["procedures"]
                and res["follow_up_days"] == bucket["follow_up_days"]
            ):
                # Notes match using fuzzy similarity
                if notes_similar(res["notes"], bucket["representative_notes"]):
                    bucket["results"].append(res)
                    placed = True
                    break

        # If no suitable bucket exists → create one
        if not placed:
            buckets.append({
                "teeth": tuple(res["teeth"]),
                "diagnosis": tuple(res["diagnosis"]),
                "procedures": tuple(res["procedures"]),
                "follow_up_days": res["follow_up_days"],
                "representative_notes": res["notes"],
                "results": [res],
            })

    # SELECT BEST BUCKET (majority agreement)
    best_bucket = max(buckets, key=lambda b: len(b["results"]))
    confidence = len(best_bucket["results"]) / runs

    # Log summary
    log.info(f"[Ensemble Summary] Buckets: {len(buckets)}, "
             f"Largest bucket: {len(best_bucket['results'])}/{runs}, "
             f"Confidence={confidence:.2f}")

    final = best_bucket["results"][0]
    final["confidence_score"] = confidence

    return {
        "final": DentalOutput(**final),
        "confidence": confidence
    }
