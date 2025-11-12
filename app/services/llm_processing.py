from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
from app.models.dental_output import DentalOutput

model = ChatOpenAI(
    model_name="gpt-4",
    temperature=0,
)

parser = PydanticOutputParser(pydantic_object=DentalOutput)

def process_dental_transcription(transcription:str) -> DentalOutput:
    prompt = f"""
    You are a professional dental AI assistant.

    Extract structured dental analysis from the following transcription of a dental consultation:

    ---TRANSCRIPTION---
    {transcription}
    -----------------

    Follow the output format strictly as defined below:
    {parser.get_format_instructions()}
    """

    response = model.invoke(prompt)
    dental_output = parser.parse(response)
    return dental_output