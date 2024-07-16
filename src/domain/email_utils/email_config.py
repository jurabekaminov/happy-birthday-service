from pydantic_settings import BaseSettings, SettingsConfigDict


class EmailSettings(BaseSettings):
    USER: str
    PASSWORD: str
    HOST: str
    PORT: int

    model_config = SettingsConfigDict(
        env_prefix="SMTP_",
        env_file=".env"
    )


email_settings = EmailSettings()
