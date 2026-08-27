from functools import lru_cache

from pydantic import AliasChoices, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Grove"
    google_api_key: str = Field(validation_alias=AliasChoices("GEMINI_API_KEY", "GOOGLE_API_KEY"))
    database_url: str = "sqlite+aiosqlite:///./grove.db"
    cors_origins: list[str] = ["http://localhost:3000"]
    debug: bool = False
    posthog_api_key: str | None = None
    posthog_host: str = "https://us.i.posthog.com"
    brevo_api_key: str | None = Field(default=None, validation_alias=AliasChoices("BREVO_API_KEY", "Brevo_API"))
    brevo_list_id: int | None = None
    n8n_webhook_url: str | None = None

    @field_validator("database_url", mode="before")
    @classmethod
    def default_database_url(cls, value):
        if value is None or not str(value).strip():
            return "sqlite+aiosqlite:///./grove.db"
        return value

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value):
        if value is None or not str(value).strip():
            return ["http://localhost:3000"]
        if isinstance(value, list):
            return value
        raw = str(value).strip()
        if raw.startswith("["):
            import json
            return json.loads(raw)
        return [origin.strip() for origin in raw.split(",") if origin.strip()]

    model_config = SettingsConfigDict(env_file=".env", extra="ignore", populate_by_name=True)


@lru_cache
def get_settings() -> Settings:
    return Settings()
