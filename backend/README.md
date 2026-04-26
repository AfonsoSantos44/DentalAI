# DentalAI

### create a virtual enviroment 
- python -m venv venv 
- venv\Scripts\activate

### using FastAPI and Uvicorn 

### unsing Whisper(Speech-to-Text)

### using LangChain

### using Pydantic for schema validation

### Audio handling tools - python - multipart

### Logging - Loguru

## Running

- test_audio -  python generate_test_audio.py
- pip install -r requirements.txt
- uvicorn app.main:app --log-level debug --port 8001
- endpoint: http://127.0.0.1:8000/
- api-doc: http://localhost:8001/docs#/

## Frontend

- The TypeScript frontend now lives in the top-level `frontend/` directory.
- Verify the build output
    - Check that the frontend emitted files into backend/app/static (index.html + js/css). Example:
        - Windows: `dir backend\app\static`
        - mac/linux: `ls backend/app/static`

- Start the backend (serves the built site)
    1. Activate the virtual environment:
         - Windows: `venv\Scripts\activate`
         - mac/linux: `source venv/bin/activate`
    2. Install Python deps (if not done): `pip install -r requirements.txt`
    3. Run the server: ` python -m uvicorn app.main:app --reload --port 8001`
    4. Open your browser at: `http://localhost:8001/`  
         - API docs: `http://localhost:8001/docs`

- (Optional) Use the frontend dev server for hot reload
    - In a separate shell: `cd frontend && npm run dev`
    - Open the dev-server URL printed in the terminal (commonly `http://localhost:3000`)

## Whisper prerequisites

- Install **FFmpeg** and make sure `ffmpeg` is available in your terminal PATH.
- If FFmpeg is installed in a custom location (common on Windows), set it in `.env`:
  - `FFMPEG_BINARY=C:/ffmpeg/bin/ffmpeg.exe`
- Without FFmpeg, `/audio/process_full` will fail during transcription with a `transcription_failed` error.
