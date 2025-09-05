from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

DEV_DATABASE_URL = "sqlite+aiosqlite:///./dev.db"


class Settings(BaseSettings):
    # General
    DEBUG: bool = True
    PROJECT_NAME: str = "Serious Connection"
    BASE_DIR: Path = Path(__file__).resolve().parent.parent

    # Database
    DATABASE_URL: str = DEV_DATABASE_URL

    # Mail
    MAIL_USERNAME: str = "noreply@serious-connection.com"
    MAIL_PASSWORD: str = ""
    MAIL_PORT: int = 1025
    MAIL_FROM: str = MAIL_USERNAME
    MAIL_SERVER: str = "localhost"
    MAIL_SSL_TLS: bool = not DEBUG
    MAIL_STARTTLS: bool = not DEBUG
    MAIL_USE_CREDENTIALS: bool = not DEBUG

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @field_validator("DEBUG", mode="before")
    @classmethod
    def parse_debug(cls, v):
        if isinstance(v, str):
            return v.lower() in ("1", "true", "yes", "on")
        return bool(v)

    @field_validator("MAIL_PORT", mode="before")
    @classmethod
    def parse_mail_port(cls, v):
        if isinstance(v, str):
            try:
                mail_port = int(v)
                return mail_port
            except ValueError:
                raise ValueError("MAIL_PORT must be an integer!")
            
        return v

    @field_validator("DATABASE_URL", mode="after")
    @classmethod
    def validate_database_url(cls, v, info):
        debug = info.data.get("DEBUG", True)

        if debug:
            # Always use Dev Database in debug mode
            return DEV_DATABASE_URL

        # When debug is False, ensure a proper Database URL is set
        if not v or v == DEV_DATABASE_URL:
            raise ValueError("DATABASE_URL must be set when DEBUG is False")

        return v


settings = Settings()
