from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
from app.models.dental_output import DentalOutput
from app.services.validation import validate_dental_output
from app.config.settings import get_settings

settings = get_settings()
print("DEBUG OPENAI KEY LOADED:", settings.openai_api_key[:8] + "...")


model = ChatOpenAI(
    model=settings.openai_model,
    api_key=settings.openai_api_key,      
    temperature=settings.openai_temperature,
)


# Create output parser
parser = PydanticOutputParser(pydantic_object=DentalOutput)

def process_dental_transcription(transcription: str) -> DentalOutput:

    prompt = f"""
    You are a professional dental AI assistant.

    Return ONLY this JSON structure:

    {{
    "teeth": [int],
    "diagnosis": [str],
    "procedures": [str],
    "follow_up_days": int,
    "notes": str
    }}

    Do NOT rename keys.
    Do NOT include extra fields.

    Schema:
    {parser.get_format_instructions()}

    --- TRANSCRIPTION ---
    {transcription}
    """

    response = model.invoke(prompt)

    parsed_output = parser.parse(response.content)

    return validate_dental_output(parsed_output.dict())
