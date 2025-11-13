from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.speech_to_text import transcribe_audio
from app.services.llm_processing import process_transcription
from app.services.file_handling import save_uploaded_file

router = APIRouter()

@router.post("/process", summary="Upload audio file and return structured dental analysis as JSON")
async def process_audio(file: UploadFile = File(...)):
    if file.content_type not in ["audio/wav", "audio/mpeg", "audio/mp3", "audio/m4a"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a valid audio file.")

    filepath = save_uploaded_file(file)

    transcription = transcribe_audio(filepath)

    if len(transcription) == 0:
        raise HTTPException(status_code=500, detail="Transcription failed or resulted in empty text.")

    dental_output = process_transcription(transcription)


    return{
        "transcription": transcription,
        "dental_analysis": dental_output.dict()
    }