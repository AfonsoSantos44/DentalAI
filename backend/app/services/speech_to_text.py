import os
import shutil

import whisper

from app.core.config.settings import get_settings

settings = get_settings()


def _resolve_ffmpeg_binary() -> str:
    ffmpeg_binary = settings.ffmpeg_binary or "ffmpeg"
    ffmpeg_path = shutil.which(ffmpeg_binary)
    if ffmpeg_path:
        return ffmpeg_path

    raise RuntimeError(
        "FFmpeg executable not found. Install FFmpeg and ensure it is available on PATH, "
        "or set FFMPEG_BINARY in your .env file (e.g., FFMPEG_BINARY=C:/ffmpeg/bin/ffmpeg.exe)."
    )


def load_whisper_model():
    return whisper.load_model(settings.whisper_model)


model = load_whisper_model()


def transcribe_audio(filepath: str) -> str:
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Audio file not found: {filepath}")

    _resolve_ffmpeg_binary()

    result = model.transcribe(
        filepath,
        fp16=False if settings.whisper_device.lower() == "cpu" else True,
    )
    transcription = result["text"].strip()
    return transcription
