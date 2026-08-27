from functools import lru_cache

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Grove"
    google_api_key: str = Field(validation_alias=AliasChoices("GEMINI_API_KEY", "GOOGLE_API_KEY"))
    database_url: str = "sqlite+aiosqlite:///./grove.db"
    cors_origins_raw: str = Field(default="http://localhost:3000", validation_alias="CORS_ORIGINS")
    debug: bool = False
    posthog_api_key: str | None = None
    posthog_host: str = "https://us.i.posthog.com"
    brevo_api_key: str | None = Field(default=None, validation_alias=AliasChoices("BREVO_API_KEY", "Brevo_API"))
    brevo_list_id: int | None = None
    n8n_webhook_url: str | None = None

    @property
    def cors_origins(self) -> list[str]:
        value = self.cors_origins_raw.strip()
        if not value:
            return ["http://localhost:3000"]
        # Render may provide either a comma-separated string or JSON-style array.
        if value.startswith("[") and value.endswith("]"):
            value = value[1:-1].replace('"', "").replace("'", "")
        return [origin.strip() for origin in value.split(",") if origin.strip()]

    @field_validator("database_url", mode="before")
    @classmethod
    def empty_database_url_uses_sqlite(cls, value):
        return value or "sqlite+aiosqlite:///./grove.db"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore", populate_by_name=True)


@lru_cache
def get_settings() -> Settings:
    return Settings()
