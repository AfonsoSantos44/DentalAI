from typing import List, Dict
from collections import Counter
from app.services.llm_processing import run_single_extraction
from app.services.validation import validate_dental_output, DentalOutput

def make_hashable(x):
    if isinstance(x, dict):
        return tuple(sorted((k, make_hashable(v)) for k, v in x.items()))
    if isinstance(x, list):
        return tuple(make_hashable(i) for i in x)
    return x

def llm_analysis(transcription: str, runs: int = 5) -> DentalOutput:
    results = []

    # Run LLM N times
    for i in range(runs):
        print(f"DEBUG: Ensemble run {i+1}/{runs}")
        
        raw_dict = run_single_extraction(transcription)  
        cleaned = validate_dental_output(raw_dict)        
        result_dict = cleaned.dict(exclude={"confidence_score"})
        
        results.append(result_dict)

    # Convert each dict to hashable form
    hashable_results = [make_hashable(r) for r in results]

    # Count duplicates
    counter = Counter(hashable_results)
    best_hashable, count = counter.most_common(1)[0]

    confidence = count / runs

    # Convert hashable tuple back to dict
    best_result = dict(best_hashable)

    # Add confidence
    best_result["confidence_score"] = confidence

    return DentalOutput(**best_result)
