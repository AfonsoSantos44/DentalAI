import difflib
from collections import Counter
from app.services.llm_processing import run_single_extraction
from app.services.validation import validate_dental_output
from app.models.dental_output import DentalOutput



def notes_similar(a: str, b: str, threshold: float = 0.85) -> bool:
    a_clean = a.lower().strip()
    b_clean = b.lower().strip()
    ratio = difflib.SequenceMatcher(None, a_clean, b_clean).ratio()
    return ratio >= threshold



def llm_analysis(transcription: str, runs: int = 5):
    intermediate_results = []

    # STEP — MULTIPLE RUNS
    for i in range(runs):
        print(f"\n------------------------------")
        print(f"DEBUG: Ensemble Run {i+1}/{runs}")
        print(f"------------------------------")

        raw = run_single_extraction(transcription)

        # Pass transcription into validator
        cleaned = validate_dental_output(raw, transcription)
        cleaned_dict = cleaned.dict(exclude={"confidence_score"})

        print(f"RUN {i+1} CLEANED: {cleaned_dict}")

        intermediate_results.append(cleaned_dict)

    # STEP — GROUPING BASED ON STRUCTURE + NOTES SIMILARITY
    buckets = []

    for res in intermediate_results:
        placed = False

        for bucket in buckets:
            # STRUCTURED FIELDS MUST MATCH
            if (
                tuple(res["teeth"]) == bucket["teeth"]
                and tuple(res["diagnosis"]) == bucket["diagnosis"]
                and tuple(res["procedures"]) == bucket["procedures"]
                and res["follow_up_days"] == bucket["follow_up_days"]
            ):
                # NOTES CAN VARY — CHECK SIMILARITY
                if notes_similar(res["notes"], bucket["representative_notes"]):
                    bucket["results"].append(res)
                    placed = True
                    break

        if not placed:
            buckets.append({
                "teeth": tuple(res["teeth"]),
                "diagnosis": tuple(res["diagnosis"]),
                "procedures": tuple(res["procedures"]),
                "follow_up_days": res["follow_up_days"],
                "representative_notes": res["notes"],
                "results": [res],
            })

    # STEP — CHOOSE LARGEST GROUP
    best_bucket = max(buckets, key=lambda b: len(b["results"]))
    confidence = len(best_bucket["results"]) / runs

    print("\n------------------------------")
    print("DEBUG: SMART ENSEMBLE SUMMARY")
    print(f"Number of groups: {len(buckets)}")
    print(f"Best group size: {len(best_bucket['results'])}/{runs}")
    print(f"Confidence Score = {confidence:.2f}")
    print("------------------------------\n")

    final = best_bucket["results"][0]
    final["confidence_score"] = confidence

    return {
        "final": DentalOutput(**final),
        "confidence": confidence,
        "all_runs": intermediate_results,
    }
