"""Application settings."""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Centralized runtime settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    app_name: str = "Mini Healthcare Equipment API"
    app_version: str = "0.1.0"
    app_env: str = "development"
    debug: bool = False
    api_prefix: str = Field(default="", alias="API_PREFIX")

    database_url: str | None = Field(default=None, alias="DATABASE_URL")
    db_user: str | None = Field(default=None, alias="DBUSER")
    db_pass: str | None = Field(default=None, alias="DBPASS")
    db_host: str | None = Field(default=None, alias="DBHOST")
    db_name: str | None = Field(default=None, alias="DBNAME")
    db_port: int = Field(default=5432, alias="DBPORT")

    @property
    def sqlalchemy_database_uri(self) -> str:
        """Resolve async SQLAlchemy database URI with SQLite fallback."""
        if self.database_url:
            return self.database_url

        if all([self.db_user, self.db_pass, self.db_host, self.db_name]):
            return (
                f"postgresql+asyncpg://{self.db_user}:{self.db_pass}"
                f"@{self.db_host}:{self.db_port}/{self.db_name}"
            )

        return "sqlite+aiosqlite:///./mini_healthcare.db"


@lru_cache
def get_settings() -> Settings:
    """Return cached settings instance."""
    return Settings()


settings = get_settings()
