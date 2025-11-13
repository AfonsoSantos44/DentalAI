from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.speech_to_text import transcribe_audio

from app.services.llm_analysis import llm_analysis

from app.utils.file_handler import save_uploaded_file

from app.utils.file_handler import delete_file


router = APIRouter()


@router.post("/process", summary="Upload audio file and return structured dental analysis as JSON")

async def process_audio(file: UploadFile = File(...)):

    if file.content_type not in ["audio/wav", "audio/mpeg", "audio/mp3", "audio/m4a"]:

        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a valid audio file.")


    filepath = save_uploaded_file(file)

    print("DEBUG: Saved file at", filepath)


    try:

        # 1. Transcription

        transcription = transcribe_audio(filepath)

        print("DEBUG: Transcription =", transcription)


        if len(transcription.strip()) == 0:

            raise HTTPException(status_code=500, detail="Transcription failed or resulted in empty text.")


        # 2. GPT Processing

        dental_output = llm_analysis(transcription, runs=5)

        print("DEBUG: Dental Output =", dental_output)


        return {
            "transcription": transcription,
            "dental_analysis": dental_output["final"].dict(),
            "confidence": dental_output["confidence"],
            "all_runs": dental_output["all_runs"]
        }


    except Exception as e:

        import traceback

        print("\n--- ERROR OCCURRED ---")

        traceback.print_exc()

        print("--- END ERROR ---\n")


        raise HTTPException(status_code=500, detail=str(e))


    finally:

        delete_file(filepath)

        print("DEBUG: Deleted file", filepath)

