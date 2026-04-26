import json
import re
from typing import Any


def _strip_markdown_fences(text: str) -> str:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s*```$", "", cleaned)
    return cleaned.strip()


def _normalize_json_text(text: str) -> str:
    cleaned = _strip_markdown_fences(text)
    cleaned = cleaned.replace("“", '"').replace("”", '"').replace("’", "'")

    replacements = {
        r"\bNone\b": "null",
        r"\bTrue\b": "true",
        r"\bFalse\b": "false",
    }
    for pattern, replacement in replacements.items():
        cleaned = re.sub(pattern, replacement, cleaned)

    cleaned = re.sub(r",\s*([}\]])", r"\1", cleaned)
    return cleaned


def _extract_json_candidate(text: str) -> str:
    normalized = _normalize_json_text(text)

    for start_char in ("{", "["):
        start = normalized.find(start_char)
        if start == -1:
            continue
        decoder = json.JSONDecoder()
        try:
            parsed, _ = decoder.raw_decode(normalized[start:])
            return json.dumps(parsed, ensure_ascii=False)
        except json.JSONDecodeError:
            continue

    return normalized


def parse_with_repair_and_retry(
    parser: Any,
    model: Any,
    base_prompt: str,
    initial_content: str,
    max_retries: int = 2,
) -> Any:
    attempts: list[str] = [initial_content, _extract_json_candidate(initial_content)]
    parse_errors = []

    for candidate in attempts:
        try:
            return parser.parse(candidate)
        except Exception as exc:
            parse_errors.append(str(exc))

    retry_prompt = (
        f"{base_prompt}\n\n"
        "Your previous response was invalid JSON for the required schema. "
        "Return only valid JSON that strictly follows the schema. "
        "Do not include markdown, commentary, or extra keys."
    )

    for _ in range(max_retries):
        retry_response = model.invoke(retry_prompt)
        repaired_candidate = _extract_json_candidate(retry_response.content)
        try:
            return parser.parse(repaired_candidate)
        except Exception as exc:
            parse_errors.append(str(exc))

    joined = " | ".join(parse_errors[-3:])
    raise ValueError(f"Failed to parse model JSON after repair/retry attempts: {joined}")
