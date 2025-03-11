from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv, find_dotenv


class Settings(BaseSettings):
    AWS_SECRET_ACCESS_KEY: str = "cEK7H7vKwmV9hzoGzkSvFj/Ac5tV3LO+zbHfoc/S"
    AWS_ACCESS_KEY_ID: str = "AKIAQFLZDHWYC4LPCRGC"
    AWS_BUCKET_NAME: str = "vivahcare-files"
    AWS_REGION: str = "us-east-2"

    class Config:
        env_file = "config/.env"
        env_file_encoding = "utf-8"


settings = Settings()