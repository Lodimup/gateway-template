from typing import Literal

from pydantic_settings import BaseSettings


class S3Settings(BaseSettings):
    AWS_S3_ENDPOINT_URL: str
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_STORAGE_BUCKET_NAME: str


class CelerySettings(BaseSettings):
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str


class FastStreamSettings(BaseSettings):
    FAST_STREAM_BROKER_URL: str


class DjangoSettings(BaseSettings):
    DEPLOYENV: Literal["local", "dev", "stg", "prod"]
    DB_NAME: str
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: str

    DEBUG: bool
    ALLOWED_HOSTS: list[str]
    CORS_ALLOWED_ORIGINS: list[str]
    SECRET_KEY: str

    SERVICE_TOKEN: str
    REDIS_CACHE_URL: str


class LogfireSettings(BaseSettings):
    LOGFIRE_TOKEN: str | None = None


class AppSettings(
    S3Settings,
    CelerySettings,
    FastStreamSettings,
    DjangoSettings,
    LogfireSettings,
    BaseSettings,
): ...


APP_SETTINGS = AppSettings()  # type: ignore
