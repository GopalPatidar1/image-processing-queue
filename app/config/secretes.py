import os
from enum import Enum
from pydantic_settings import BaseSettings, SettingsConfigDict

class AppEnvironment(str, Enum):
    TEST = "test"
    DEV = "dev"
    PROD = "prod"

APP_ENV = os.getenv("APP_ENV")

class Settings(BaseSettings):
    APP_ENV: AppEnvironment
    DB_URL: str
    DB_URL_SYNC: str

    model_config = SettingsConfigDict(
        env_file=f".env.{APP_ENV}",
        env_file_encoding="utf-8",
        extra="ignore",
    )

secretes = Settings()