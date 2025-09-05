from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

DEV_DATABASE_URL = "sqlite:///./dev.db"


class Settings(BaseSettings):
    # General
    DEBUG: bool = True
    PROJECT_NAME: str = "Serious Connection"

    # Database
    DATABASE_URL: str = DEV_DATABASE_URL

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @field_validator("DEBUG", mode="before")
    @classmethod
    def parse_debug(cls, v):
        if isinstance(v, str):
            return v.lower() in ("1", "true", "yes", "on")
        return bool(v)

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
