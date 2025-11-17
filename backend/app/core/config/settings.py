from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    DATABASE_URL: str
    openai_api_key: str
    openai_model: str = "gpt-4o-mini"
    openai_temperature: float = 0.0

    whisper_model: str = "base"
    whisper_device: str = "cpu"
    
    upload_folder: str = "uploads"
    temp_audio_folder: str = "temp_audio"

    service_name: str = "DentalAI Microservice"
    environment: str = "development"

    model_config = SettingsConfigDict(
        env_file="C:/Users/reiaf/Desktop/DentalAi/DentalAI/backend/.env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

@lru_cache()
def get_settings() -> Settings:
    return Settings()
