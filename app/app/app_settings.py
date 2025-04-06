from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    DEPLOYENV: str
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
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str
    REDIS_CACHE_URL: str

    AWS_S3_ENDPOINT_URL: str
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_STORAGE_BUCKET_NAME: str


AppSettings = AppSettings()
