from pathlib import Path
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    openai_api_key: str
    openai_model: str = "gpt-4o-mini"
    openai_temperature: float = 0.0

    whisper_model: str = "base"
    whisper_device: str = "cpu"
    ffmpeg_binary: str = "ffmpeg"

    upload_folder: str = "uploads"
    temp_audio_folder: str = "temp_audio"

    service_name: str = "DentalAI Microservice"
    environment: str = "development"

    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).resolve().parents[3] / ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

@lru_cache()
def get_settings() -> Settings:
    return Settings()
