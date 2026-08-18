import logging
from pathlib import Path

from pydantic import ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)

# Locate optional local .env relative to this file
ENV_PATH = Path(__file__).resolve().parent.parent / ".env"


class Settings(BaseSettings):
    LLAMA_URL: str
    LLAMA_MODEL: str
    LLAMA_PORT: int
    LLAMA_CTX_SIZE: int
    LLAMA_THREADS: int

    model_config = SettingsConfigDict(
        # Pass path if file exists, else None.
        # Python won't throw a FileNotFoundError if it's missing!
        env_file=str(ENV_PATH) if ENV_PATH.is_file() else None,
        env_file_encoding="utf-8",
        extra="ignore",
    )


try:
    settings = Settings()
except ValidationError as e:
    logger.error("Missing required environment variables:\n%s", e)
    raise SystemExit(1) from e
