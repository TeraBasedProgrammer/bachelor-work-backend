import pathlib

import decouple
from pydantic_settings import BaseSettings

ROOT_DIR = pathlib.Path(__file__).parent.parent.parent.parent.resolve()


class BackendBaseSettings(BaseSettings):
    # Web
    WEB_URL: str = decouple.config("WEB_URL", default="http://localhost:3000")
    DEBUG: bool = decouple.config("DEBUG", cast=bool, default=True)
    LOGGING_LEVEL: str = decouple.config("LOGGING_LEVEL", default="DEBUG")
    REDIS_URL: str = decouple.config("REDIS_URL", default="redis://redis:6379")
    JWT_SECRET: str = decouple.config("JWT_SECRET")
    IS_ALLOWED_CREDENTIALS: bool = decouple.config("IS_ALLOWED_CREDENTIALS", cast=bool)
    GOOGLE_AUTH_CLIENT_ID: str = decouple.config("GOOGLE_AUTH_CLIENT_ID")

    # Database
    POSTGRES_USER: str = decouple.config("POSTGRES_USER")
    POSTGRES_PASSWORD: str = decouple.config("POSTGRES_PASSWORD")
    POSTGRES_DB: str = decouple.config("POSTGRES_DB")
    POSTGRES_PORT: int = decouple.config("POSTGRES_PORT", cast=int)
    POSTGRES_HOST: str = decouple.config("POSTGRES_HOST")

    # AWS
    AWS_ACCESS_KEY_ID: str = decouple.config("AWS_ACCESS_KEY_ID")
    AWS_SECRET_KEY: str = decouple.config("AWS_SECRET_KEY")
    AWS_REGION: str = decouple.config("AWS_REGION")
    AWS_BUCKET_NAME: str = decouple.config("AWS_BUCKET_NAME")
    AWS_S3_ENDPOINT: str = decouple.config("AWS_S3_ENDPOINT")

    # Stripe
    STRIPE_SECRET_KEY: str = decouple.config("STRIPE_SECRET_KEY")
    STRIPE_WEBHOOK_SECRET: str = decouple.config("STRIPE_WEBHOOK_SECRET")
    STRIPE_25_CREDITS_PRICE_ID: str = decouple.config("STRIPE_25_CREDITS_PRICE_ID")
    STRIPE_200_CREDITS_PRICE_ID: str = decouple.config("STRIPE_200_CREDITS_PRICE_ID")
    STRIPE_500_CREDITS_PRICE_ID: str = decouple.config("STRIPE_500_CREDITS_PRICE_ID")

    # SMTP
    SMTP_HOST: str = decouple.config("SMTP_HOST")
    SMTP_PORT: int = decouple.config("SMTP_PORT", cast=int)
    SMTP_USER: str = decouple.config("SMTP_USER")
    SMTP_PASSWORD: str = decouple.config("SMTP_PASSWORD")

    # CORS
    ALLOWED_ORIGINS: list[str] = ["*"]
    ALLOWED_METHODS: list[str] = ["*"]
    ALLOWED_HEADERS: list[str] = ["*"]

    class Config:
        env_file = f"{ROOT_DIR}/.env"


settings = BackendBaseSettings()
