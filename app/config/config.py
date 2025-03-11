import os

from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv('app/config/.env'))

aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_bucket_name = os.getenv("AWS_BUCKET_NAME")
aws_region = os.getenv("AWS_REGION")


class Settings(BaseSettings):
    AWS_SECRET_ACCESS_KEY: str = aws_secret_key
    AWS_ACCESS_KEY_ID: str = aws_access_key_id
    AWS_BUCKET_NAME: str = aws_bucket_name
    AWS_REGION: str = aws_region

    class Config:
        env_file = "config/.env"
        env_file_encoding = "utf-8"


settings = Settings()