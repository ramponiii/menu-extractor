from loguru import logger
from pydantic_settings import BaseSettings, SettingsConfigDict


class Secrets(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )
    cohere_settings__client_name: str
    cohere_settings__api_key: str


# note: Secrets() is populated from the .env file, which is not detected by Pylance
secrets = Secrets()  # type: ignore

__all__ = ["logger", "secrets"]
