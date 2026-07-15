"""Application configuration.

Everything here is loaded from ENVIRONMENT VARIABLES (with sensible defaults),
never hardcoded. This is the 12-factor "config in the environment" principle:
the same image/binary runs in dev, CI, and prod — only the env vars change.

When we containerize, these become `-e LOG_LEVEL=DEBUG` flags and, later,
Kubernetes ConfigMaps/Secrets. Because it all funnels through this one file,
the rest of the app never has to care where a value came from.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # env_file is a convenience for local dev; in containers we pass real env vars.
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = "Notes API"
    environment: str = "development"  # override with ENVIRONMENT=production
    log_level: str = "INFO"          # override with LOG_LEVEL=DEBUG


# A single shared settings instance, imported wherever config is needed.
settings = Settings()
