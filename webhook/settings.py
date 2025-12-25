from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Settings for the webhook server.

    Attributes:
        DEBUG: Enable debug mode for development.
        LOG_LEVEL: Logging level (e.g., DEBUG, INFO, WARNING, ERROR).
        SERVER_HOST: Host address for the server to bind to.
        SERVER_PORT: Port number for the server to listen on.
        WEBHOOK_HOST: Host address for webhook callbacks.
    """

    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"

    SERVER_HOST: str = "localhost"
    SERVER_PORT: int = 5000
    WEBHOOK_HOST: str = "localhost"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
