from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Grove"
    google_api_key: str
    database_url: str = "sqlite+aiosqlite:///./grove.db"
    cors_origins: list[str] = ["http://localhost:3000"]
    debug: bool = False

    # Optional, zero-cost-until-needed growth infrastructure.
    posthog_api_key: str | None = None
    posthog_host: str = "https://us.i.posthog.com"
    brevo_api_key: str | None = None
    brevo_list_id: int | None = None
    n8n_webhook_url: str | None = None

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
