import os
import whisper
from app.config.settings import get_settings

settings = get_settings()

def load_whisper_model():
    return whisper.load_model(settings.whisper_model)

model = load_whisper_model()

def transcribe_audio(filepath):
    result = model.transcribe(filepath)
    transcription = result["text"].strip()
    return transcription
