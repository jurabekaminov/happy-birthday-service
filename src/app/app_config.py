from datetime import UTC, timezone

from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    TITLE: str
    VERSION: str
    TZ: timezone = UTC
    
    model_config = SettingsConfigDict(
        env_prefix="APP_",
        env_file=".env"
    )

app_settings = AppSettings()
