from __future__ import annotations

from functools import lru_cache
from typing import Literal, Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Runbook Grounding Agent"
    environment: str = "dev"
    debug: bool = False

    database_url: str = "sqlite:///./runbook_qa.db"
    log_level: str = "INFO"

    provider_mode: Literal["auto", "mock", "openai"] = "auto"
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-5-mini"

    retrieval_mode: Literal["keyword", "embedding"] = "keyword"
    min_confidence: float = 0.35
    max_chunks: int = 4

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    @property
    def normalized_database_url(self) -> str:
        if self.database_url.startswith("postgres://"):
            return self.database_url.replace("postgres://", "postgresql://", 1)
        return self.database_url


@lru_cache
def get_settings() -> Settings:
    return Settings()
