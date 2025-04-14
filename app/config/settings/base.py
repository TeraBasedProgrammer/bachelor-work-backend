import pathlib

import decouple
from pydantic_settings import BaseSettings

ROOT_DIR = pathlib.Path(__file__).parent.parent.parent.parent.resolve()


class BackendBaseSettings(BaseSettings):
    WEB_URL: str = decouple.config("WEB_URL", default="http://localhost:3000")
    DEBUG: bool = decouple.config("DEBUG", cast=bool, default=True)
    LOGGING_LEVEL: str = decouple.config("LOGGING_LEVEL", default="DEBUG")
    REDIS_URL: str = decouple.config("REDIS_URL", default="redis://redis:6379")
    JWT_SECRET: str = decouple.config("JWT_SECRET")
    POSTGRES_USER: str = decouple.config("POSTGRES_USER")
    POSTGRES_PASSWORD: str = decouple.config("POSTGRES_PASSWORD")
    POSTGRES_DB: str = decouple.config("POSTGRES_DB")
    POSTGRES_PORT: int = decouple.config("POSTGRES_PORT", cast=int)
    POSTGRES_HOST: str = decouple.config("POSTGRES_HOST")
    IS_ALLOWED_CREDENTIALS: bool = decouple.config("IS_ALLOWED_CREDENTIALS", cast=bool)
    GOOGLE_AUTH_CLIENT_ID: str = decouple.config("GOOGLE_AUTH_CLIENT_ID")
    SMTP_HOST: str = decouple.config("SMTP_HOST")
    SMTP_PORT: int = decouple.config("SMTP_PORT", cast=int)
    SMTP_USER: str = decouple.config("SMTP_USER")
    SMTP_PASSWORD: str = decouple.config("SMTP_PASSWORD")
    ALLOWED_ORIGINS: list[str] = ["*"]
    ALLOWED_METHODS: list[str] = ["*"]
    ALLOWED_HEADERS: list[str] = ["*"]

    class Config:
        env_file = f"{ROOT_DIR}/.env"


settings = BackendBaseSettings()
