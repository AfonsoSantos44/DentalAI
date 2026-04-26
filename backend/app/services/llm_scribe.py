from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser

from app.core.config.settings import get_settings
from app.models.dental_scribe_output import DentalScribeOutput
from app.services.json_resilience import parse_with_repair_and_retry

settings = get_settings()

scribe_model = ChatOpenAI(
    model=settings.openai_model,
    api_key=settings.openai_api_key,
    temperature=0.2
)

scribe_parser = PydanticOutputParser(pydantic_object=DentalScribeOutput)

SCRIBE_PROMPT_TEMPLATE = """
You are a professional dental AI scribe.

Your task is to convert the consultation transcript + the structured clinical JSON
into a detailed human-readable dental report in BOTH Portuguese (PT-PT) and English (US).

You MUST strictly follow this JSON schema:

{{
  "reason_for_appointment": "string or null",

  "clinical_summary_pt": "string",
  "clinical_summary_en": "string",

  "patient_explanation_pt": "string",
  "patient_explanation_en": "string",

  "recommended_treatments_pt": "string",
  "recommended_treatments_en": "string",

  "next_steps_pt": "string",
  "next_steps_en": "string"
}}

--- RULES ---
1. Produce ONLY valid JSON. No markdown, no extra words.
2. Portuguese MUST be European Portuguese (Portugal).
3. Patient-friendly sections must be simple and empathetic.
4. Clinical summaries must be concise and medically correct.
5. recommended_treatments_* must be realistic and based on findings.
6. reason_for_appointment should be extracted if possible; else null.

--- INPUT DATA ---

[TRANSCRIPTION]
{transcription}

[CLINICAL_JSON]
{clinical_json}

Generate the final JSON now.

Schema:
{schema}
"""


def run_scribe_transformation(transcription: str, clinical_output: dict) -> DentalScribeOutput:
    prompt = SCRIBE_PROMPT_TEMPLATE.format(
        transcription=transcription,
        clinical_json=clinical_output,
        schema=scribe_parser.get_format_instructions()
    )

    response = scribe_model.invoke(prompt)
    parsed = parse_with_repair_and_retry(
        parser=scribe_parser,
        model=scribe_model,
        base_prompt=prompt,
        initial_content=response.content,
        max_retries=2,
    )
    return parsed
