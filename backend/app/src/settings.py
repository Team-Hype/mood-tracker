"""Application settings loaded from environment variables and .env file."""

__all__ = ["settings"]

import ssl
from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class DefaultSettings(BaseSettings):
    """Central configuration for the Mood Tracker backend.

    Values are read from environment variables or the .env file located
    at the repository root.  All fields can be overridden at runtime by
    setting the corresponding environment variable.
    """

    model_config = SettingsConfigDict(env_file=Path(__file__).parent.parent.parent.parent / ".env", extra="ignore")

    APP_NAME: str = "mood-tracker-backend"
    PATH_PREFIX: str = "/api/v1"
    APP_HOST: str = "0.0.0.0"
    PROTOCOL: str = "http"
    CURRENT_HOST: str = "0.0.0.0"
    APP_PORT: int = 5000

    POSTGRES_DB: str = "postgres"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_PORT: int = 5432
    DB_CONNECT_RETRY: int = 20
    DB_POOL_SIZE: int = 15
    DB_USE_SSL: bool = False
    DB_SSL_KEY_PATH: Optional[str] = None

    SWAGGER_PATH: Optional[str] = "/swagger"
    REDOC_PATH: Optional[str] = None

    @property
    def current_host_url(self) -> str:
        """Return the full base URL of the current host including protocol."""
        return f"{self.PROTOCOL}://{self.CURRENT_HOST}"

    @property
    def database_settings(self) -> dict:
        """Return a dict of database connection parameters."""
        return {
            "database": self.POSTGRES_DB,
            "user": self.POSTGRES_USER,
            "password": self.POSTGRES_PASSWORD,
            "host": self.POSTGRES_HOST,
            "port": self.POSTGRES_PORT,
        }

    @property
    def database_uri(self) -> str:
        """Async database uri"""
        return "postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}".format(**self.database_settings)

    @property
    def database_uri_sync(self) -> str:
        """Sync database uri"""
        return "postgresql://{user}:{password}@{host}:{port}/{database}".format(**self.database_settings)

    @property
    def db_context(self) -> dict:
        """Return SQLAlchemy connect_args dict, including SSL context when enabled."""
        if not self.DB_USE_SSL:
            return {}
        ssl_context = ssl.create_default_context(cafile=self.DB_SSL_KEY_PATH)
        ssl_context.verify_mode = ssl.CERT_REQUIRED
        return {"ssl": ssl_context}


settings = DefaultSettings()
