import secrets
from pathlib import Path

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    # Base
    API_SERVER_PROJECT_NAME: str
    ENVIRONMENT: str
    API_PREFIX: str
    MARIADB_SERVER: str
    MARIADB_DATABASE: str
    MARIADB_USER: str
    MARIADB_PASSWORD: str

    ACCESS_TOKEN_EXPIRE_MINUTES: int
    ACCESS_TOKEN_SECRET_KEY: str = secrets.token_urlsafe(32)

    FIRST_SUPERUSER_EMAIL: EmailStr
    FIRST_SUPERUSER_USERNAME: str
    FIRST_SUPERUSER_PASSWORD: str

    class Config:
        env_file = Path(__file__).resolve().parent.parent.parent.parent / \
            ".env"  # get absolute path
        env_file_encoding = 'utf-8'


dev_path = Path(__file__).resolve().parent.parent.parent.parent / \
    ".env"  # get absolute path
settings = Settings(_env_file=dev_path, _env_file_encoding='utf-8')
