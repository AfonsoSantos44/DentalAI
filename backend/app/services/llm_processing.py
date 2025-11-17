from langchain_openai import ChatOpenAI

from langchain_core.output_parsers import PydanticOutputParser

from app.models.dental_output import DentalOutput

from app.services.validation import validate_dental_output

from app.core.config.settings import get_settings


settings = get_settings()

print("DEBUG OPENAI KEY LOADED:", settings.openai_api_key[:8] + "...")



model = ChatOpenAI(

    model=settings.openai_model,

    api_key=settings.openai_api_key,      

    temperature=settings.openai_temperature,

)



# Create output parser

parser = PydanticOutputParser(pydantic_object=DentalOutput)


def run_single_extraction(transcription: str) -> dict:


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

    "notes" MUST always be a full sentence summary of key findings.
    NEVER leave "notes" empty.
    Always rewrite the notes using the patient’s words and the clinician’s actions.
    Be aware that if we have number of teeth like this 2-4, it means teeth 2, 3, and 4 for example.


    Schema:

    {parser.get_format_instructions()}


    --- TRANSCRIPTION ---

    {transcription}
    """


    response = model.invoke(prompt)


    parsed_output = parser.parse(response.content)


    return parsed_output.dict()

