from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    # -------------------------
    # OpenAI / LLM Configuration
    # -------------------------
    openai_api_key: str
    openai_model: str = "gpt-4o-mini"
    openai_temperature: float = 0.0

    # -------------------------
    # Whisper Configuration
    # -------------------------
    whisper_model: str = "base"         
    whisper_device: str = "cpu"         

    # -------------------------
    # File Handling
    # -------------------------
    upload_folder: str = "uploads"
    temp_audio_folder: str = "temp_audio"

    # -------------------------
    # Global service settings
    # -------------------------
    service_name: str = "DentalAI Microservice"
    environment: str = "development"     
    # Load values from .env file automatically
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


# A cached instance so settings load only once
@lru_cache()
def get_settings() -> Settings:
    return Settings()
