from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    LLAMA_URL: str
    LLAMA_MODEL: str
    LLAMA_PORT: int = 8080
    LLAMA_CTX_SIZE: int = 4096
    LLAMA_THREADS: int = 8

    model_config = SettingsConfigDict(
        env_file=f"{BASE_DIR}/.env",
        env_file_encoding="utf-8",
    )

settings = Settings()