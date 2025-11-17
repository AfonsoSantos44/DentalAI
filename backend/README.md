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
- Run `npm install` and `npm run build` from `frontend/` to emit assets into `backend/app/static`, which FastAPI serves at runtime.
