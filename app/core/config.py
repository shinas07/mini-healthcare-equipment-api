from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Mini Healthcare Equipment API"
    app_version: str = "0.1.0"
    debug: bool = False
    api_prefix: str = "/api"

    # Database settings
    database_url: str | None = None




@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()