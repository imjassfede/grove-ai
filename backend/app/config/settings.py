from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Growth AI"
    anthropic_api_key: str
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/growthai"
    cors_origins: list[str] = ["http://localhost:3000"]
    debug: bool = False

    model_config = {"env_file": ".env"}


@lru_cache
def get_settings() -> Settings:
    return Settings()
