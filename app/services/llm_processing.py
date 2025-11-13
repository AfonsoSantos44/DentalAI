from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
from app.models.dental_output import DentalOutput
from app.services.validation import sanitize_llm_output

model = ChatOpenAI(
    model="gpt-4o-mini", 
    temperature=0,
)

# Create output parser
parser = PydanticOutputParser(pydantic_object=DentalOutput)

def process_dental_transcription(transcription: str) -> DentalOutput:
    prompt = f"""
    You are a professional dental AI assistant.

    Extract structured dental analysis from the following transcription of a dental consultation:

    --- TRANSCRIPTION ---
    {transcription}
    ----------------------

    Follow this JSON schema exactly:
    {parser.get_format_instructions()}
    """


    response = model.invoke(prompt)

    parsed_output = parser.parse(response.content)

    return sanitize_llm_output(parsed_output.dict())
